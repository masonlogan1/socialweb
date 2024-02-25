"""
Provides objects and functions for packaging classes into a format the JSON-LD
engine can load
"""
import logging
from collections.abc import Iterable
from jsonld.base import JsonProperty, PropertyAwareObject
from jsonld.utils import CLASS_CHANGE_CONTEXT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class JsonLdPackage:
    """
    A discrete package of classes, properties, and transformation functions
    that can be given to the JSON-LD engine and used to process new and existing
    JSON-LD data

    All packages MUST have a unique namespace
    """

    def __init__(self, namespace: str, objects: Iterable = tuple(),
                 properties: Iterable = tuple(), property_mapping: dict = None):
        self.logger = logging.getLogger(f'JsonLdPackage_{namespace}')
        # TODO: save original objects as "templates" to be used when
        #   combining packages (immutable structure must be rebuilt each time)

        # TODO: cloned property classes need to be wrapped in such a way that
        #   any time a method (or property) returns a class that is in the,
        #   package, it should use the PACKAGE version of that class, not the
        #   CODE version of the class
        # namespace has to be set BEFORE ANYTHING ELSE HAPPENS, do not move it!
        self.namespace = namespace
        # classes are objects that the engine will produce from incoming data
        self.object_ref = self.__clone_classes(objects)
        self.objects = tuple(self.object_ref.values())
        # properties are managed attributes for classes
        self.property_ref = self.__clone_classes(properties)
        self.properties = tuple(self.object_ref.values())
        # property_mapping connects properties to classes on instantiation
        self.property_mapping = property_mapping

        self.__ref = {obj.__get_namespace__(): obj
                      for obj in self.objects + self.properties}

        self.__perform_mapping()

    @property
    def namespace(self):
        """
        Unique namespace for the publisher of this package
        :return:
        """
        return getattr(self, '___namespace___', None)

    @namespace.setter
    def namespace(self, ns):
        # can only be set once, during construction
        if self.namespace:
            raise AttributeError(f'JsonLdPackage namespace is immutable')
        if not isinstance(ns, str):
            raise TypeError(f'JsonLdPackage namespace must be a string, ' +
                            f'got {type(ns)}')
        self.___namespace___ = ns

    @property
    def objects(self):
        """
        Classes registered to this package
        :return: tuple of Class objects
        """
        return getattr(self, '___objects___', tuple())

    @objects.setter
    def objects(self, objects: Iterable):
        if self.objects:
            raise AttributeError(f'JsonLdPackage classes are immutable')
        for obj in objects:
            logger.info(f'Setting "{obj.__get_namespace__()}" in package ' +
                        f'"{self.namespace}" to class "{obj.__name__}"')
        self.___objects___ = objects

    @property
    def properties(self):
        return getattr(self, '___properties___', tuple())

    @properties.setter
    def properties(self, properties: dict):
        if self.properties:
            raise AttributeError(f'JsonLdPackage properties are immutable')
        for prop in properties:
            logger.info(f'Setting "{prop.__get_namespace__()}" in package ' +
                        f'"{self.namespace}" to property "{prop.__name__}"')
        self.___properties___ = properties

    def __perform_mapping(self):
        """
        Connects all properties to an object
        :return:
        """
        for object_namespace, property_classes in self.property_mapping.items():
            self.link_properties(property_classes, object_namespace)
            self[object_namespace].__get_properties__(refresh=True)

    def link_property(self, property_class: JsonProperty,
                      object_class: PropertyAwareObject):
        """
        Connects a given property to the specified class. Extracts the property
        details from the JsonProperty's registration and adds it to the
        PropertyAwareObject in a way that allows it to function as a normally
        added @property (or @contextualproperty) structure
        :param property_class: JsonProperty to add to a PropertyAwareObject
        :param object_class: PropertyAwareObject to accept the new property
        :return:
        """
        setattr(object_class, property_class.__get_property_name__(),
                property(*property_class.__get_registration__()))

    def link_properties(self, property_classes: Iterable[JsonProperty],
                        object_namespace: str):
        object_class = self[object_namespace]
        if not object_class:
            raise ValueError(f'No such object "{object_namespace}" in package' +
                             f' "{self.namespace}"')
        for property_class in property_classes:
            self.link_property(property_class, object_class)

    def update_property_link(self, property_class: JsonProperty,
                             object_class: PropertyAwareObject):
        setattr(object_class, property_class.__get_property_name__(),
                property(*property_class.__get_registration__()))

    def remove_property_link(self, property_name: str,
                             object_class: PropertyAwareObject):
        delattr(object_class, property_name)

    def __wrap_callables(self, cls):
        """
        Wraps anything callable for a class with a function that changes the
        type of return values if the class of the value is in the package.
        """
        def wrapper(fn):
            def wrap_return(*args, **kwargs):
                if (val := fn(*args, **kwargs)).__class__ not in self.object_ref.keys():
                    return val
                with val.switch_context(CLASS_CHANGE_CONTEXT):
                    return self.__change_class(val, self.object_ref.get(val.__class__))
            return wrap_return
        # locate anything callable and wrap it so output values will be mapped,
        # when applicable
        for name, method in cls.__dict__.items():
            if callable(method):
                setattr(cls, name, wrapper(method))

    def __change_class(self, obj, new_class):
        # fetch the property values, if any, that are applicable; then
        # fetch the current property values, if any, so that if the new class
        # does not implement the same properties, the values will be transferred
        # to the new class as attributes to avoid data loss when handling
        # the same data in different packages
        props = {name: getattr(obj, name, None)
                 for name in getattr(new_class, '__properties__', ())}
        attrs = {name: getattr(obj, name, None)
                 for name in getattr(obj, '__properties__', ())}
        # merge both for simplicity and to avoid setting the same values twice
        data = {**props, **attrs}
        obj.__class__ = new_class
        obj.__properties__ = obj.__get_properties__(refresh=True)
        for name, val in data.items():
            try:
                setattr(obj, name, val)
            except AttributeError as e:
                self.logger.exception(f'Could not set {name}')
        return obj

    def __clone_classes(self, classes):
        """
        Clones the base objects used to create the package. Copying the classes
        allows the base objects to remain unchanged (i.e. the original objects
        do not have their properties linked or functionality altered outside
        the package)
        :param classes:
        :return:
        """
        # creates a dictionary that organizes classes based on how many
        # package-internal dependencies they have
        ordered = {}
        for cls in classes:
            deps = [c for c in classes if c in cls.mro() and c != cls]
            ordered[len(deps)] = ordered.get(len(deps), []) + [cls]

        # creates a list where classes are sorted by their number of deps
        classes = []
        for val in sorted(ordered.keys()):
            classes += ordered[val]

        class_ref = {cls: None for cls in classes}

        for cls in classes:
            # IF there is a cloned class for a dependency (root will not have!)
            # THEN have the dependent cloned class inherit from it
            inherits = [val for obj, val in class_ref.items()
                        if obj in cls.mro() and val is not None]
            inherits = (cls,) if not inherits else (inherits[-1], cls)
            class_ref[cls] = type(cls.__name__, inherits, cls.__dict__.copy())
            self.__wrap_callables(class_ref[cls])
        return class_ref

    def __getitem__(self, keys):
        if isinstance(keys, str):
            return self.__ref.get(keys, None)
        if any(not isinstance(key, str) for key in keys):
            raise ValueError('JsonLdPackage getitem can only accept strings')
        return [self.__ref.get(key, None) for key in keys]

    def __str__(self):
        # this should probably return the name of the package
        return f'JsonLdPackage {self.namespace}'

    def __add__(self, other):
        if not isinstance(other, JsonLdPackage):
            raise TypeError(f'Cannot combine JsonLdPackage with {type(other)}')
        new_namespaces = [cls.__get_namespace__() for cls in other.classes]
        kept_classes = tuple(cls for cls in self.classes
                             if cls.__get_namespace__() not in new_namespaces)
        classes = kept_classes + other.classes

        new_namespaces = [prp.__get_namespace__() for prp in other.properties]
        kept_props = tuple(prp for prp in self.properties
                           if prp.__get_namespace__() not in new_namespaces)
        properties = kept_props + other.properties

        return JsonLdPackage(namespace=self.namespace, classes=classes,
                             properties=properties)

    def __sub__(self, other):
        if not isinstance(other, JsonLdPackage):
            raise TypeError(f'Cannot subtract {type(other)} from JsonLdPackage')
        removed_cls_ns = [cls.__get_namespace__() for cls in other.classes]
        remaining_cls = tuple(cls for cls in self.classes
                              if cls.__get_namespace__() not in removed_cls_ns)

        removed_prp_ns = [cls.__get_namespace__() for cls in other.classes]
        remaining_prps = tuple(prp for prp in other.properties
                               if prp.__get_namespace__() not in removed_prp_ns)

        return JsonLdPackage(namespace=self.namespace,
                             classes=remaining_cls,
                             properties=remaining_prps)

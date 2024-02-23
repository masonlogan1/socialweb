"""
Provides objects and functions for packaging classes into a format the JSON-LD
engine can load
"""
import logging
from collections.abc import Iterable
from jsonld.base import JsonProperty, PropertyAwareObject

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class JsonLdPackage:
    """
    A discrete package of classes, properties, and transformation functions
    that can be given to the JSON-LD engine and used to process new and existing
    JSON-LD data

    All packages MUST have a unique namespace
    """
    def __init__(self, namespace: str, classes: Iterable = tuple(),
                 properties: Iterable = tuple(), property_mapping: dict = None,
                 *args, **kwargs):
        # namespace has to be set BEFORE ANYTHING ELSE HAPPENS, do not move it!
        self.namespace = namespace
        # classes are objects that the engine will produce from incoming data
        self.classes = classes
        # properties are managed attributes for classes
        self.properties = properties
        # property_mapping connects properties to classes on instantiation
        self.property_mapping = property_mapping

        self.__ref = {obj.__get_namespace__(): obj
                      for obj in self.classes + self.properties}

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
    def classes(self):
        """
        Classes registered to this package
        :return: tuple of Class objects
        """
        return getattr(self, '___classes___', tuple())

    @classes.setter
    def classes(self, classes: Iterable):
        if self.classes:
            raise AttributeError(f'JsonLdPackage classes are immutable')
        for cls in classes:
            logger.info(f'Setting "{cls.__get_namespace__()}" in package ' +
                        f'"{self.namespace}" to class "{cls.__name__}"')
        self.___classes___ = classes

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

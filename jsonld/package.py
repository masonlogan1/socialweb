"""
Provides objects and functions for packaging classes into a format the JSON-LD
engine can load
"""
import logging
from collections.abc import Iterable
from jsonld.base import JsonProperty, PropertyAwareObject
from jsonld.kamino import ClassCloner

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class JsonLdPackage(ClassCloner):
    """
    A discrete package of classes, properties, and transformation functions
    that can be given to the JSON-LD engine and used to process new and existing
    JSON-LD data

    All packages MUST have a unique namespace
    """
    def __init__(self, namespace: str, objects: Iterable = tuple(),
                 properties: Iterable = tuple(), property_mapping: dict = None):
        # namespace has to be set BEFORE ANYTHING ELSE HAPPENS, do not move it!
        self.namespace = namespace
        self.logger = logging.getLogger(f'JsonLdPackage_{namespace}')
        # classes are objects that the engine will produce from incoming data
        self.object_ref = self.clone_classes(objects)
        self.objects = tuple(self.object_ref.values())
        # properties are managed attributes for classes
        self.property_ref = self.clone_classes(properties)
        self.properties = tuple(self.property_ref.values())
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
        for object_namespace, property_namespaces in self.property_mapping.items():
            self.link_properties(property_namespaces, object_namespace)
        for object in self.objects:
            object.__get_properties__(refresh=True)

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
        # setattr(object_class, property_class.__get_property_name__(),
        #         property(*property_class.__get_registration__()))
        setattr(object_class, property_class.__get_property_name__(),
                property_class.__get_property__())

    def link_properties(self, property_namespaces: Iterable[str],
                        object_namespace: str):
        object_class = self[object_namespace]
        if not object_class:
            raise ValueError(f'No such object "{object_namespace}" in package' +
                             f' "{self.namespace}"')
        for property_namespace in property_namespaces:
            property_class = self[property_namespace]
            if not property_class:
                raise ValueError(f'No such property "{property_namespace}" ' +
                                 f'in package "{self.namespace}"')
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
        new_namespaces = [cls.__get_namespace__() for cls in other.objects]
        kept_classes = tuple(cls for cls in self.objects
                             if cls.__get_namespace__() not in new_namespaces)
        objects = kept_classes + other.objects

        new_namespaces = [prp.__get_namespace__() for prp in other.properties]
        kept_props = tuple(prp for prp in self.properties
                           if prp.__get_namespace__() not in new_namespaces)
        properties = kept_props + other.properties

        return JsonLdPackage(namespace=self.namespace, objects=objects,
                             properties=properties)

    def __sub__(self, other):
        if not isinstance(other, JsonLdPackage):
            raise TypeError(f'Cannot subtract {type(other)} from JsonLdPackage')
        removed_obj_ns = [cls.__get_namespace__() for cls in other.objects]
        remaining_objs = tuple(cls for cls in self.objects
                              if cls.__get_namespace__() not in removed_obj_ns)

        removed_prp_ns = [cls.__get_namespace__() for cls in other.properties]
        remaining_prps = tuple(prp for prp in other.properties
                               if prp.__get_namespace__() not in removed_prp_ns)

        return JsonLdPackage(namespace=self.namespace,
                             objects=remaining_objs,
                             properties=remaining_prps)

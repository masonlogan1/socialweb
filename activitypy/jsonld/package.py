"""
Provides objects and functions for packaging classes into a format the JSON-LD
engine can load
"""
import logging
from collections.abc import Iterable

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# TODO: should be immutable, add/sub should return a NEW package
class JsonLdPackage:
    """
    A discrete package of classes, properties, and transformation functions
    that can be given to the JSON-LD engine and used to process new and existing
    JSON-LD data

    All packages MUST have a unique namespace
    """

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

    def __init__(self, namespace: str, classes: Iterable = tuple(),
                 properties: Iterable = tuple(), *args, **kwargs):
        # namespace has to be set BEFORE ANYTHING ELSE HAPPENS, do not move it!
        self.namespace = namespace

        # classes are objects that the engine will produce from incoming data
        self.classes = classes
        # properties are managed attributes for classes
        self.properties = properties

    def __getitem__(self, key):
        # need to decide what the return format should look like and how slicing
        # would work here
        raise NotImplementedError("Cannot get item from JsonLdPackage objects")

    def __str__(self):
        # this should probably return the name of the package
        return f'JsonLdPackage {self.namespace}'

    def __add__(self, other):
        if not isinstance(other, JsonLdPackage):
            raise TypeError(f'Cannot combine JsonLdPackage with {type(other)}')
        class_namespaces = [cls.__get_namespace__() for cls in self.classes]
        new_classes = [cls for cls in other.classes
                       if cls.__get_namespace__() not in class_namespaces]
        new_classes = tuple(list(self.classes) + new_classes)

        prop_namespaces = [prp.__get_namespace__() for prp in self.properties]
        new_props = [prp for prp in other.properties
                     if prp.__get_namespace__() not in prop_namespaces]
        new_props = tuple(list(self.properties) + new_props)

        return JsonLdPackage(namespace=self.namespace, classes=new_classes,
                             properties=new_props)

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

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

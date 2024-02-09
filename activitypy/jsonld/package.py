"""
Provides objects and functions for packaging classes into a format the JSON-LD
engine can load
"""
import logging
from collections.abc import Iterable
from hashlib import sha256

from activitypy.jsonld.jsonld import ApplicationActivityJson
from activitypy.jsonld.base import JsonProperty

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        return self.__namespace

    @namespace.setter
    def namespace(self, ns):
        # can only be set once, during construction
        if getattr(self, 'namespace', None):
            raise AttributeError(f'JsonLdPackage namespace is immutable')
        if not isinstance(ns, str):
            # TODO: enforce type-safety by checking inheritance of base classes
            raise TypeError(f'JsonLdPackage namespace must be a string, ' +
                            f'got {type(ns)}')
        self.__namespace = ns

    @property
    def classes(self):
        """
        Classes registered to this package
        :return: tuple of Class objects
        """
        return getattr(self, '_JsonLdPackage__classes', dict())

    @classes.setter
    def classes(self, classes: dict):
        # classes must always be a dict
        if not isinstance(classes, dict):
            raise TypeError(f"'classes' MUST be a dict or dict-like object")
        # enforces type safety
        if (bad_classes := [cls.__name__ for cls in classes.values()
                            if not issubclass(cls, ApplicationActivityJson)]):
            raise ValueError(f'''cannot add "{'", "'.join(bad_classes)}" ''' +
                             f'to package "{self.namespace}", classes added ' +
                             'to package MUST inherit from activitypy.jsonld.' +
                             'ApplicationActivityJson')
        # logs changes to package
        for id, cls in classes.items():
            # TODO: enforce type-safety by checking inheritance of base classes
            logger.info(f'Setting "{id}" in package "{self.namespace}" ' +
                        f'to class "{cls.__name__}"')
        self.__classes = classes

    @property
    def properties(self):
        return getattr(self, '_JsonLdPackage__properties', dict())

    @properties.setter
    def properties(self, properties: dict):
        if not isinstance(properties, dict):
            raise TypeError(f"'properties' MUST be a dict or dict-like object")
        # enforces type safety
        if (bad_props := [cls.__name__ for cls in properties.values()
                          if not issubclass(cls, JsonProperty)]):
            raise ValueError(
                f'''cannot add "{'", "'.join(bad_props)}" ''' +
                f'to package "{self.namespace}", properties added ' +
                'to package MUST inherit from activitypy.jsonld.' +
                'JsonProperty')
        for id, prop in properties.items():
            # TODO: enforce type-safety by checking inheritance of base classes
            logger.info(f'Setting "{id}" in package "{self.namespace}" ' +
                        f'to property class "{prop.__name__}"')
        self.__properties = properties

    @property
    def transforms(self):
        return getattr(self, '_JsonLdPackage__transforms', dict())

    @transforms.setter
    def transforms(self, transforms: dict):
        if not isinstance(transforms, dict):
            raise TypeError(f"'transforms' MUST be a dict or dict-like object")
        bad_pairs = [f'({type(cls)}: {type(fn)})'
                     for cls, fn in transforms.items()
                     if not issubclass(cls, ApplicationActivityJson)
                     or not callable(fn)]
        if bad_pairs:
            raise ValueError(
                f'cannot add transforms to package "{self.namespace}", ' +
                f'each transform must map a class inheriting from activitypy.' +
                f'jsonld.ApplicationActivityJson to a callable; ' +
                f'''found "{', '.join(bad_pairs)}"''')
        for cls, func in transforms.items():
            logger.info(f'Setting transform function for "{cls.__name__}" ' +
                        f'in package "{self.namespace}" to function '
                        f'"{func.__name__}"')
        self.__transforms = transforms

    def __init__(self, namespace: str, classes: Iterable = None,
                 properties: Iterable = None, transforms: Iterable = None,
                 *args, **kwargs):
        # namespace has to be set BEFORE ANYTHING ELSE HAPPENS, do not move it!
        self.namespace = namespace

        # classes are objects that the engine will produce from incoming data
        self.classes = classes or dict()
        # properties are managed attributes for classes
        self.properties = properties or dict()
        self.transforms = transforms or dict()

    def __iter__(self):
        # need to decide how we should iterate over the data
        raise NotImplementedError("JsonLdPackage objects cannot be iterated")

    def __getitem__(self, key):
        # need to decide what the return format should look like and how slicing
        # would work here
        raise NotImplementedError("Cannot get item from JsonLdPackage objects")

    def __str__(self):
        # this should probably return the name of the package
        raise NotImplementedError("Can't convert JsonLdPackage into a string")

    def __hash__(self):
        # the hash should be derived from the namespace
        return hash(self.namespace)

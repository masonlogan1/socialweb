"""
Module for storing the JsonLdEngine class, which is capable of transforming
json text into python objects (and vice-versa) based on the loaded packages
"""
import logging
from collections.abc import Iterable
from typing import Iterable as typeIterable

from jsonld.engine.json_input import PropertyJsonIntake
from jsonld.package import JsonLdPackage


class JsonLdEngine(PropertyJsonIntake):

    def __init__(self, packages: JsonLdPackage | typeIterable[JsonLdPackage]):
        """
        :param packages: the packages to load into the engine
        """
        # keeps a copy of all the packages provided
        packages = (packages,) if not isinstance(packages, Iterable) else packages
        self.___packages___ = packages
        if not self.packages:
            raise ValueError(f'No packages provided!')

        self.logger = logging.getLogger(f'JsonLdEngine')

        # combines all packages into a single package before unpacking
        self.package = self.packages[0]
        for package in self.packages[1:]:
            self.package += package

        self.__load_objects()

    @property
    def packages(self):
        if not hasattr(self, '___packages___'):
            self.__packages___ = tuple()
        return self.___packages___

    def __load_objects(self) -> None:
        """
        Unpacks the contents of the package into a usable format
        :param package: the package to unpack
        """
        for cls in self.package.objects:
            # registers/updates each type by its namespace id
            if cls.__get_namespace__() not in self.class_registry.keys():
                self.register_class(cls.__get_namespace__(), cls)

        for name, cls in self.class_registry.items():
            # adds the object classes as attributes on the engine
            if hasattr(self, cls.__name__):
                self.logger.error(
                    f'Name {cls.__name__} conflicts with existing attribute, ' +
                    f'engine may be become unstable!'
                )
            self._add_class_to_engine(cls)

    def _add_class_to_engine(self, cls, name=None):
        """

        :param cls: the class to make available as an attribute of the engine
        :param name: the name to use
        :return:
        """
        name = name if name else cls.__name__
        self.logger.info(f"Adding {cls.__name__} to engine as '{name}'")
        setattr(self, name, cls)

    def register_class(self, name, cls):
        """
        Adds a name-class mapping to the engine's class registry
        :param name: the fully qualified namespace id to associate with the class
        :param cls: the new object class
        """
        self.logger.info(f'Registering jsonld type "{name}" as {cls.__name__}')
        if name in self.class_registry.keys():
            raise ValueError(f'"{name}" already exists in mapping, cannot add')
        self.class_registry.update({name: cls})
        # give registered classes a reference back to their engine
        setattr(cls, '__jsonld_engine__', self)

    # TODO: set up method that handles queues and connect to __getitem__ for
    #   easy handling of a data queue (vital for multithreading!)
    def __getitem__(self, keys):
        # allows for the creation of json objects by passing in json text with
        # a syntax similar to list item selection
        return_one = False
        if isinstance(keys, str):
            return_one = True
            keys = [keys]
        if not isinstance(keys, (list, tuple)):
            raise TypeError('JsonLdEngine list accepts json-formatted text ' +
                            f'or a list/tuple of strings, not {type(keys)}')
        if any(not isinstance(key, str) for key in keys):
            raise TypeError(f'JsonLdEngine list provided with {type(keys)} ' +
                            'must contain only json-format strings')
        if return_one:
            return self.from_json(keys[0])
        return [self.from_json(key) for key in keys]

    def __add__(self, other):
        if isinstance(other, JsonLdPackage):
            return JsonLdEngine(self.packages + other)

        if isinstance(other, JsonLdEngine):
            # combine packages from both engines with the second engine's
            # packages layered on top of this engine's
            return JsonLdEngine(self.packages + other.packages)

        raise TypeError(f'Can only add "JsonLdPackage" and "JsonLdEngine" to ' +
                        'JsonLdEngine objects')

    def __sub__(self, other):
        if isinstance(other, JsonLdPackage):
            return JsonLdEngine(self.packages - other)

        if isinstance(other, JsonLdEngine):
            return JsonLdEngine(self.packages - other.packages)

        raise TypeError(f'Can only subtract "JsonLdPackage" and ' +
                        f'"JsonLdEngine" from JsonLdEngine objects')

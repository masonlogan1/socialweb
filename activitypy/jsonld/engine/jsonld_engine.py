"""
Module for storing the JsonLdEngine class, which is capable of transforming
json text into python objects (and vice-versa) based on the loaded packages
"""
import logging
from collections.abc import Iterable
from typing import Iterable as typeIterable

from activitypy.jsonld.engine.json_input import PropertyJsonIntake
from activitypy.jsonld.package import JsonLdPackage


# TODO: needs to be immutable
#   o combine packages IN ORDER into single package
#   o unpack package into engine and make properties read-only
#       - i.e. "read any/write ONCE"
class JsonLdEngine(PropertyJsonIntake):

    def __init__(self, packages: JsonLdPackage | typeIterable[JsonLdPackage]):
        """
        :param packages: the packages to load into the engine
        """
        # keeps a copy of all the packages provided
        packages = (packages,) if packages is not Iterable else packages
        self.___packages___ = packages
        if not self.packages:
            raise ValueError(f'No packages provided!')

        self.logger = logging.getLogger(f'JsonLdEngine')

        # combines all packages into a single package before unpacking
        self.package = self.packages[0]
        for package in self.packages[1:]:
            self.package += package

        self.__load_classes()
        self.__load_properties()

    @property
    def packages(self):
        if not hasattr(self, '___packages___'):
            self.__packages___ = tuple()
        return self.___packages___

    def __load_classes(self) -> None:
        """
        Unpacks the contents of the package into a usable format
        :param package: the package to unpack
        """
        for cls in self.package.classes:
            # registers/updates each type by its namespace id
            if cls.__get_namespace__() not in self.class_registry.keys():
                self.register_class(cls.__get_namespace__(), cls)
                continue
            self.update_class(cls.__get_namespace__(), cls)

    def __load_properties(self) -> None:
        """
        Unpacks the contents of the package into a usable format
        :param package: the package to unpack
        """
        for cls in self.package.properties:
            # registers/updates each type by its namespace id
            if cls.__get_namespace__() not in self.class_registry.keys():
                self.register_property(cls.__get_namespace__(), cls)
                continue
            self.update_property(cls.__get_namespace__(), cls)

    def register_class(self, name, cls):
        """
        Adds a name-class mapping to the engine's class registry
        :param name: the fully qualified namespace id to associate with the class
        :param cls: the new object class
        """
        self.logger.info(f'Registering jsonld type "{name}" as {cls.__name__}')
        if name in self.class_registry.keys():
            raise ValueError(
                f'"{name}" already exists in mapping, cannot add new')
        self.class_registry.update(**{name: cls})

    def update_class(self, name, cls):
        """
        Adds a name-class mapping to the engine's class registry
        :param name: the fully qualified namespace id to associate with the class
        :param cls: the new object class
        """
        self.logger.info(f'Updating jsonld type "{name}" to {cls.__name__}')
        if name not in self.class_registry.keys():
            self.logger.info(f'registration update for type "{name}" ' +
                                f'made but type does not exist')
        self.class_registry.update({name: cls})

    def remove_class(self, name, cls):
        if name not in self.class_registry.keys():
            self.logger.warning(f'no registration update for type "{name}"; ' +
                                f'no action taken, remediate if possible')
            return
        self.logger.info(f'removing registry for type "{name}"')
        self.class_registry.pop(name)

    def register_property(self, name, cls):
        """
        Adds a name-class mapping to the engine's property registry
        :param name: the fully qualified namespace id to associate with the class
        :param cls: the new object class
        """
        self.logger.info(f'Registering jsonld type "{name}" as {cls.__name__}')
        if name in self.property_registry.keys():
            raise ValueError(
                f'"{name}" already exists in mapping, cannot add new')
        self.property_registry.update(**{name: cls})

    def update_property(self, name, cls):
        """
        Adds a name-class mapping to the engine's property registry
        :param name: the fully qualified namespace id to associate with the class
        :param cls: the new object class
        """
        self.logger.info(f'Updating jsonld type "{name}" to {cls.__name__}')
        if name not in self.property_registry.keys():
            self.logger.info(f'registration update for type "{name}" ' +
                                f'made but type does not exist; adding instead')
        self.property_registry.update({name: cls})

    def remove_property(self, name, cls):
        if name not in self.property_registry.keys():
            self.logger.warning(f'no registration update for type "{name}"; ' +
                                f'no action taken, remediate if possible')
            return
        self.logger.info(f'removing registry for type "{name}"')
        self.property_registry.pop(name)

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

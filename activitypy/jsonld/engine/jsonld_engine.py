"""
Module for storing the JsonLdEngine class, which is capable of transforming
json text into python objects (and vice-versa) based on the loaded packages
"""
import logging
from collections.abc import Iterable
from typing import Iterable as typeIterable

from activitypy.jsonld.engine.json_input import PropertyJsonIntake
from activitypy.jsonld.package import JsonLdPackage


class JsonLdEngine(PropertyJsonIntake):

    def __init__(self, engine_ns,
                 package: JsonLdPackage | typeIterable[JsonLdPackage]):
        """
        :param engine_ns: fully-qualified URI namespace for the engine
        :param package: the package to load into the engine
        """
        self.namespace = engine_ns
        self.packages = (package,) if package is not Iterable else package
        self.logger = logging.getLogger(f'JsonLdEngine_{engine_ns}')

        for package in self.packages:
            self.add_package(package)

    @property
    def property_registry(self):
        if not hasattr(self, '___property_registry___'):
            self.___property_registry___ = dict()
        return self.___property_registry___

    @property
    def transform_registry(self):
        if not hasattr(self, '___transform_registry___'):
            self.___transform_registry___ = dict()
        return self.___transform_registry___

    def add_package(self, package: JsonLdPackage):
        """
        Adds the contents of the new package to the engine
        :param package:
        :return:
        """
        self.__load_classes(package.classes)

    def __load_classes(self, classes) -> None:
        """
        Unpacks the contents of the package into a usable format
        :param package: the package to unpack
        """
        for cls in classes:
            # registers/updates each type by its namespace id
            if cls.__get_namespace__() not in self.class_registry.keys():
                self.register_property(cls.__get_namespace__(), cls)
                continue
            self.update_property(cls.__get_namespace__(), cls)

    def __load_properties(self, properties) -> None:
        """
        Unpacks the contents of the package into a usable format
        :param package: the package to unpack
        """
        for cls in properties:
            # registers/updates each type by its namespace id
            if cls.__get_namespace__() not in self.class_registry.keys():
                self.register_class(cls.__get_namespace__(), cls)
                continue
            self.update_class(cls.__get_namespace__(), cls)

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
            self.logger.warning(f'registration update for type "{name}" ' +
                                f'made but type does not exist; adding instead')
            return self.register_class(name, cls)
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
            self.logger.warning(f'registration update for type "{name}" ' +
                                f'made but type does not exist; adding instead')
            return self.register_class(name, cls)
        self.property_registry.update({name: cls})

    def remove_property(self, name, cls):
        if name not in self.property_registry.keys():
            self.logger.warning(f'no registration update for type "{name}"; ' +
                                f'no action taken, remediate if possible')
            return
        self.logger.info(f'removing registry for type "{name}"')
        self.property_registry.pop(name)

    def register_transform(self, name, cls):
        """
        Adds a name-class mapping to the engine's transform mapping
        :param name: the fully qualified namespace id to associate with the class
        :param cls: the new object class
        """
        self.logger.info(f'Registering jsonld type "{name}" as {cls.__name__}')
        if name in self.property_registry.keys():
            raise ValueError(
                f'"{name}" already exists in mapping, cannot add new')
        self.property_registry.update(**{name: cls})

    def update_transform(self, name, cls):
        """
        Adds a name-class mapping to the engine's transform mapping
        :param name: the fully qualified namespace id to associate with the class
        :param cls: the new object class
        """
        self.logger.info(f'Updating jsonld type "{name}" to {cls.__name__}')
        if name not in self.property_registry.keys():
            self.logger.warning(f'registration update for type "{name}" ' +
                                f'made but type does not exist; adding instead')
            return self.register_class(name, cls)
        self.property_registry.update({name: cls})

    def remove_transform(self, name, cls):
        if name not in self.property_registry.keys():
            self.logger.warning(f'no registration update for type "{name}"; ' +
                                f'no action taken, remediate if possible')
            return
        self.logger.info(f'removing registry for type "{name}"')
        self.property_registry.pop(name)

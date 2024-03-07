"""
Classes and functions for managing a single object database
"""
from collections.abc import Iterable

from citrine.node import CitrineConnection
from persistent import Persistent


class CitrineCrystal(Persistent):
    """
    Object capable of being persisted to a CitrineNode database
    """

    @classmethod
    def rebuild(cls, crystal) -> object:
        """
        Takes a CitrineCrystal and rebuilds the original object from it as
        closely as possible
        :param crystal: the persistent CitrineCrystal object to be rebuilt
        :return: the reconstructed object
        """

    @classmethod
    def crystallize(cls, obj: object):
        """
        Takes an object, extracts everything possible from it, and returns a
        CitrineCrystal object that can be persisted into the database
        :param obj: the object to be persisted into the database
        :return: the CitrineCrystal created from the object
        """


class CitrineDB(CitrineConnection):
    """
    Represents a node intended to handle jsonld.ApplicationActivityJson objects
    """
    def create(self, id: str, obj):
        """
        Converts the object into a persistable format and stores it to the
        database
        :param id:
        :param obj:
        :return:
        """
        if self.root.container.exists(id):
            raise ValueError(f'Object with id "{id}" already exists')
        with self:
            self.root.container.save(id, obj)

    def read(self, id):
        """
        Retrieves the object from the database and returns it to its original
        format
        :param id:
        :return:
        """
        if not self.root.container.exists(id):
            raise ValueError(f'No object with id "{id}" in the database')
        return self.root.container.get(id)

    def update(self, id, obj: object):
        """
        Locates the object by the given id and updates it to the new object
        :param id:
        :param obj:
        :return:
        """
        with self:
            self.root.container.save(id, obj)

    def delete(self, id):
        """
        Locates the object by the given id and removes it from the database
        :param id:
        :return:
        """
        with self:
            self.root.container.delete(id)

    def __getitem__(self, keys):
        """
        Shortcut for the read method that can return multiple entities
        """
        if isinstance(keys, slice):
            raise TypeError(f'{self.__class__} indices must be strings or '
                            'iterables of strings, not slice')
        if isinstance(keys, str):
            return self.read(keys)
        return [self.read(id) for id in keys]

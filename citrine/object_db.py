"""
Classes and functions for managing a single object database
"""

from citrine.node import DbNode
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


class CitrineNode(DbNode):
    """
    Represents a node intended to handle jsonld.ApplicationActivityJson objects
    """

    def create(self, obj: object):
        """
        Converts the object into a persistable format and stores it to the
        database
        :param obj:
        :return:
        """

    def read(self, id):
        """
        Retrieves the object from the database and returns it to its original
        format
        :param id:
        :return:
        """

    def update(self, id, obj: object):
        """
        Locates the object by the given id and updates it to the new object
        :param id:
        :param obj:
        :return:
        """

    def delete(self, id):
        """
        Locates the object by the given id and removes it from the database
        :param id:
        :return:
        """

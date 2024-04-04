import uuid
import logging

from persistent import Persistent
from persistent.mapping import PersistentMapping

class Metadata(Persistent):
    """
    Object used by a CitrineConnection as a form of metadata on the contents of
    the database
    """

    def __init__(self, size=None, cache=None):
        super().__init__()
        self.size = size
        self.cache = cache


class Container(Persistent):
    """
    Object used to manage a collection of PersistentMapping objects within
    an object database. Uses the hash value of the object to determine which
    container it should be kept in.
    """

    @property
    def containers_size(self):
        return len(self.containers.keys())

    @property
    def size(self):
        return sum((len(con.keys()) for con in self.containers.values()))

    def __init__(self, containers: dict | PersistentMapping = None):
        super().__init__()
        # Containers will be stored as a PM of PMs
        self.containers = containers if containers is not None else \
            PersistentMapping({0: PersistentMapping()})

    def expand_size(self, new_size: int):
        if new_size <= self.containers_size:
            raise ValueError(f'Cannot expand from {self.containers_size} ' +
                             f'containers to {new_size} containers, new size ' +
                             f'must be larger than existing size')
        self.containers = PersistentMapping({
            key: self.containers.get(key, PersistentMapping())
            for key in range(new_size)
        })

    def has(self, id) -> bool:
        """
        Return a bool describing whether the object is already present in the
        database
        :param id:
        :return:
        """
        return id in self.__locate_container(id).keys()

    def read(self, id):
        """
        Return an object by the given id
        :param id:
        :return:
        """
        return self.__locate_container(id).get(id, None)

    def write(self, id, obj):
        """
        Save an object to the database at the given id location
        :param obj:
        :param id:
        :return:
        """
        self.__locate_container(id)[id] = obj

    def delete(self, id):
        """
        Remove an object from the database by the given id
        :param id:
        :return:
        """
        self.__locate_container(id).pop(id)

    def __locate_container(self, id: str):
        """
        Locate the appropriate container based on the provided id value
        :param id:
        :return:
        """
        # ensure we get the same value each time
        val = int.from_bytes(str(id).encode(), 'big')
        val = val % self.containers_size
        return self.containers[val]
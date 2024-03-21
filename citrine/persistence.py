"""
Objects and functions for persisting incoming objects in a safe, recoverable
format. Objects are deconstructed and their component forms are stored in
a CitrineCrystal, which is capable of reconstructing the object.
"""
import uuid
import logging

from persistent import Persistent
from persistent.mapping import PersistentMapping
from transaction import ThreadTransactionManager, TransactionManager

# "why does EVERYTHING say citrine??" because I named things that work in a
# very specific way with each other and should not be replaced with default
# zodb components as "citrine" + original name

class CitrineTransactionManager(TransactionManager):
    """
    Single-threaded transaction manager for persisting objects to a Citrine
    Database.

    Builds on the existing ``transaction.TransactionManager`` by providing
    decorators that allow the manager to make individual methods transactional
    and the ability to give each transaction a unique UUID for logging any
    action carried out in a transaction
    """

    def __init__(self, explicit=False):
        super().__init__(explicit=explicit)
        self.autocommit = True
        self.logger = logging.getLogger('CTransManager')
        self.logger.setLevel(logging.INFO)

    def __enter__(self):
        self.transaction_uuid = uuid.uuid4()
        self.logger.info(f'START TRANSACTION {self.transaction_uuid}')
        self.autocommit = False
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.commit()
            self.logger.info(f'TRANSACTION {self.transaction_uuid} SUCCESSFUL')
        else:
            self.abort()
            self.logger.error(f'TRANSACTION {self.transaction_uuid} FAILED')
        self.autocommit = True
        self.transaction_uuid = None


class CitrineThreadTransactionManager(ThreadTransactionManager):
    """
    Thread-local CitrineTransactionManager that creates a copy in the thread
    that this object is used in.
    """

    def __init__(self):
        super().__init__()
        self.manager = CitrineTransactionManager()


def autocommit(fn):
    """
    Decorator designed to work with CitrineTransactionManager. Decorator will
    automatically commit so long as the transaction manager's autocommit
    attribute is set to True.
    :param fn:
    :return:
    """

    def decorator(obj, id, *args, **kwargs):
        tm = obj.transaction_manager
        if not tm.autocommit:
            if getattr(tm, 'transaction_uuid', None):
                tm.logger.info(f'{tm.transaction_uuid}: {fn.__name__} {id}')
            return fn(obj, id, *args, **kwargs)
        with tm:
            tm.logger.info(f'{tm.transaction_uuid}: {fn.__name__} {id}')
            return fn(obj, id, *args, **kwargs)

    return decorator


class DbMetadata(Persistent):
    """
    Object used by a CitrineConnection as a form of metadata on the contents of
    the database
    """

    def __init__(self, size=None, cache=None):
        super().__init__()
        self.size = size
        self.cache = cache


class DbContainer(Persistent):
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


class ClassCrystal(Persistent):
    """
    Persistent object that can deconstruct and store a class in a persistent
    manner, and then reconstruct the class after being retrieved
    """


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

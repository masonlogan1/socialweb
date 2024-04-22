"""
Classes and functions for managing collections of objects into a ZODB database.
"""
import logging
from math import ceil
from uuid import uuid4

from persistent import Persistent

# if the zope people would like to make sure the BTree class is directly
# importable rather than the current "cleverer than you" bs they have going on,
# that would be FANTASTIC.
from BTrees import _OOBTree
BTree = _OOBTree.BTree

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DEFAULT_MAX = 5000


class CollectionCapacityError(Exception):
    """
    Raised when an operation will exceed the capacity of a collection.
    """


class RestrictedItemError(Exception):
    """
    Raised when attempting to access or alter an item in a collection that
    is not meant to be accessed or altered.
    """


class CollectionMeta(Persistent):
    """
    Metadata object for managing a Collection. Keeps information on the size,
    object size limit, and groups the Collection belongs to.

    This object is ONLY intended to be used with ``citrine.storage.Collection``
    objects.
    """
    # I picked these numbers because anything under 60% of the default seems to
    # work perfectly well, but performance drops off after that point
    HEALTHY = 0
    ACCEPTABLE = 60
    ALERT = 70
    WARNING = 80
    CRITICAL = 90
    LEVELS = [HEALTHY, ACCEPTABLE, ALERT, WARNING, CRITICAL]
    # Things can become unstable over 5000 using the default ZODB DB cache size

    @property
    def size(self):
        """Number of items in the collection."""
        return len(self.obj.keys())

    @property
    def usage(self):
        """Percent of used space as a float value"""
        return self.size / self.max_size

    @property
    def status(self):
        """
        Helpful map for tracking the status of a collection. Can indicate if it
        may be time to either prune or create another collection that holds
        more objects.
        """
        return max(v for v in self.LEVELS if v <= ceil(self.usage * 100))

    def __init__(self, obj, uuid, max_size, strict, **kwargs):
        super().__init__(**kwargs)
        self.obj = obj
        self.uuid = uuid
        self.max_size = max_size
        self.strict = strict


class Collection(Persistent):
    """
    Modified version of a OOBTree that provides a metadata object and several
    properties derived from it for easily keeping track of the size and health
    of the collection. Also provides a "strict" mode that will put a hard limit
    on the number of items the collection can store to ensure stability.
    """

    # "why list these out when you can just use obj.meta.whatever?"
    # because I like things to be easier to reach.
    @property
    def uuid(self):
        return self.meta.uuid

    @property
    def size(self):
        # subtract one to account for stored metadata object
        return self.meta.size

    @property
    def usage(self):
        return self.meta.usage

    @property
    def status(self):
        return self.meta.status

    @property
    def max_size(self):
        return self.meta.max_size

    @property
    def strict(self):
        return self.meta.strict

    @strict.setter
    def strict(self, value: bool):
        self.meta.strict = value

    @property
    def meta(self):
        return self.___metadata___

    def __init__(self, uuid: str = None, max_size: int = None, strict=True,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = BTree()
        self.___metadata___ = CollectionMeta(
            self.tree,
            uuid=uuid if uuid else str(uuid4()),
            max_size=max_size if max_size else DEFAULT_MAX,
            strict=strict
        )

    def get(self, key, default=None):
        """
        Retrieve a value from the collection.
        :param key: the key associated with the desired item
        :param default: value to return if the key does not exist
        """
        return self.tree.get(key, default)

    def insert(self, key, value):
        """
        Insert a single key-value pair into the collection
        :param key: the identifier
        :param value: the value to store
        :raises CollectionCapacityError: if the size of the collection exceeds
        the limit in strict mode
        """
        if self.size >= self.max_size and self.strict:
            raise CollectionCapacityError(
                f'Cannot insert "{key}"; maximum size reached!'
            )
        return self.tree.insert(key, value)

    def update(self, collection):
        """
        Update a collection with a set of key-value pairs.
        :param collection: An iterable that provides key-value pairs
        :raises CollectionCapacityError: if the size of the new keys to be
        inserted will exceed the limit in strict mode
        """
        new_keys = [key for key in collection.keys() if key not in self.keys()]
        if self.size + len(new_keys) > self.max_size and self.strict:
            raise CollectionCapacityError(
                f'Cannot update collection; maximum size reached!'
            )
        return self.tree.update(collection)

    def pop(self, key, default=None):
        """
        Pop a key from the collection and return its value.
        :param key: identifier of the value
        :param default: alternate value to return if the key is not present
        :return:
        """
        if key not in self.keys() and default is None:
            raise KeyError(f'Key "{key}" not found in collection')
        return self.tree.pop(key, default)

    def popitem(self):
        """
        Pop a key from the collection and return the key-value pair
        :raise KeyError: if the key is not present in the collection
        """
        return self.tree.popitem()

    def setdefault(self, key, value):
        """
        If the key already exists then return the previous value stored there,
        else set the key to the value and return that
        :param key: id of item to write to
        :param value: the value to write, if applicable
        :return: existing value or provided value if no value currently exists
        """
        return self.tree.setdefault(key, value)

    def clear(self):
        """
        Clears all values in the collection
        """
        return self.tree.clear()

    def keys(self):
        """
        Return a view of all keys in the collection
        :return: OOBTreeItems object
        """
        return self.tree.keys()

    def iterkeys(self, min=None, max=None):
        """
        Return a view of all keys in the collection within a minimum/maximum
        range.
        :param min: the lowest key to return
        :param max: the highest key to return
        :return: generator of key
        """
        return (key for key, value in self.iteritems(min, max))

    def values(self):
        """
        Return a view of all values in the collection
        :return: OOBTreeItems object
        """
        return self.tree.values()

    def itervalues(self, min=None, max=None):
        """
        Return a view of all keys in the collection within a minimum/maximum
        range.
        :param min: the lowest value to return
        :param max: the highest value to return
        :return: generator of values
        """
        return self.tree.itervalues(min, max)

    def items(self):
        """
        Return a view of all items in the collection
        :return: OOBTreeItems object
        """
        return self.tree.items()

    def iteritems(self, min=None, max=None):
        """
        Return a view of all keys in the collection within a minimum/maximum
        range.
        :param min: the lowest key in the items
        :param max: the highest key in the items
        :return: generator of key-value pairs
        """
        return self.tree.iteritems(min, max)

    def byValue(self, min=None):
        """
        Returns anything where key >= min in (value, key) pairs
        :param min: minimum value to start from
        :return:
        """
        return self.tree.byValue(min)

    def maxKey(self, max=None):
        """
        Returns the highest-value key in the collection with an optional
        ceiling on the potential keys
        :param max: highest key value to return
        :raise ValueError: if there are no keys in the collection
        """
        return self.tree.maxKey(max)

    def minKey(self, min=None):
        """
        Returns the lowest-value key in the collection with an optional floor
        on the potential keys
        :param max: lowest key value to return
        :raise ValueError: if there are no keys in the collection
        """
        return self.tree.minKey(min)

    def has_key(self, key):
        """
        Returns True if a key exists in the collection, False otherwise
        :param key: the desired identifier
        :return: whether the key is present as a boolean
        """
        return self.tree.has_key(key)

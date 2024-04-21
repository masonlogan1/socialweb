import logging
from math import ceil
from uuid import uuid4

from persistent import Persistent

from citrine.storage.collection import Collection


def groupfn(fn):
    def decorator(obj, key, *args, **kwargs):
        index = int.from_bytes(key.encode()) % (len(obj.collections))
        collection = obj.collections[index]
        fn(obj, collection, key, *args, **kwargs)
    return decorator

class CollectionGroupMeta(Persistent):
    """
    Allows for tracking the internal status of CollectionGroup objects in a way
    that can be stored as an independent persistent object.
    """

    @property
    def size(self):
        return sum(collection.size for collection in self.collections)

    @property
    def max_size(self):
        return sum(collection.max_size for collection in self.collections)

    @property
    def max_collection_size(self):
        return max(collection.max_size for collection in self.collections)

    @property
    def usage(self):
        """Percent of used space"""
        return self.size / self.max_size

    @property
    def collection_usage(self):
        """Percent of used space by collection"""
        return {collection: collection.usage for collection in self.collections}

    @property
    def highest_collection_usage(self):
        return max(self.collection_usage.values())

    @property
    def lowest_collection_usage(self):
        return min(self.collection_usage.values())

    @property
    def status(self):
        """
        Provides the status of the collection group. Will use the highest status
        from the collections; if one collection is unstable it threatens the
        stability of the entire group.
        """
        return max(collection.status for collection in self.collections)

    def __init__(self, obj):
        self.obj = obj
        self.collections = tuple(self.obj.collections)


class CollectionGroup(Persistent):
    """
    A collection of multiple Collection objects.

    Intended to act as an immutable set. Collections created by/managed by a
    CollectionGroup should not be modified directly as their contents may not
    be reachable when attempting to use any of the standard operations.

    These objects should be saved to a database immediately if possible, keeping
    them in memory can cause a number of issues if they start to grow too large
    before the initial commit.
    """
    def __init__(self, collections, **kwargs):
        super().__init__(**kwargs)
        # repeating UUID values
        if len({col.uuid for col in collections}) != len(collections):
            raise KeyError("Collections must not have conflicting UUID values")
        self.collections = collections
        self.meta = CollectionGroupMeta(self)

    @groupfn
    def get(self, collection: Collection, key: str, value):
        return collection.get(key)

    @groupfn
    def insert(self, collection: Collection, key: str, value):
        return collection.insert(key, value=value)

    @groupfn
    def update(self, collection: Collection, incoming_collection):
        return collection.update(incoming_collection)
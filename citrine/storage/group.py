import logging
from itertools import chain
from math import ceil
from uuid import uuid4

from persistent import Persistent

from citrine.storage.collection import Collection, DEFAULT_MAX

minimum = min
maximum = max


def get_group_index(id: str, num_collections):
    return int.from_bytes(id.encode()) % num_collections


def groupfn(fn):
    # they key MUST be either a kwarg OR the first positional arg
    def decorator(obj, *args, **kwargs):
        key = kwargs.get('key', None if not args else args[0])
        index = get_group_index(key, len(obj.collections))
        collection = obj.collections[index]
        # fn gives us the function from Collection
        return fn(obj, *args, **kwargs)(collection, *args, **kwargs)
    return decorator


class GroupCapacityError(Exception):
    """
    Raised when an operation will exceed the capacity of a collection.
    """


class GroupView:
    fn = lambda *args, **kwargs: None

    def __init__(self, collections):
        self.collections = collections

    def __len__(self):
        count = 0
        for _ in self:
            count += 1
        return count

    def __iter__(self):
        for collection in self.collections:
            for item in self.fn(collection):
                yield item


class GroupKeys(GroupView):
    def fn(self, collection):
        return Collection.keys(collection)


class GroupValues(GroupView):
    def fn(self, collection):
        return Collection.values(collection)


class GroupItems(GroupView):
    def fn(self, collection):
        return Collection.items(collection)


class GroupMeta(Persistent):
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


class Group(Persistent):
    """
    A group of multiple Collection objects.

    Intended to act as an immutable set. Collections created by/managed by a
    CollectionGroup should not be modified directly as their contents may not
    be reachable when attempting to use any of the standard operations.

    These objects should be saved to a database immediately if possible, keeping
    them in memory can cause a number of issues if they start to grow too large
    before the initial commit.
    """

    @property
    def size(self):
        """
        The number of objects in this group
        """
        return self.meta.size

    @property
    def max_size(self):
        """
        The total number of objects this group can contain
        """
        return self.meta.max_size

    @property
    def max_collection_size(self):
        """
        Highest max_size among the component collections
        """
        return self.meta.max_collection_size

    @property
    def usage(self):
        """
        Usage percentage of all collections combined
        """
        return self.meta.usage

    @property
    def collection_usage(self):
        """
        Usage percentage of each collection in this group
        """
        return self.meta.collection_usage

    @property
    def highest_collection_usage(self):
        """
        Highest usage amount of the collection
        """
        return self.meta.highest_collection_usage

    @property
    def lowest_collection_usage(self):
        """
        Lowest usage amount of the collection
        """
        return self.meta.lowest_collection_usage

    @property
    def status(self):
        """
        Most urgent status among the group's collections
        """
        return self.meta.status

    @property
    def meta(self):
        """
        Metadata object for this group
        """
        return self.___metadata___

    @property
    def collections(self):
        """
        Collection objects for this group
        :return:
        """
        return self.___collections___

    @property
    def strict(self):
        return all(collection.strict for collection in self.collections)

    @strict.setter
    def strict(self, value):
        if not isinstance(value, bool):
            raise TypeError("'strict' must be a boolean")
        for collection in self.collections:
            collection.strict = value

    def __init__(self, collections, strict=False, **kwargs):
        super().__init__(**kwargs)
        # repeating UUID values
        if len({col.uuid for col in collections}) != len(collections):
            raise KeyError("Collections must not have conflicting UUID values")
        self.___collections___ = collections
        self.___metadata___ = GroupMeta(self)
        self.strict = strict

    @staticmethod
    def new(size: int = None, max_collection_size: int = DEFAULT_MAX,
            strict=False, custom: dict = None):
        """
        Creates a new, empty Group.

        If ``custom`` is not used, a number of identically-sized collections
        will be created

        If ``custom`` is used, collections will be created to meet the sizes
        specified. The parameter should be an iterable of key-value pairs
        matching pairs of integer numbers. The first number is the hash for the
        collection, the second number is the size of the collection

        If the keys in a custom collection do not make a continuous set of
        whole numbers starting at zero, collections will be created to fill the
        gaps using ``max_collection_size`` as the size for each one

        If ``custom`` is provided and a ``size`` is provided that exceeds the
        highest key value, additional collections will be added to meet the
        size requirement

        If a size is specified that is lower than the highest custom key value,
        a ``KeyError`` will be raised

        To put it simply, ``custom`` allows you to define specific container
        sizes by the hash value of the items that will be stored there, and any
        gaps will be automatically filled

        :param size: the total number of containers that should be created
        :param max_collection_size: the maximum number of objects each container can handle
        :param strict: whether to raise exceptions if the max_collection_size is exceeded (default False)
        :param custom: a mapping of custom collection sizes to the key hash values
        :return: Group
        """
        # generate everything if custom definition is not provided
        if not custom:
            if not size:
                raise ValueError("Size must be provided if no custom " +
                                 "definition is")
            collections = tuple(Collection(max_size=max_collection_size)
                                for _ in range(size))
            return Group(collections=collections)
        # ensure any gaps are filled if custom definition is provided
        keys = tuple(custom.keys())
        if any(not isinstance(key, int) for key in keys):
            raise KeyError("Custom collection keys must be integers")
        if not size:
            size = max(custom.keys())
        if size and size < max(custom.keys()):
            raise KeyError("Size must be greater than highest key")
        # fill gaps with default generation
        for key in range(size):
            if key not in keys:
                custom[key] = max_collection_size
        collections = tuple(Collection(max_size=max_collection_size,
                                       strict=strict)
                            for _, max_collection_size in custom.items())
        return Group(collections=collections)

    @groupfn
    def get(self, key, default=None):
        """
        Retrieve a value from the collection.
        :param key: the key associated with the desired item
        :param default: value to return if the key does not exist
        """
        return Collection.get

    @groupfn
    def insert(self, key, value):
        """
        Insert a single key-value pair into the collection
        :param key: the identifier
        :param value: the value to store
        :raises GroupCapacityError: if the size of the collection exceeds
        the limit in strict mode
        """
        if (self.size >= self.max_size
                and key not in self.keys()
                and self.strict):
            raise GroupCapacityError("Maximum size reached! Cannot insert")
        return Collection.insert

    def update(self, collection):
        """
        Update a collection with a set of key-value pairs.
        :param collection: An iterable that provides key-value pairs
        :raises CollectionCapacityError: if the size of the new keys to be
        inserted will exceed the limit in strict mode
        """
        new_keys = (key for key in collection.keys() if key not in self.keys())
        if len(tuple(new_keys)) + self.size > self.max_size and self.strict:
            raise GroupCapacityError("Maximum size reached! Cannot perform update")

        num_collections = len(self.collections)
        split_collection = {_: {} for _ in range(len(self.collections))}
        for key, value in collection.items():
            split_collection[get_group_index(key, num_collections)][key] = value

        for index, collection in split_collection.items():
            self.collections[index].update(collection)

    @groupfn
    def pop(self, key, default=None):
        """
        Pop a key from the collection and return its value.
        :param key: identifier of the value
        :param default: alternate value to return if the key is not present
        :return:
        """
        return Collection.pop

    def popitem(self):
        """
        Pop a key from the collection and return the key-value pair
        :raise KeyError: if the key is not present in the collection
        """
        return self.minKey(), self.pop(self.minKey())

    @groupfn
    def setdefault(self, key, value):
        """
        If the key already exists then return the previous value stored there,
        else set the key to the value and return that
        :param key: id of item to write to
        :param value: the value to write, if applicable
        :return: existing value or provided value if no value currently exists
        """
        return Collection.setdefault

    def clear(self):
        """
        Clears all values in the collection
        """
        return [collection.clear() for collection in self.collections]

    def keys(self):
        """
        Return a view of all keys in the collection
        :return: OOBTreeItems object
        """
        return GroupKeys(self.collections)

    def iterkeys(self, min=None, max=None):
        """
        Return a view of all keys in the collection within a minimum/maximum
        range.
        :param min: the lowest key to return
        :param max: the highest key to return
        :return: generator of key
        """
        gens = [collection.iterkeys(min, max)
                for collection in self.collections]
        vals = list()
        for gen in gens:
            try:
                vals.append(next(gen))
            except StopIteration:
                vals.append(None)
        while any(vals):
            # get the lowest value
            next_val = minimum((v for v in vals if v is not None))
            # replace the lowest value with the next value from the generator
            try:
                vals[vals.index(next_val)] = next(gens[vals.index(next_val)])
            except StopIteration:
                vals[vals.index(next_val)] = None
            yield next_val

    def values(self):
        """
        Return a view of all values in the collection
        :return: OOBTreeItems object
        """
        return GroupValues(self.collections)

    def itervalues(self, min=None, max=None):
        """
        Return a view of all keys in the collection within a minimum/maximum
        range.
        :param min: the lowest value to return
        :param max: the highest value to return
        :return: generator of values
        """
        gens = [collection.itervalues(min, max)
                for collection in self.collections]
        vals = list()
        for gen in gens:
            try:
                vals.append(next(gen))
            except StopIteration:
                vals.append(None)
        while any(vals):
            # get the lowest value
            next_val = minimum((v for v in vals if v is not None))
            # replace the lowest value with the next value from the generator
            try:
                vals[vals.index(next_val)] = next(gens[vals.index(next_val)])
            except StopIteration:
                vals[vals.index(next_val)] = None
            yield next_val

    def items(self):
        """
        Return a view of all items in the collection
        :return: OOBTreeItems object
        """
        return GroupItems(self.collections)

    def iteritems(self, min=None, max=None):
        """
        Return a view of all keys in the collection within a minimum/maximum
        range.
        :param min: the lowest key in the items
        :param max: the highest key in the items
        :return: generator of key-value pairs
        """
        gens = [collection.iteritems(min, max)
                for collection in self.collections]
        keys = list()
        items = dict()
        for gen in gens:
            try:
                item = next(gen)
                keys.append(item[0])
                items[item[0]] = item[1]
            except StopIteration:
                keys.append(None)
        while any(keys):
            # get the lowest value
            next_key = minimum((v for v in keys if v is not None))
            # replace the lowest value with the next value from the generator
            try:
                item = next(gens[keys.index(next_key)])
                keys[keys.index(next_key)] = item[0]
                items[item[0]] = item[1]
                yield next_key, items.pop(next_key)
            except StopIteration:
                keys[keys.index(next_key)] = None
                yield next_key, items.pop(next_key)

    def byValue(self, min=None):
        """
        Returns anything where key >= min in (value, key) pairs
        :param min: minimum value to start from
        :return:
        """
        values = [collection.byValue(min) for collection in self.collections]
        combined = list()
        for group in values:
            combined += list(group)
        for val in sorted(combined, reverse=True):
            yield val

    def maxKey(self, max=None):
        """
        Returns the highest-value key in the collection with an optional
        ceiling on the potential keys
        :param max: highest key value to return
        :raise ValueError: if there are no keys in the collection
        """
        return maximum(collection.maxKey(max)
                       for collection in self.collections)

    def minKey(self, min=None):
        """
        Returns the lowest-value key in the collection with an optional floor
        on the potential keys
        :param max: lowest key value to return
        :raise ValueError: if there are no keys in the collection
        """
        return minimum(collection.minKey(min)
                       for collection in self.collections)

    @groupfn
    def has_key(self, key):
        """
        Returns True if a key exists in the collection, False otherwise
        :param key: the desired identifier
        :return: whether the key is present as a boolean
        """
        return Collection.has_key

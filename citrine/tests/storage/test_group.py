from unittest import TestCase, main
from unittest.mock import MagicMock

from ZODB import DB

from citrine.storage import group
from citrine.storage.collection import Collection, CollectionMeta


class DummyGroup:
    """
    Dummy object that provides a group of fake collections for testing purposes
    """
    def __init__(self, collections=tuple()):
        self.collections = collections


class GroupMetaTests(TestCase):
    """
    Test cases for citrine.storage.group.GroupMeta that ensure a GroupMeta
    object combines the metadata information from the group's component parts
    """

    def test_size(self):
        """
        Test that a GroupMeta object combines the size of all component
        collections
        """
        collection0 = Collection(max_size=10)
        collection1 = Collection(max_size=10)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
            collection1.insert(f'key1.{i}', f'value1.{i}')
        dummy = MagicMock(collections=(collection0, collection1))

        expected_size = 20
        meta = group.GroupMeta(dummy)
        self.assertEqual(meta.size, expected_size)

    def test_max_size(self):
        """
        Tests that a GroupMeta object combines the max_size of all components
        """
        collection0 = Collection(max_size=10)
        collection1 = Collection(max_size=15)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
            collection1.insert(f'key1.{i}', f'value1.{i}')
        dummy = MagicMock(collections=(collection0, collection1))

        expected = 25
        meta = group.GroupMeta(dummy)
        self.assertEqual(meta.max_size, expected)

    def test_max_collection_size(self):
        """
        Tests that a GroupMeta object returns the highest max_size for all
        collections in the group
        """
        collection0 = Collection(max_size=10)
        collection1 = Collection(max_size=15)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
            collection1.insert(f'key1.{i}', f'value1.{i}')
        dummy = MagicMock(collections=(collection0, collection1))

        expected = 15
        meta = group.GroupMeta(dummy)
        self.assertEqual(meta.max_collection_size, expected)

    def test_usage(self):
        """
        Tests that a GroupMeta object returns the usage of all components as
        a float value
        """
        collection0 = Collection(max_size=20)
        collection1 = Collection(max_size=20)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
            collection1.insert(f'key1.{i}', f'value1.{i}')
        dummy = MagicMock(collections=(collection0, collection1))

        meta = group.GroupMeta(dummy)

        usage = int(meta.usage*100)
        self.assertEqual(usage, 50)

    def test_collection_usage(self):
        """
        Tests that a GroupMeta object returns a dictionary of all collections
        along with their usage percentages
        :return:
        """
        collection0 = Collection(max_size=20)
        collection1 = Collection(max_size=20)
        collections = (collection0, collection1)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
            collection1.insert(f'key1.{i}', f'value1.{i}')
        dummy = MagicMock(collections=collections)

        meta = group.GroupMeta(dummy)

        expected = 50
        usage = meta.collection_usage
        for index, item in enumerate(usage.items()):
            self.assertEqual(item[0], collections[index])
            self.assertEqual(int(item[1]*100), expected)

    def test_highest_collection_usage(self):
        """:return:
        Tests that a GroupMeta object can return the highest usage value from
        all component collections
        """
        collection0 = Collection(max_size=20)
        collection1 = Collection(max_size=20)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
        for i in range(15):
            collection1.insert(f'key1.{i}', f'value1.{i}')
        dummy = MagicMock(collections=(collection0, collection1))

        expected = 75
        meta = group.GroupMeta(dummy)
        highest = int(meta.highest_collection_usage * 100)
        self.assertEqual(highest, expected)

    def test_lowest_collection_usage(self):
        """
        Tests that a GroupMeta object can return the lowest usage value from
        all component collections
        """
        collection0 = Collection(max_size=20)
        collection1 = Collection(max_size=20)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
        for i in range(15):
            collection1.insert(f'key1.{i}', f'value1.{i}')
        dummy = MagicMock(collections=(collection0, collection1))

        expected = 50
        meta = group.GroupMeta(dummy)
        lowest = int(meta.lowest_collection_usage * 100)
        self.assertEqual(lowest, expected)

    def test_status(self):
        """
        Tests that a GroupMeta object returns the most severe status from all
        component collections as a member of the Enumerated type
        """
        collection0 = Collection(max_size=20)
        collection1 = Collection(max_size=20)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
        for i in range(10):
            collection1.insert(f'key1.{i}', f'value1.{i}')
        dummy = MagicMock(collections=(collection0, collection1))

        meta = group.GroupMeta(dummy)

        # start with both collections <50%
        status = meta.status
        self.assertEqual(status, CollectionMeta.HEALTHY)

        # increase collection0 to ~65%
        for i in range(10, 13):
            collection0.insert(f'key0.{i}', f'value0.{i}')
        status = meta.status
        self.assertEqual(status, CollectionMeta.ACCEPTABLE)

        # increase collection1 to ~75%
        for i in range(10, 15):
            collection1.insert(f'key0.{i}', f'value0.{i}')
        status = meta.status
        self.assertEqual(status, CollectionMeta.ALERT)

        # increase collection0 to ~85%
        for i in range(12, 17):
            collection0.insert(f'key0.{i}', f'value0.{i}')
        status = meta.status
        self.assertEqual(status, CollectionMeta.WARNING)

        # increase collection1 to >90%
        for i in range(15, 19):
            collection1.insert(f'key0.{i}', f'value0.{i}')
        status = meta.status
        self.assertEqual(status, CollectionMeta.CRITICAL)


class GroupConstructionTests(TestCase):
    """
    Test cases for citrine.storage.group.Group that check the group is properly
    constructing itself according to the specified size with the correct
    sizing and strictness
    """


class GroupPropertyTests(TestCase):
    """
    Test cases for citrine.storage.group.Group that checks the properties of
    the Group object properly pass through metadata information
    """

    # THESE ARE A DUPLICATE OF THE TESTS IN META, HOWEVER WE NEED TO MAKE SURE
    # THAT THE GROUP RETAINS THE FUNCTIONALITY!
    def test_size(self):
        """
        Test that a GroupMeta object combines the size of all component
        collections
        """
        collection0 = Collection(max_size=10)
        collection1 = Collection(max_size=10)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
            collection1.insert(f'key1.{i}', f'value1.{i}')
        grp = group.Group(collections=(collection0, collection1))

        # test size with manually created collections
        expected_size = 20
        self.assertEqual(grp.size, expected_size)

        # test size with automatically generated collections
        grp = group.Group.new(size=2, max_collection_size=20)
        for i in range(30):
            grp.insert(f'key0.{i}', f'value0.{i}')
        expected_size = 30
        self.assertEqual(grp.size, expected_size)

    def test_max_size(self):
        """
        Tests that a GroupMeta object combines the max_size of all components
        """
        collection0 = Collection(max_size=10)
        collection1 = Collection(max_size=15)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
            collection1.insert(f'key1.{i}', f'value1.{i}')
        grp = group.Group(collections=(collection0, collection1))

        # test max_size with manually generated collections
        expected = 25
        self.assertEqual(grp.max_size, expected)

        # test max_size with automatically generated collections
        grp = group.Group.new(size=2, max_collection_size=20)
        for i in range(30):
            grp.insert(f'key0.{i}', f'value0.{i}')
        expected_size = 40
        self.assertEqual(grp.max_size, expected_size)

    def test_max_collection_size(self):
        """
        Tests that a GroupMeta object returns the highest max_size for all
        collections in the group
        """
        collection0 = Collection(max_size=10)
        collection1 = Collection(max_size=15)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
            collection1.insert(f'key1.{i}', f'value1.{i}')
        grp = group.Group(collections=(collection0, collection1))

        # test with manually created collections
        expected = 15
        self.assertEqual(grp.max_collection_size, expected)

        # test with automatically generated collections
        grp = group.Group.new(custom={0: 10, 1: 15})
        expected = 15
        self.assertEqual(grp.max_collection_size, expected)

    def test_usage(self):
        """
        Tests that a GroupMeta object returns the usage of all components as
        a float value
        """
        collection0 = Collection(max_size=20)
        collection1 = Collection(max_size=20)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
            collection1.insert(f'key1.{i}', f'value1.{i}')
        grp = group.Group(collections=(collection0, collection1))

        # test with manually created collections
        expected = 50
        usage = int(grp.usage*100)
        self.assertEqual(usage, expected)

        # test with generated collections
        grp = group.Group.new(size=2, max_collection_size=20)
        for i in range(30):
            grp.insert(f'key0.{i}', f'value0.{i}')
        expected = 75
        self.assertEqual(int(grp.usage*100), expected)

    def test_collection_usage(self):
        """
        Tests that a GroupMeta object returns a dictionary of all collections
        along with their usage percentages
        :return:
        """
        collection0 = Collection(max_size=20)
        collection1 = Collection(max_size=20)
        collections = (collection0, collection1)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
            collection1.insert(f'key1.{i}', f'value1.{i}')
        grp = group.Group(collections=(collection0, collection1))

        # test with manual collections
        expected = 50
        usage = grp.collection_usage
        for index, item in enumerate(usage.items()):
            self.assertEqual(item[0], collections[index])
            self.assertEqual(int(item[1]*100), expected)

        # test with generated collections
        grp = group.Group.new(size=2, max_collection_size=20)
        for i in range(20):
            grp.insert(f'key0.{i}', f'value0.{i}')
        expected = 50
        usage = grp.collection_usage
        for index, item in enumerate(usage.items()):
            self.assertEqual(item[0], grp.collections[index])
            self.assertEqual(int(item[1] * 100), expected)

    def test_highest_collection_usage(self):
        """
        Tests that a GroupMeta object can return the highest usage value from
        all component collections
        """
        collection0 = Collection(max_size=20)
        collection1 = Collection(max_size=20)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
        for i in range(15):
            collection1.insert(f'key1.{i}', f'value1.{i}')
        grp = group.Group(collections=(collection0, collection1))

        # test with manual collections
        expected = 75
        highest = int(grp.highest_collection_usage * 100)
        self.assertEqual(highest, expected)

        # test with generated collections
        grp = group.Group.new(size=2, max_collection_size=20)
        for i in range(10):
            grp.insert(f'key.{i}', f'value{i}')
        for i in range(10, 20, 2):
            grp.insert(f'key.{i}', f'value{i}')
        expected = 50
        self.assertEqual(int(grp.highest_collection_usage*100), expected)

    def test_lowest_collection_usage(self):
        """
        Tests that a GroupMeta object can return the lowest usage value from
        all component collections
        """
        collection0 = Collection(max_size=20)
        collection1 = Collection(max_size=20)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
        for i in range(15):
            collection1.insert(f'key1.{i}', f'value1.{i}')
        grp = group.Group(collections=(collection0, collection1))

        # test with manual collections
        expected = 50
        lowest = int(grp.lowest_collection_usage * 100)
        self.assertEqual(lowest, expected)

        # test with generated collections
        # test with generated collections
        grp = group.Group.new(size=2, max_collection_size=20)
        for i in range(10):
            grp.insert(f'key.{i}', f'value{i}')
        for i in range(10, 20, 2):
            grp.insert(f'key.{i}', f'value{i}')
        expected = 25
        self.assertEqual(int(grp.lowest_collection_usage*100), expected)

    def test_status(self):
        """
        Tests that a GroupMeta object returns the most severe status from all
        component collections as a member of the Enumerated type
        """
        collection0 = Collection(max_size=20)
        collection1 = Collection(max_size=20)
        for i in range(10):
            collection0.insert(f'key0.{i}', f'value0.{i}')
        for i in range(10):
            collection1.insert(f'key1.{i}', f'value1.{i}')
        grp = group.Group(collections=(collection0, collection1))

        # start with both collections <50%
        status = grp.status
        self.assertEqual(status, CollectionMeta.HEALTHY)

        # increase collection0 to ~65%
        for i in range(10, 13):
            collection0.insert(f'key0.{i}', f'value0.{i}')
        status = grp.status
        self.assertEqual(status, CollectionMeta.ACCEPTABLE)

        # increase collection1 to ~75%
        for i in range(10, 15):
            collection1.insert(f'key0.{i}', f'value0.{i}')
        status = grp.status
        self.assertEqual(status, CollectionMeta.ALERT)

        # increase collection0 to ~85%
        for i in range(12, 17):
            collection0.insert(f'key0.{i}', f'value0.{i}')
        status = grp.status
        self.assertEqual(status, CollectionMeta.WARNING)

        # increase collection1 to >90%
        for i in range(15, 19):
            collection1.insert(f'key0.{i}', f'value0.{i}')
        status = grp.status
        self.assertEqual(status, CollectionMeta.CRITICAL)


class GroupStorageTests(TestCase):
    """
    Test cases for citrine.storage.group.Group that ensure the standard
    Collection interface is distributed across multiple collections without
    manual intervention

    Does not test the internal handling, only that the interface works exactly
    as expected
    """

    # This is a modified duplicate of the CollectionStorageTests

    def test_iterkeys(self):
        """
        Tests that the Collection.iterkeys method will iterate over all keys,
        iterate over keys when a range is specified, and will ALWAYS ignore
        the "meta" key
        :return:
        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(grp.iterkeys()), [])

        keys0 = ['key0.0', 'key0.1', 'key0.2', 'key0.3', 'key0.4']
        keys1 = ['key1.0', 'key1.1', 'key1.2', 'key1.3', 'key1.4']
        keys2 = ['key2.0', 'key2.1', 'key2.2', 'key2.3', 'key2.4']
        key_set = (keys0, keys1, keys2)
        keys = keys0 + keys1 + keys2
        values0 = ['value0.0', 'value0.1', 'value0.2', 'value0.3', 'value0.4']
        values1 = ['value1.0', 'value1.1', 'value1.2', 'value1.3', 'value1.4']
        values2 = ['value2.0', 'value2.1', 'value2.2', 'value2.3', 'value2.4']
        value_set = (values0, values1, values2)
        values = values0 + values1 + values2
        # we're inserting the keys directly into the COLLECTIONS rather than
        # through the group's insert to avoid assuming that the group insert
        # already works
        for index, collection in enumerate(collections):
            for key, value in zip(key_set[index], value_set[index]):
                collection.insert(key, value)

        # check for all keys
        expected = keys
        out = list(grp.iterkeys())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for keys 1, 2, and 3
        expected = keys[1:8]
        out = list(grp.iterkeys(min=keys[1], max=keys[7]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for keys 0, 1, and 2
        expected = keys[:6]
        out = list(grp.iterkeys(max=keys[5]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for keys 2, 3, and 4
        expected = keys[7:]
        out = list(grp.iterkeys(min=keys[7]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_itervalues(self):
        """
        Tests that the Collection.itervalues method will iterate over all
        values, iterate over values when a range is specified, and will ALWAYS
        ignore the "meta" value
        :return:
        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(grp.itervalues()), [])

        keys0 = ['key0.0', 'key0.1', 'key0.2', 'key0.3', 'key0.4']
        keys1 = ['key1.0', 'key1.1', 'key1.2', 'key1.3', 'key1.4']
        keys2 = ['key2.0', 'key2.1', 'key2.2', 'key2.3', 'key2.4']
        key_set = (keys0, keys1, keys2)
        keys = keys0 + keys1 + keys2
        values0 = ['value0.0', 'value0.1', 'value0.2', 'value0.3', 'value0.4']
        values1 = ['value1.0', 'value1.1', 'value1.2', 'value1.3', 'value1.4']
        values2 = ['value2.0', 'value2.1', 'value2.2', 'value2.3', 'value2.4']
        value_set = (values0, values1, values2)
        values = values0 + values1 + values2
        for index, collection in enumerate(collections):
            for key, value in zip(key_set[index], value_set [index]):
                collection.insert(key, value)

        # check for all values
        expected = values
        out = list(grp.itervalues())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 1, 2, and 3
        expected = values[1:8]
        out = list(grp.itervalues(min=keys[1], max=keys[7]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 0, 1, and 2
        expected = values[:7]
        out = list(grp.itervalues(max=keys[6]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 2, 3, and 4
        expected = values[7:]
        out = list(grp.itervalues(min=keys[7]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_iteritems(self):
        """
        Tests that the Collection.itervalues method will iterate over all
        values, iterate over values when a range is specified, and will ALWAYS
        ignore the "meta" value
        :return:
        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(grp.iterkeys()), [])

        keys0 = ['key0.0', 'key0.1', 'key0.2', 'key0.3', 'key0.4']
        keys1 = ['key1.0', 'key1.1', 'key1.2', 'key1.3', 'key1.4']
        keys2 = ['key2.0', 'key2.1', 'key2.2', 'key2.3', 'key2.4']
        key_set = (keys0, keys1, keys2)
        keys = keys0 + keys1 + keys2
        values0 = ['value0.0', 'value0.1', 'value0.2', 'value0.3', 'value0.4']
        values1 = ['value1.0', 'value1.1', 'value1.2', 'value1.3', 'value1.4']
        values2 = ['value2.0', 'value2.1', 'value2.2', 'value2.3', 'value2.4']
        value_set = (values0, values1, values2)
        values = values0 + values1 + values2
        items0 = {k: v for k, v in zip(keys0, values0)}
        items1 = {k: v for k, v in zip(keys1, values1)}
        items2 = {k: v for k, v in zip(keys2, values2)}
        item_set = (items0, items1, items2)
        items = {**items0, **items1, **items2}
        for index, collection in enumerate(collections):
            for key, value in zip(key_set[index], value_set[index]):
                collection.insert(key, value)

        # check for all fifteen values
        expected = {k: v for k, v in items.items()}
        out = dict(grp.iteritems())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 1, 2, and 3
        expected = {k: v for k, v in items.items() if k in keys[1:4]}
        out = dict(grp.iteritems(min=keys[1], max=keys[3]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 0, 1, and 2
        expected = {k: v for k, v in items.items() if k in keys[:3]}
        out = dict(grp.iteritems(max=keys[2]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

        # check for values 2, 3, and 4
        expected = {k: v for k, v in items.items() if k in keys[2:]}
        out = dict(grp.iteritems(min=keys[2]))
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_keys(self):
        """
        Tests that the Collection.iterkeys method will iterate over all keys,
        iterate over keys when a range is specified, and will ALWAYS ignore
        the "meta" key
        :return:
        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(grp.iterkeys()), [])

        keys0 = ['key0.0', 'key0.1', 'key0.2', 'key0.3', 'key0.4']
        keys1 = ['key1.0', 'key1.1', 'key1.2', 'key1.3', 'key1.4']
        keys2 = ['key2.0', 'key2.1', 'key2.2', 'key2.3', 'key2.4']
        key_set = (keys0, keys1, keys2)
        keys = keys0 + keys1 + keys2
        values0 = ['value0.0', 'value0.1', 'value0.2', 'value0.3', 'value0.4']
        values1 = ['value1.0', 'value1.1', 'value1.2', 'value1.3', 'value1.4']
        values2 = ['value2.0', 'value2.1', 'value2.2', 'value2.3', 'value2.4']
        value_set = (values0, values1, values2)
        values = values0 + values1 + values2
        items0 = {k: v for k, v in zip(keys0, values0)}
        items1 = {k: v for k, v in zip(keys1, values1)}
        items2 = {k: v for k, v in zip(keys2, values2)}
        item_set = (items0, items1, items2)
        items = {**items0, **items1, **items2}
        for index, collection in enumerate(collections):
            for key, value in zip(key_set[index], value_set[index]):
                collection.insert(key, value)

        # check for all keys
        expected = keys
        out = list(grp.keys())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_values(self):
        """
        Tests that the Collection.itervalues method will iterate over all
        values, iterate over values when a range is specified, and will ALWAYS
        ignore the "meta" value
        :return:
        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(grp.iterkeys()), [])

        keys0 = ['key0.0', 'key0.1', 'key0.2', 'key0.3', 'key0.4']
        keys1 = ['key1.0', 'key1.1', 'key1.2', 'key1.3', 'key1.4']
        keys2 = ['key2.0', 'key2.1', 'key2.2', 'key2.3', 'key2.4']
        key_set = (keys0, keys1, keys2)
        keys = keys0 + keys1 + keys2
        values0 = ['value0.0', 'value0.1', 'value0.2', 'value0.3', 'value0.4']
        values1 = ['value1.0', 'value1.1', 'value1.2', 'value1.3', 'value1.4']
        values2 = ['value2.0', 'value2.1', 'value2.2', 'value2.3', 'value2.4']
        value_set = (values0, values1, values2)
        values = values0 + values1 + values2
        items0 = {k: v for k, v in zip(keys0, values0)}
        items1 = {k: v for k, v in zip(keys1, values1)}
        items2 = {k: v for k, v in zip(keys2, values2)}
        item_set = (items0, items1, items2)
        items = {**items0, **items1, **items2}
        for index, collection in enumerate(collections):
            for key, value in zip(key_set[index], value_set[index]):
                collection.insert(key, value)

        # check for all values
        expected = values
        out = list(grp.values())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_items(self):
        """
        Tests that the Collection.itervalues method will iterate over all
        values, iterate over values when a range is specified, and will ALWAYS
        ignore the "meta" value
        :return:
        """
        collections = (Collection(max_size=5), Collection(max_size=5),
                       Collection(max_size=5))
        grp = group.Group(collections=collections)

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(grp.iterkeys()), [])

        keys0 = ['key0.0', 'key0.1', 'key0.2', 'key0.3', 'key0.4']
        keys1 = ['key1.0', 'key1.1', 'key1.2', 'key1.3', 'key1.4']
        keys2 = ['key2.0', 'key2.1', 'key2.2', 'key2.3', 'key2.4']
        key_set = (keys0, keys1, keys2)
        keys = keys0 + keys1 + keys2
        values0 = ['value0.0', 'value0.1', 'value0.2', 'value0.3', 'value0.4']
        values1 = ['value1.0', 'value1.1', 'value1.2', 'value1.3', 'value1.4']
        values2 = ['value2.0', 'value2.1', 'value2.2', 'value2.3', 'value2.4']
        value_set = (values0, values1, values2)
        values = values0 + values1 + values2
        items0 = {k: v for k, v in zip(keys0, values0)}
        items1 = {k: v for k, v in zip(keys1, values1)}
        items2 = {k: v for k, v in zip(keys2, values2)}
        item_set = (items0, items1, items2)
        items = {**items0, **items1, **items2}
        for index, collection in enumerate(collections):
            for key, value in zip(key_set[index], value_set[index]):
                collection.insert(key, value)

        # check for all five values
        expected = {k: v for k, v in items.items()}
        out = dict(grp.items())
        self.assertEqual(expected, out, msg=f'{out} != {expected}')

    def test_insert(self):
        """
        Test that the implementation of ``insert`` in the Collection class works
        as intended.

        Tests that we can insert values, that we cannot exceed capacity in
        strict mode, that we can exceed capacity with strict mode off, and that
        attempting to insert a value for meta will raise an exception
        """
        collections = (Collection(max_size=3), Collection(max_size=3),
                       Collection(max_size=3))
        grp = group.Group(collections=collections, strict=True)

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(grp.iterkeys()), [])

        keys0 = ['key0.0', 'key0.1', 'key0.2']
        keys1 = ['key1.0', 'key1.1', 'key1.2']
        keys2 = ['key2.0', 'key2.1', 'key2.2']
        key_set = (keys0, keys1, keys2)
        keys = keys0 + keys1 + keys2
        values0 = ['value0.0', 'value0.1', 'value0.2']
        values1 = ['value1.0', 'value1.1', 'value1.2']
        values2 = ['value2.0', 'value2.1', 'value2.2']
        value_set = (values0, values1, values2)
        values = values0 + values1 + values2
        items0 = {k: v for k, v in zip(keys0, values0)}
        items1 = {k: v for k, v in zip(keys1, values1)}
        items2 = {k: v for k, v in zip(keys2, values2)}
        item_set = (items0, items1, items2)
        items = {**items0, **items1, **items2}
        for key, value in items.items():
            grp.insert(key, value)

        collection_items = dict()
        for collection in grp.collections:
            for key, value in collection.items():
                collection_items[key] = value

        # test that everything we have inserted made its way into the collection
        self.assertEqual(collection_items, items, msg=f'{collection_items} != {items}')

        # test that when strict==True, we cannot exceed the capacity
        with self.assertRaises(group.GroupCapacityError):
            grp.insert('key5', 'val5')

        # test that when strict==False, we can exceed the capacity
        grp.strict = False
        grp.insert('key3.0', 'val3.0')
        self.assertEqual(grp.collections[0].get('key3.0'), 'val3.0')

    def test_update(self):
        """
        Tests that the implementation of ``update`` in the Collection class
        works as intended.

        Tests that we can a dict of values, that we cannot exceed capacity in
        strict mode, that we can exceed capacity with strict mode off, that
        attempting to insert a value for meta will raise an exception, and that
        if an update fails the size or type checks nothing will be added
        """
        collections = (Collection(max_size=3), Collection(max_size=3),
                       Collection(max_size=3))
        grp = group.Group(collections=collections, strict=True)

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(grp.iterkeys()), [])

        keys0 = ['key0.0', 'key0.1', 'key0.2']
        keys1 = ['key1.0', 'key1.1', 'key1.2']
        keys2 = ['key2.0', 'key2.1', 'key2.2']
        key_set = (keys0, keys1, keys2)
        keys = keys0 + keys1 + keys2
        values0 = ['value0.0', 'value0.1', 'value0.2']
        values1 = ['value1.0', 'value1.1', 'value1.2']
        values2 = ['value2.0', 'value2.1', 'value2.2']
        value_set = (values0, values1, values2)
        values = values0 + values1 + values2
        items0 = {k: v for k, v in zip(keys0, values0)}
        items1 = {k: v for k, v in zip(keys1, values1)}
        items2 = {k: v for k, v in zip(keys2, values2)}
        item_set = (items0, items1, items2)
        items = {**items0, **items1, **items2}

        # test that everything made its way into the group
        grp.update(items)
        collection_items = dict()
        for collection in grp.collections:
            for key, value in collection.items():
                collection_items[key] = value
        self.assertEqual(collection_items, items,
                         msg=f'{collection_items} != {items}')

        # test that when strict==True, we cannot exceed the capacity
        too_many = {f'key{i}': f'val{i}' for i in range(5, 20)}
        with self.assertRaises(group.GroupCapacityError):
            grp.update(too_many)

        # check that a failed update does not insert ANY of the keys, even if
        # there is enough room for some of them
        for key in too_many.keys():
            self.assertNotIn(key, grp.keys())

        # test that when strict==False, we can exceed the capacity
        grp.strict = False
        too_many = {f'key{i}': f'val{i}' for i in range(5, 20)}
        grp.update(too_many)
        for key, value in too_many.items():
            self.assertIn(key, grp.keys())

    def test_get(self):
        """
        Tests that the implementation of ``get`` in the Collection class
        works as intended.

        Tests that we can get a value back by its key, that attempting to
        directly access the meta object will raise an exception, and that we
        can set a default value for when a key does not exist.
        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(grp.iterkeys()), [])

        keys0 = ['key0.0', 'key0.1', 'key0.2']
        keys1 = ['key1.0', 'key1.1', 'key1.2']
        keys2 = ['key2.0', 'key2.1', 'key2.2']
        key_set = (keys0, keys1, keys2)
        keys = keys0 + keys1 + keys2
        values0 = ['value0.0', 'value0.1', 'value0.2']
        values1 = ['value1.0', 'value1.1', 'value1.2']
        values2 = ['value2.0', 'value2.1', 'value2.2']
        value_set = (values0, values1, values2)
        values = values0 + values1 + values2
        items0 = {k: v for k, v in zip(keys0, values0)}
        items1 = {k: v for k, v in zip(keys1, values1)}
        items2 = {k: v for k, v in zip(keys2, values2)}
        item_set = (items0, items1, items2)
        items = {**items0, **items1, **items2}
        for key, value in items.items():
            grp.insert(key, value)

        # test that every item can be accessed via get
        for key, value in items.items():
            self.assertEqual(grp.get(key), value)

        # test that the default value will be returned if a key does not exist
        self.assertEqual(grp.get('keyNull', 'valNull'), 'valNull')

        # test that the default is ignored if the key DOES exist
        self.assertEqual(grp.get(keys[0], 'valNull'), values[0])

    def test_maxkey(self):
        """
        Tests that the implementation of ``maxkey`` in the Collection class
        works as intended.

        Tests that we can get the key with the highest value, that we can
        define a ceiling, and that the meta object will not ever be returned
        (even if no other keys exist)
        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)

        with self.assertRaises(ValueError):
            grp.maxKey()

        keys = ['key0.0', 'key0.1', 'key0.2', 'key1.0', 'key1.1', 'key1.2',
                'key2.0', 'key2.1', 'key2.2']
        values = ['value0.0', 'value0.1', 'value0.2', 'value1.0', 'value1.1',
                  'value1.2', 'value2.0', 'value2.1', 'value2.2']
        items = {k: v for k, v in zip(keys, values)}
        for key, value in items.items():
            grp.insert(key, value)

        # tests that the highest key from our inserted values appears
        self.assertEqual(grp.maxKey(), keys[-1],
                         f'{grp.maxKey()} != {keys[-1]}')
        # tests that a lower-value key is returned if we set a ceiling
        self.assertEqual(grp.maxKey(max=keys[3]), keys[3],
                         f'{grp.maxKey(max=keys[3])} != {keys[3]}')

    def test_minKey(self):
        """
        Tests that the implementation of ``minkey`` in the Collection class
        works as intended.

        Tests that we can get the key with the highest value, that we can
        define a floor, and that the meta object will not ever be returned
        (even if no other keys exist)
        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)

        with self.assertRaises(ValueError):
            grp.minKey()

        keys = ['key0.0', 'key0.1', 'key0.2', 'key1.0', 'key1.1', 'key1.2',
                'key2.0', 'key2.1', 'key2.2']
        values = ['value0.0', 'value0.1', 'value0.2', 'value1.0', 'value1.1',
                  'value1.2', 'value2.0', 'value2.1', 'value2.2']
        items = {k: v for k, v in zip(keys, values)}
        for key, value in items.items():
            grp.insert(key, value)

        # tests that the highest key from our inserted values appears
        self.assertEqual(grp.minKey(), keys[0],
                         f'{grp.minKey()} != {keys[0]}')
        # tests that a lower-value key is returned if we set a ceiling
        self.assertEqual(grp.minKey(min=keys[3]), keys[3],
                         f'{grp.minKey(min=keys[3])} != {keys[3]}')

    def test_pop(self):
        """
        Tests that the implementation of ``pop`` in the Collection class
        works as intended.

        Tests that pop returns the correct value, that the value is removed
        from the collection after, that the meta object cannot be popped, and
        that attempting to pop a nonexistent object will raise a KeyError.
        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)
        keys = ['key0.0', 'key0.1', 'key0.2', 'key1.0', 'key1.1', 'key1.2',
                'key2.0', 'key2.1', 'key2.2']
        values = ['value0.0', 'value0.1', 'value0.2', 'value1.0', 'value1.1',
                  'value1.2', 'value2.0', 'value2.1', 'value2.2']
        items = {k: v for k, v in zip(keys, values)}
        for key, value in items.items():
            grp.insert(key, value)

        # test that we get the desired value for the key
        value = grp.pop(keys[2])
        self.assertEqual(value, values[2])

        # test that the key-value pair has disappeared from the collection
        self.assertNotIn(value, grp.values())
        self.assertNotIn(keys[2], grp.keys())

        # test that attempting to pop a nonexistent value will raise a KeyError
        with self.assertRaises(KeyError):
            grp.pop('nonexistent key')

        # test that default will be returned if popping a nonexistent key
        value = grp.pop('nonexistent key', 'default')
        self.assertEqual(value, 'default')

        # test that default will not be returned if popping an existent key
        value = grp.pop(keys[0], 'default')
        self.assertEqual(value, values[0])

    def test_popitem(self):
        """
        Tests that the implementation of ``pop`` in the Collection class
        works as intended.

        Tests that pop returns the correct value, that the value is removed
        from the collection after, that the meta object cannot be popped, and
        that attempting to pop a nonexistent object will raise a KeyError.
        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)
        keys = ['key0.0', 'key0.1', 'key0.2', 'key1.0', 'key1.1', 'key1.2',
                'key2.0', 'key2.1', 'key2.2']
        values = ['value0.0', 'value0.1', 'value0.2', 'value1.0', 'value1.1',
                  'value1.2', 'value2.0', 'value2.1', 'value2.2']
        items = {k: v for k, v in zip(keys, values)}
        for key, value in items.items():
            grp.insert(key, value)

        # test that we get the desired value for the key
        key, value = grp.popitem()
        self.assertEqual(key, keys[0])
        self.assertEqual(value, values[0])

        # test that the key-value pair has disappeared from the collection
        self.assertNotIn(key, grp.keys())
        self.assertNotIn(value, grp.values())

    def test_setdefault(self):
        """

        :return:
        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)
        keys = ['key0.0', 'key0.1', 'key0.2', 'key1.0', 'key1.1', 'key1.2',
                'key2.0', 'key2.1', 'key2.2']
        values = ['value0.0', 'value0.1', 'value0.2', 'value1.0', 'value1.1',
                  'value1.2', 'value2.0', 'value2.1', 'value2.2']
        items = {k: v for k, v in zip(keys, values)}
        for key, value in items.items():
            grp.insert(key, value)

        # test that the default is returned if the key does not exist
        value = grp.setdefault('key5', 'val5')
        self.assertEqual(value, 'val5')

        # test that the new value has been inserted
        self.assertEqual(grp.get('key5'), 'val5')

        # test that the key value is returned if the key does exist
        value = grp.setdefault(keys[0], 'val0-1')
        self.assertEqual(value, values[0])

        # test that the value was not changed
        self.assertEqual(grp.get(keys[0]), values[0])

    def test_byValue(self):
        """

        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)
        keys = ['key0.0', 'key0.1', 'key0.2', 'key1.0', 'key1.1', 'key1.2',
                'key2.0', 'key2.1', 'key2.2']
        values = ['value0.0', 'value0.1', 'value0.2', 'value1.0', 'value1.1',
                  'value1.2', 'value2.0', 'value2.1', 'value2.2']
        items = {k: v for k, v in zip(keys, values)}
        for key, value in items.items():
            grp.insert(key, value)

        value_key = tuple((value, key) for key, value in items.items())

        # test that we get an iterable of value-key pairs
        expected = value_key[::-1]
        actual = tuple(grp.byValue())
        self.assertEqual(expected, actual)

        # test that we get a list of value-key pairs where a minimum is set
        expected = value_key[2::][::-1]
        actual = tuple(grp.byValue(min='value0.2'))
        self.assertEqual(expected, actual)

    def test_clear(self):
        """

        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)
        keys = ['key0.0', 'key0.1', 'key0.2', 'key1.0', 'key1.1', 'key1.2',
                'key2.0', 'key2.1', 'key2.2']
        values = ['value0.0', 'value0.1', 'value0.2', 'value1.0', 'value1.1',
                  'value1.2', 'value2.0', 'value2.1', 'value2.2']
        items = {k: v for k, v in zip(keys, values)}
        for key, value in items.items():
            grp.insert(key, value)

        self.assertEqual(len(grp.keys()), len(keys))

        grp.clear()

        self.assertEqual(len(grp.keys()), 0)


    def test_has_key(self):
        """

        """
        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)

        # check that we receive an iterable that produces nothing
        self.assertEqual(list(grp.iterkeys()), [])

        collections = (Collection(), Collection(), Collection())
        grp = group.Group(collections=collections)
        keys = ['key0.0', 'key0.1', 'key0.2', 'key1.0', 'key1.1', 'key1.2',
                'key2.0', 'key2.1', 'key2.2']
        values = ['value0.0', 'value0.1', 'value0.2', 'value1.0', 'value1.1',
                  'value1.2', 'value2.0', 'value2.1', 'value2.2']
        items = {k: v for k, v in zip(keys, values)}
        for key, value in items.items():
            grp.insert(key, value)

        # test that keys in the collection are all found
        for key in keys:
            self.assertTrue(grp.has_key(key))

        # test that keys not in the collection are not found
        for key in ['key5', 'key6', 'key7']:
            self.assertFalse(grp.has_key(key))


class GroupDivisionTests(TestCase):
    """
    Test cases for citrine.storage.group.Group that ensures groups are dividing
    the data load across multiple collections correctly

    Tests the interface only incidentally, tests are primarily intended to
    check that objects are being assigned to the correct collections and that
    retrieval operations look for the correct location
    """



if __name__ == '__main__':
    main()

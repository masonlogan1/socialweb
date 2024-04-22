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

from unittest import TestCase, main
from unittest.mock import MagicMock, call, patch

from tempfile import NamedTemporaryFile, TemporaryDirectory, mkdtemp, mkstemp
from uuid import uuid4

from ZODB import DB
from ZODB.POSException import POSKeyError

from citrine.storage import container
from citrine.storage.group import Group

from citrine.storage.consts import HEALTHY, ACCEPTABLE, ALERT, WARNING, CRITICAL


class ContainerMetaTests(TestCase):
    """
    Tests that a Container's metadata is a reflection of the groups stored
    inside.
    """

    def test_size(self):
        """
        Tests that the size value matches the sum of the size of all groups
        """
        # test against one empty group
        mock_container = MagicMock()
        primary = MagicMock(size=0)
        mock_container.primary = primary
        mock_container.groups = (primary,)

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 0)

        # test against one group with one item
        mock_container = MagicMock()
        primary = MagicMock(size=1)
        mock_container.primary = primary
        mock_container.groups = (primary,)

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 1)

        # test against one group with multiple items
        mock_container = MagicMock()
        primary = MagicMock(size=10)
        mock_container.primary = primary
        mock_container.groups = (primary,)

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 10)

        # test against multiple empty groups
        mock_container = MagicMock()
        primary = MagicMock(size=0)
        mock_container.primary = primary
        mock_container.groups = (primary, MagicMock(size=0), MagicMock(size=0))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 0)

        # test against multiple groups, primary w/ one item, others empty
        mock_container = MagicMock()
        primary = MagicMock(size=1)
        mock_container.primary = primary
        mock_container.groups = (primary, MagicMock(size=0), MagicMock(size=0))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 1)

        # test against multiple groups, secondary w/ one item, others empty
        mock_container = MagicMock()
        primary = MagicMock(size=0)
        mock_container.primary = primary
        mock_container.groups = (primary, MagicMock(size=1), MagicMock(size=0))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 1)

        # test against multiple groups, primary w/ multiple items, others empty
        mock_container = MagicMock()
        primary = MagicMock(size=10)
        mock_container.primary = primary
        mock_container.groups = (primary, MagicMock(size=0), MagicMock(size=0))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 10)

        # test against multiple groups, secondary w/ multiple items, others empty
        mock_container = MagicMock()
        primary = MagicMock(size=0)
        mock_container.primary = primary
        mock_container.groups = (primary, MagicMock(size=10), MagicMock(size=0))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 10)

        # test against multiple groups, multiple w/ items, others empty
        mock_container = MagicMock()
        primary = MagicMock(size=10)
        mock_container.primary = primary
        mock_container.groups = (primary, MagicMock(size=10), MagicMock(size=0))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 20)

        mock_container = MagicMock()
        primary = MagicMock(size=0)
        mock_container.primary = primary
        mock_container.groups = (
        primary, MagicMock(size=10), MagicMock(size=10))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 20)

        # test against multiple groups, all w/ items
        mock_container = MagicMock()
        primary = MagicMock(size=10)
        mock_container.primary = primary
        mock_container.groups = (
        primary, MagicMock(size=10), MagicMock(size=10))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 30)

    def test_max_size(self):
        """
        Tests that the max_size value matches the capacity of all groups
        """
        # test against one group
        mock_container = MagicMock()
        primary = MagicMock(max_size=10)
        mock_container.primary = primary
        mock_container.groups = (primary,)

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.max_size, 10)

        # test against multiple groups w/ matching sizes
        mock_container = MagicMock()
        primary = MagicMock(max_size=10)
        mock_container.primary = primary
        mock_container.groups = (primary, MagicMock(max_size=10),
                                 MagicMock(max_size=10))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.max_size, 30)

        # test against multiple groups w/ different sizes
        mock_container = MagicMock()
        primary = MagicMock(max_size=10)
        mock_container.primary = primary
        mock_container.groups = (primary, MagicMock(max_size=20),
                                 MagicMock(max_size=30))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.max_size, 60)

    def test_capacity(self):
        """
        Tests the capacity value matches the capacity of the primary group
        """
        # test against one group
        mock_container = MagicMock()
        primary = MagicMock(max_size=10)
        mock_container.primary = primary
        mock_container.groups = (primary,)

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.capacity, 10)

        # test against multiple to make sure only primary group is used
        mock_container = MagicMock()
        primary = MagicMock(max_size=10)
        mock_container.primary = primary
        mock_container.groups = (primary, MagicMock(max_size=20),
                                 MagicMock(max_size=30))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.capacity, 10)

    def test_used(self):
        """
        Tests the used value matches the number of items in the primary group
        """
        # test against one group
        mock_container = MagicMock()
        primary = MagicMock(size=10)
        mock_container.primary = primary
        mock_container.groups = (primary,)

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.used, 10)

        # test against multiple to make sure only primary group is used
        mock_container = MagicMock()
        primary = MagicMock(size=10)
        mock_container.primary = primary
        mock_container.groups = (primary,
                                 MagicMock(max_size=20),
                                 MagicMock(max_size=30))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.used, 10)

    def test_usage(self):
        """
        Tests that the usage value matches the percentage of use of the primary
        group
        """
        # test against one group
        mock_container = MagicMock()
        primary = MagicMock(usage=0.55)
        mock_container.primary = primary
        mock_container.groups = (primary,)

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(int(meta.usage * 100), 55)

        # test against multiple to make sure only primary group is used
        mock_container = MagicMock()
        primary = MagicMock(usage=0.66)
        mock_container.primary = primary
        mock_container.groups = (primary,
                                 MagicMock(usage=0.33),
                                 MagicMock(usage=0.01))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(int(meta.usage * 100), 66)

    def test_status(self):
        """
        Tests that the status value matches the status of the primary group
        """
        # test against one group
        mock_container = MagicMock()
        primary = MagicMock(status=HEALTHY)
        mock_container.primary = primary
        mock_container.groups = (primary,)

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.status, HEALTHY)

        primary.status = WARNING
        self.assertEqual(meta.status, WARNING)

        # test against multiple to make sure only primary group is used
        mock_container = MagicMock()
        primary = MagicMock(status=HEALTHY)
        mock_container.primary = primary
        mock_container.groups = (primary,
                                 MagicMock(status=CRITICAL),
                                 MagicMock(status=ALERT))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.status, HEALTHY)

        primary.status = WARNING
        self.assertEqual(meta.status, WARNING)


class ContainerPropertyTests(TestCase):
    """
    Tests that a Container's metadata is passed directly through its properties
    """

    @patch.object(container, 'ContainerMeta')
    def test_meta(self, metamock):
        """
        Tests that the ``meta`` property will return the metadata object
        """
        primary = MagicMock()
        groups = (primary, MagicMock(max_size=20), MagicMock(max_size=30))
        obj = container.Container(primary, groups)

        self.assertEqual(metamock.return_value, obj.meta)

    def test_primary(self):
        """
        Tests that the ``primary`` property will return the primary group
        """
        # test when primary is only group
        primary = MagicMock()
        groups = (primary,)
        obj = container.Container(primary, groups)

        self.assertEqual(primary, obj.primary)

        # test when multiple groups are present
        primary = MagicMock()
        groups = (primary, MagicMock(max_size=20), MagicMock(max_size=30))
        obj = container.Container(primary, groups)

        self.assertEqual(primary, obj.primary)

    def test_groups(self):
        """
        Tests that the ``groups`` property will return the groups iterable
        """
        # test when primary is only group
        primary = MagicMock()
        groups = (primary,)
        obj = container.Container(primary, groups)

        self.assertEqual(groups, obj.groups)

        # test when multiple groups are present
        primary = MagicMock()
        groups = (primary, MagicMock(max_size=20), MagicMock(max_size=30))
        obj = container.Container(primary, groups)

        self.assertEqual(groups, obj.groups)

    def test_size(self):
        """
        Tests that the ``size`` property will return the number of items
        in all groups
        """
        # test when primary is only group and empty
        primary = MagicMock(size=0)
        groups = (primary,)
        obj = container.Container(primary, groups)

        expected = 0
        self.assertEqual(obj.size, expected)

        # test when primary is only group and has items
        primary = MagicMock(size=10)
        groups = (primary,)
        obj = container.Container(primary, groups)

        expected = 10
        self.assertEqual(obj.size, expected)

        # test with multiple groups; all empty
        primary = MagicMock(size=0)
        groups = (primary, MagicMock(size=0), MagicMock(size=0))
        obj = container.Container(primary, groups)

        expected = 0
        self.assertEqual(obj.size, expected)

        # test with multiple groups; only primary has items
        primary = MagicMock(size=5)
        groups = (primary, MagicMock(size=0), MagicMock(size=0))
        obj = container.Container(primary, groups)

        expected = 5
        self.assertEqual(obj.size, expected)

        # test with multiple groups; only secondary have items
        primary = MagicMock(size=0)
        groups = (primary, MagicMock(size=5), MagicMock(size=10))
        obj = container.Container(primary, groups)

        expected = 15
        self.assertEqual(obj.size, expected)

        # test with multiple groups; primary and secondary have items
        primary = MagicMock(size=5)
        groups = (primary, MagicMock(size=5), MagicMock(size=10))
        obj = container.Container(primary, groups)

        expected = 20
        self.assertEqual(obj.size, expected)

    def test_max_size(self):
        """
        Tests that the ``max_size`` property will return the maximum size of
        all groups
        """
        # test when primary is only group
        primary = MagicMock(max_size=5)
        groups = (primary,)
        obj = container.Container(primary, groups)

        expected = 5
        self.assertEqual(obj.max_size, expected)

        # test with multiple groups; all same size
        primary = MagicMock(max_size=5)
        groups = (primary, MagicMock(max_size=5), MagicMock(max_size=5))
        obj = container.Container(primary, groups)

        expected = 15
        self.assertEqual(obj.max_size, expected)

        # test with multiple groups; different sizes
        primary = MagicMock(max_size=5)
        groups = (primary, MagicMock(max_size=10), MagicMock(max_size=15))
        obj = container.Container(primary, groups)

        expected = 30
        self.assertEqual(obj.max_size, expected)

    def test_used(self):
        """
        Tests that the ``used`` property will return the number of items in
        the primary group
        """
        # test when primary is only group
        primary = MagicMock(size=5)
        groups = (primary,)
        obj = container.Container(primary, groups)

        expected = 5
        self.assertEqual(obj.used, expected)

        # test with multiple groups; all same used
        primary = MagicMock(size=10)
        groups = (primary, MagicMock(size=10), MagicMock(size=10))
        obj = container.Container(primary, groups)

        expected = 10
        self.assertEqual(obj.used, expected)

        # test with multiple groups; different used
        primary = MagicMock(size=15)
        groups = (primary, MagicMock(size=18), MagicMock(size=25))
        obj = container.Container(primary, groups)

        expected = 15
        self.assertEqual(obj.used, expected)

    def test_usage(self):
        """
        Tests that the ``usage`` property will return the percentage of used
        space in the primary group
        """
        # test when primary is only group
        primary = MagicMock(usage=.35)
        groups = (primary,)
        obj = container.Container(primary, groups)

        expected = 35
        self.assertEqual(int(obj.usage * 100), expected)

        # test with multiple groups; all same usage rate
        primary = MagicMock(usage=.24)
        groups = (primary, MagicMock(usage=.11), MagicMock(usage=.80))
        obj = container.Container(primary, groups)

        expected = 24
        self.assertEqual(int(obj.usage * 100), expected)

        # test with multiple groups; different usage rates
        primary = MagicMock(usage=.55)
        groups = (primary, MagicMock(usage=.65), MagicMock(usage=.14))
        obj = container.Container(primary, groups)

        expected = 55
        self.assertEqual(int(obj.usage * 100), expected)

    def test_status(self):
        """
        Tests that the ``status`` property will return the status of the primary
        group
        """
        # test when primary is only group
        primary = MagicMock(status=HEALTHY)
        groups = (primary,)
        obj = container.Container(primary, groups)

        expected = HEALTHY
        self.assertEqual(obj.status, expected)

        # test with multiple groups; all same status
        primary = MagicMock(status=WARNING)
        groups = (primary, MagicMock(status=WARNING), MagicMock(status=WARNING))
        obj = container.Container(primary, groups)

        expected = WARNING
        self.assertEqual(obj.status, expected)

        # test with multiple groups; different statuses
        primary = MagicMock(status=CRITICAL)
        groups = (primary, MagicMock(status=ALERT), MagicMock(status=HEALTHY))
        obj = container.Container(primary, groups)

        expected = CRITICAL
        self.assertEqual(obj.status, expected)

    def test_strict(self):
        """
        Tests that the ``strict`` property will return the strictness of the
        primary group
        """
        # test with only primary
        primary = MagicMock(strict=False)
        groups = (primary,)
        obj = container.Container(primary, groups)

        self.assertFalse(obj.strict)

        primary.strict = True
        self.assertTrue(obj.strict)

        # test with multiple groups; different strictnesses
        primary = MagicMock(strict=False)
        secondary0 = MagicMock(strict=False)
        groups = (primary, secondary0, MagicMock(strict=False))
        obj = container.Container(primary, groups)

        self.assertFalse(obj.strict)

        secondary0.strict = True
        self.assertFalse(obj.strict)

        primary.strict = True
        self.assertTrue(obj.strict)


class ContainerConstructorTests(TestCase):
    """
    Tests that a Container can be constructed either by passing in an
    existing group or through the use of ``Container.new`` to automatically
    generate an internal group prepared for a certain initial capacity.
    """

    def test_sets_correct_primary_group(self):
        """
        Tests that the primary group is set correctly to the ``primary``
        property
        """
        # tests that the primary is set if it is the only group
        primary = MagicMock()
        obj = container.Container(primary)

        self.assertEqual(primary, obj.primary)

        # tests that the primary is set if more than one group is present
        primary = MagicMock()
        groups = (primary, MagicMock(), MagicMock(), MagicMock())
        obj = container.Container(primary, groups)

        self.assertEqual(primary, obj.primary)

    def test_sets_all_groups(self):
        """
        Tests that the default init will add one or more groups to the
        ``groups`` property in the order they were provided in
        """
        # tests that all groups are added and in order
        primary = MagicMock()
        grp0 = MagicMock()
        grp1 = MagicMock()
        grp2 = MagicMock()
        groups = (primary, grp0, grp1, grp2)
        obj = container.Container(primary, groups)

        self.assertEqual(groups, obj.groups)

        # tests that if primary is not in groups it is added to the start
        primary = MagicMock()
        grp0 = MagicMock()
        grp1 = MagicMock()
        grp2 = MagicMock()
        groups = (grp0, grp1, grp2)
        obj = container.Container(primary, groups)

        expected = (primary, grp0, grp1, grp2)
        self.assertEqual(expected, obj.groups)

    def test_sets_strictness(self):
        """
        Tests that the default init will set the ``strict`` property correctly
        """
        # tests with only one group
        primary = MagicMock(strict=False)
        obj = container.Container(primary, strict=False)
        self.assertFalse(obj.strict)
        self.assertFalse(obj.primary.strict)

        primary = MagicMock(strict=True)
        obj = container.Container(primary, strict=True)
        self.assertTrue(obj.strict)
        self.assertTrue(obj.primary.strict)

        primary = MagicMock(strict=True)
        obj = container.Container(primary, strict=False)
        self.assertFalse(obj.strict)
        self.assertFalse(obj.primary.strict)

        primary = MagicMock(strict=False)
        obj = container.Container(primary, strict=True)
        self.assertTrue(obj.strict)
        self.assertTrue(obj.primary.strict)

        # tests with multiple groups (only primary is set)
        primary = MagicMock(strict=False)
        grp0 = MagicMock(strict=False)
        grp1 = MagicMock(strict=False)
        grp2 = MagicMock(strict=False)
        groups = (primary, grp0, grp1, grp2)
        obj = container.Container(primary, groups, strict=False)
        self.assertFalse(obj.strict)
        self.assertFalse(obj.primary.strict)
        for group in groups[1:]:
            self.assertFalse(group.strict)

        primary = MagicMock(strict=True)
        grp0 = MagicMock(strict=False)
        grp1 = MagicMock(strict=False)
        grp2 = MagicMock(strict=False)
        groups = (primary, grp0, grp1, grp2)
        obj = container.Container(primary, groups, strict=True)
        self.assertTrue(obj.strict)
        self.assertTrue(obj.primary.strict)
        for group in groups[1:]:
            self.assertFalse(group.strict)

        primary = MagicMock(strict=True)
        grp0 = MagicMock(strict=False)
        grp1 = MagicMock(strict=False)
        grp2 = MagicMock(strict=False)
        groups = (primary, grp0, grp1, grp2)
        obj = container.Container(primary, groups, strict=False)
        self.assertFalse(obj.strict)
        self.assertFalse(obj.primary.strict)
        for group in groups[1:]:
            self.assertFalse(group.strict)

        primary = MagicMock(strict=False)
        grp0 = MagicMock(strict=False)
        grp1 = MagicMock(strict=False)
        grp2 = MagicMock(strict=False)
        groups = (primary, grp0, grp1, grp2)
        obj = container.Container(primary, groups, strict=True)
        self.assertTrue(obj.strict)
        self.assertTrue(obj.primary.strict)
        for group in groups[1:]:
            self.assertFalse(group.strict)

    def test_new_default_constructors(self):
        """
        Tests that ``Container.new`` creates a container with the correct
        sizing and collections with the default parameters.
        """
        # tests that 20 collections are created
        obj = container.Container.new()
        expected = 23
        self.assertEqual(len(obj.primary.collections), expected)

    def test_new_custom_capacity(self):
        """
        Tests that ``Container.new`` creates a container with a provided
        ``capacity`` parameter and the default ``collection_max_size``
        """
        # tests that 1 collection is created
        obj = container.Container.new(capacity=5000)
        expected_collections = 1
        expected_size = 5000
        self.assertEqual(len(obj.primary.collections), expected_collections)
        self.assertEqual(obj.primary.max_size, expected_size)

        # tests that 11 collections are created
        obj = container.Container.new(capacity=50000)
        expected_collections = 11
        expected_size = 55000
        self.assertEqual(len(obj.primary.collections), expected_collections)
        self.assertEqual(obj.primary.max_size, expected_size)

        # tests that 30 collections are created
        obj = container.Container.new(capacity=150000)
        expected_collections = 31
        expected_size = 155000
        self.assertEqual(len(obj.primary.collections), expected_collections)
        self.assertEqual(obj.primary.max_size, expected_size)

        # tests that a group can be created with a capacity smaller than
        # collection_max_size
        obj = container.Container.new(capacity=150)
        expected_collections = 1
        expected_size = 150
        self.assertEqual(len(obj.primary.collections), expected_collections)
        self.assertEqual(obj.primary.max_size, expected_size)

    def test_new_custom_collection_max_size(self):
        """
        Tests that ``Container.new`` creates a container with a provided
        ``collection_max_size`` parameter and the default ``capacity``
        """
        # tests that 1 collection is created
        obj = container.Container.new(collection_max_size=100000)
        expected_collections = 1
        expected_size = 100000
        self.assertEqual(len(obj.primary.collections), expected_collections)
        self.assertEqual(obj.primary.max_size, expected_size)

        # tests that 11 collections are created
        obj = container.Container.new(collection_max_size=10000)
        expected_collections = 11
        expected_size = 110000
        self.assertEqual(len(obj.primary.collections), expected_collections)
        self.assertEqual(obj.primary.max_size, expected_size)

        # tests that 31 collections are created
        obj = container.Container.new(collection_max_size=3300)
        expected_collections = 31
        expected_size = 102300
        self.assertEqual(len(obj.primary.collections), expected_collections)
        self.assertEqual(obj.primary.max_size, expected_size)

    def test_new_custom_capacity_and_collection_max_size(self):
        """
        Tests that ``Container.new`` creates a container with provided
        ``capacity`` and ``collection_max_size`` parameters
        """
        # tests that 1 collection is created
        # tests that 1 collection is created
        obj = container.Container.new(capacity=1000, collection_max_size=1000)
        expected_collections = 1
        expected_size = 1000
        self.assertEqual(len(obj.primary.collections), expected_collections)
        self.assertEqual(obj.primary.max_size, expected_size)

        # tests that 11 collections are created
        obj = container.Container.new(capacity=9000, collection_max_size=850)
        expected_collections = 11
        expected_size = 9350
        self.assertEqual(len(obj.primary.collections), expected_collections)
        self.assertEqual(obj.primary.max_size, expected_size)

        # tests that 31 collections are created
        obj = container.Container.new(capacity=99000, collection_max_size=3300)
        expected_collections = 31
        expected_size = 102300
        self.assertEqual(len(obj.primary.collections), expected_collections)
        self.assertEqual(obj.primary.max_size, expected_size)

        # tests that a group can be created with a capacity smaller than
        # collection_max_size
        obj = container.Container.new(capacity=150, collection_max_size=1500)
        expected_collections = 1
        expected_size = 150
        self.assertEqual(len(obj.primary.collections), expected_collections)
        self.assertEqual(obj.primary.max_size, expected_size)

    def test_new_custom_strict(self):
        """
        Tests that ``Container.new`` creates a container with a provided
        ``strict`` parameter
        """
        # test that strict mode is enabled
        obj = container.Container.new(strict=True)
        self.assertTrue(obj.strict)
        self.assertTrue(obj.primary.strict)

        # test that strict mode is disabled
        obj = container.Container.new(strict=False)
        self.assertFalse(obj.strict)
        self.assertFalse(obj.primary.strict)


class ContainerReadWriteTests(TestCase):
    """
    Tests that a Container can use the standard ``read``, ``write``, ``has``,
    and ``delete`` methods for reading and writing to the internal group.
    """

    def test_write(self):
        """
        Tests that a Container can write to the primary group.
        """
        # test that a single-group Container can write an object to an id
        id = 'id0'
        value = 'value0'

        obj = container.Container.new()
        obj.write(id, value)

        self.assertEqual(obj.primary.get(id), value)

        # test that a single-group Container can overwrite an existing object
        id = 'id1'
        value = 'value1'

        obj = container.Container.new()
        obj.write(id, value)

        new_value = 'value1-0'
        obj.write(id, new_value)

        self.assertEqual(obj.primary.get(id), new_value)

        # test that a multi-group Container writes an object to ONLY the primary
        id = 'id2'
        value = 'value2'

        obj = container.Container.new(capacity=30, collection_max_size=10)
        obj.write(id, value)

        self.assertEqual(obj.primary.get(id), value)

        for group in obj.groups[1:]:
            self.assertFalse(group.has(id))

        # test that a multi-group Container overwrites ONLY on the primary
        id = 'id3'
        value = 'value3'

        primary = Group.new(1)
        groups = (primary, Group.new(1))
        obj = container.Container(primary, groups)

        # inserting value into the primary and secondary
        obj.groups[1].insert(id, value)
        obj.write(id, value)

        new_value = 'value3-0'
        obj.write(id, new_value)

        # primary should be updated, secondary should not
        self.assertEqual(obj.primary.get(id), new_value)
        self.assertEqual(obj.groups[1].get(id), value)

        # test that attempting to use a non-string ID will raise a TypeError
        id = 0
        value = 'bad value'

        obj = container.Container.new(capacity=30, collection_max_size=10)

    def test_read(self):
        """
        Tests that a Container can read from the groups
        """
        # test that a single-group Container can read an object from the group
        id = 'id0-0'
        value = 'value0-0'

        obj = container.Container.new()
        obj.primary.insert(id, value)

        self.assertEqual(obj.read(id), value)

        # test that a single-group Container will return the default value if
        # an object does not exist
        id = 'id1-0'
        default = 'default1-0'

        obj = container.Container.new()

        self.assertEqual(obj.read(id, default), default)

        # test that a single-group Container will return None if the value is
        # not present
        id = 'id2-0'

        obj = container.Container.new()

        self.assertIsNone(obj.read(id))

        # test that a multi-group Container will read an object from the
        # primary if it is found there
        id = 'id3-0'
        value = 'value3-0'
        alt_value_1 = 'value3-1'
        alt_value_2 = 'value3-2'


        primary = Group.new(1)
        groups = (primary, Group.new(1), Group.new(2))
        obj = container.Container(primary, groups)

        obj.primary.insert(id, value)
        obj.groups[1].insert(id, alt_value_1)
        obj.groups[2].insert(id, alt_value_2)

        self.assertEqual(obj.read(id), value)

        # test that a multi-group Container will read an object from the first
        # secondary if it is found there
        id = 'id4-0'
        alt_value_1 = 'value4-1'
        alt_value_2 = 'value4-2'

        primary = Group.new(1)
        groups = (primary, Group.new(1), Group.new(2))
        obj = container.Container(primary, groups)

        obj.groups[1].insert(id, alt_value_1)
        obj.groups[2].insert(id, alt_value_2)

        self.assertEqual(obj.read(id), alt_value_1)

        # test that a multi-group Container will return the default value if
        # an object does not exist
        id = 'id5-0'
        default = 'default5-0'

        primary = Group.new(1)
        groups = (primary, Group.new(1), Group.new(2))
        obj = container.Container(primary, groups)

        self.assertEqual(obj.read(id, default), default)

        # test that a multi-group Container will return None if the value is
        # not present
        primary = Group.new(1)
        groups = (primary, Group.new(1), Group.new(2))
        obj = container.Container(primary, groups)

        self.assertIsNone(obj.read(id))

    def test_delete(self):
        """
        Tests that a Container can delete from the primary group.
        """
        # test that a single-group Container can remove an item
        id = 'id0-0'
        value = 'value0-0'

        obj = container.Container.new()
        obj.primary.insert(id, value)
        self.assertEqual(obj.primary.get(id), value)

        obj.delete(id)
        self.assertIsNone(obj.primary.get(id))

        # test that a single-group Container will do nothing if an item does not
        # exist
        id = 'id1-0'

        obj = container.Container.new()
        self.assertIsNone(obj.primary.get(id))

        obj.delete(id)
        self.assertIsNone(obj.primary.get(id))

        # test that a multi-group Container will delete all instances of
        # an object
        id = 'id2-0'
        value = 'value2-0'
        alt_value_1 = 'value2-1'
        alt_value_2 = 'value2-2'

        primary = Group.new(1)
        groups = (primary, Group.new(1), Group.new(2))
        obj = container.Container(primary, groups)

        obj.primary.insert(id, value)
        obj.groups[1].insert(id, alt_value_1)
        obj.groups[2].insert(id, alt_value_2)

        self.assertEqual(obj.primary.get(id), value)
        self.assertEqual(obj.groups[1].get(id), alt_value_1)
        self.assertEqual(obj.groups[2].get(id), alt_value_2)

        obj.delete(id)

        self.assertIsNone(obj.primary.get(id))
        self.assertIsNone(obj.groups[1].get(id))
        self.assertIsNone(obj.groups[2].get(id))

        # test that a multi-group Container will do nothing if an item is not
        # found in any of the groups
        id = 'id3-0'

        primary = Group.new(1)
        groups = (primary, Group.new(1), Group.new(2))
        obj = container.Container(primary, groups)

        self.assertIsNone(obj.primary.get(id))
        self.assertIsNone(obj.groups[1].get(id))
        self.assertIsNone(obj.groups[2].get(id))

        obj.delete(id)

        self.assertIsNone(obj.primary.get(id))
        self.assertIsNone(obj.groups[1].get(id))
        self.assertIsNone(obj.groups[2].get(id))

    def test_has(self):
        """
        Tests that a Container will return True if an object is located in any
        of the groups
        """
        # test that a single-group Container returns 1 if an item is found
        id = 'id0-0'
        value = 'value0-0'

        obj = container.Container.new()
        obj.primary.insert(id, value)

        expected = 1
        self.assertEqual(obj.has(id), expected)

        # test that a single-group Container returns 0 if an item is not found
        id = 'id1-0'

        obj = container.Container.new()

        expected = 0
        self.assertEqual(obj.has(id), expected)

        # test that a multi-group Container returns the number of times an item
        # is found
        id = 'id2-0'
        value = 'value2-0'
        alt_value_1 = 'value2-1'
        alt_value_2 = 'value2-2'

        primary = Group.new(1)
        groups = (primary, Group.new(1), Group.new(2))
        obj = container.Container(primary, groups)

        obj.primary.insert(id, value)
        obj.groups[1].insert(id, alt_value_1)
        obj.groups[2].insert(id, alt_value_2)

        expected = 3
        self.assertEqual(obj.has(id), expected)

        # test that a multi-group Container returns 0 if an item is not found
        id = 'id3-0'

        primary = Group.new(1)
        groups = (primary, Group.new(1), Group.new(2))
        obj = container.Container(primary, groups)

        expected = 0
        self.assertEqual(obj.has(id), expected)


class ContainerInternalCondenseTests(TestCase):
    """
    Tests that a Container can condense its secondary containers into the
    primary container.
    """
    def test_single_secondary_condense_without_transfer_without_overlap(self):
        """
        Tests that a Container can condense a single secondary container into
        the primary container without damaging the secondary containers
        """
        primary = Group.new(3)
        secondary = Group.new(7)
        groups = (primary, secondary)
        obj = container.Container(primary, groups)

        primary_keys = ['0', '1', '2', '3', '4']
        secondary_keys = ['5', '6', '7', '8', '9']

        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0']
        secondary_values = ['val5.1', 'val6.1', 'val7.1', 'val8.1', 'val9.1']

        keys = primary_keys + secondary_keys
        values = primary_values + secondary_values

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)

        # check that none of these keys are in the current primary
        for key in secondary_keys:
            self.assertFalse(obj.primary.has_key(key))

        obj.condense(transfer=False)

        # check that all keys are in the new primary
        for key in keys:
            self.assertTrue(obj.primary.has_key(key))
        # check that all values are correct
        for key, value in zip(keys, values):
            self.assertEquals(obj.primary.get(key), value)

        # check that secondary group still has its contents
        self.assertEqual(obj.groups[1], secondary)
        for key, value in zip(secondary_keys, secondary_values):
            self.assertTrue(obj.groups[1].has_key(key))
            self.assertEqual(obj.groups[1].get(key), value)

    def test_single_secondary_condense_without_transfer_with_overlap(self):
        """
        Tests that a Container can condense a single secondary container into
        the primary container without damaging the secondary containers.
        Overlapping keys should keep the primary group's value
        """
        primary = Group.new(3)
        secondary = Group.new(7)
        groups = (primary, secondary)
        obj = container.Container(primary, groups)

        primary_keys = ['0', '1', '2', '3', '4', '5']
        secondary_keys = ['4', '5', '6', '7', '8', '9']

        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0']
        secondary_values = ['val4.1', 'val5.1', 'val6.1', 'val7.1', 'val8.1',
                            'val9.1']

        keys = primary_keys + secondary_keys[2:]
        values = primary_values + secondary_values[2:]

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)

        # check that none of these keys are in the current primary
        for key in secondary_keys[2:]:
            self.assertFalse(obj.primary.has_key(key))

        obj.condense(transfer=False)

        # check that all keys are in the new primary
        for key in keys:
            self.assertTrue(obj.primary.has_key(key))
        # check that all values are correct
        for key, value in zip(keys, values):
            self.assertEquals(obj.primary.get(key), value)

        # check that secondary group still has its contents
        self.assertEqual(obj.groups[1], secondary)
        for key, value in zip(secondary_keys, secondary_values):
            self.assertTrue(obj.groups[1].has_key(key))
            self.assertEqual(obj.groups[1].get(key), value)

    def test_multiple_secondary_condense_without_transfer_without_overlap(self):
        """
        Tests that a Container can condense multiple secondary containers into
        the primary container without damaging the secondary containers
        """
        primary = Group.new(3)
        secondary = Group.new(7)
        tertiary = Group.new(11)
        groups = (primary, secondary, tertiary)
        obj = container.Container(primary, groups)

        primary_keys = ['0', '1', '2']
        secondary_keys = ['3', '4', '5']
        tertiary_keys = ['6', '7', '8', '9']

        primary_values = ['val0.0', 'val1.0', 'val2.0']
        secondary_values = ['val3.1', 'val4.1', 'val5.1']
        tertiary_values = ['val6.2', 'val7.2', 'val8.2', 'val9.2']

        keys = primary_keys + secondary_keys + tertiary_keys
        values = primary_values + secondary_values + tertiary_values

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # check that none of these keys are in the current primary
        for key in secondary_keys + tertiary_keys:
            self.assertFalse(obj.primary.has_key(key))

        obj.condense(transfer=False)

        # check that all keys are in the new primary
        for key in keys:
            self.assertTrue(obj.primary.has_key(key))
        # check that all values are correct
        for key, value in zip(keys, values):
            self.assertEquals(obj.primary.get(key), value)

        # check that secondary group still has its contents
        self.assertEqual(obj.groups[1], secondary)
        for key, value in zip(secondary_keys, secondary_values):
            self.assertTrue(obj.groups[1].has_key(key))
            self.assertEqual(obj.groups[1].get(key), value)
        # check that tertiary group still has its contents
        self.assertEqual(obj.groups[2], tertiary)
        for key, value in zip(tertiary_keys, tertiary_values):
            self.assertTrue(obj.groups[2].has_key(key))
            self.assertEqual(obj.groups[2].get(key), value)

    def test_multiple_secondary_condense_without_transfer_with_overlap(self):
        """
        Tests that a Container can condense multiple secondary containers into
        the primary container without damaging the secondary containers
        """
        primary = Group.new(3)
        secondary = Group.new(7)
        tertiary = Group.new(11)
        groups = (primary, secondary, tertiary)
        obj = container.Container(primary, groups)

        primary_keys = ['0', '1', '2', '3']
        secondary_keys = ['2', '3', '4', '5', '6']
        tertiary_keys = ['5', '6', '7', '8', '9']

        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0']
        secondary_values = ['val2.1', 'val3.1', 'val4.1', 'val5.1', 'val6.1']
        tertiary_values = ['val5.2', 'val6.2', 'val7.2', 'val8.2', 'val9.2']

        keys = primary_keys + secondary_keys[2:] + tertiary_keys[2:]
        values = primary_values + secondary_values[2:] + tertiary_values[2:]

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # check that none of these keys are in the current primary
        for key in secondary_keys[2:] + tertiary_keys[2:]:
            self.assertFalse(obj.primary.has_key(key))

        obj.condense(transfer=False)

        # check that all keys are in the new primary
        for key in keys:
            self.assertTrue(obj.primary.has_key(key))
        # check that all values are correct
        for key, value in zip(keys, values):
            self.assertEquals(obj.primary.get(key), value)

        # check that secondary group still has its contents
        self.assertEqual(obj.groups[1], secondary)
        for key, value in zip(secondary_keys, secondary_values):
            self.assertTrue(obj.groups[1].has_key(key))
            self.assertEqual(obj.groups[1].get(key), value)
        # check that tertiary group still has its contents
        self.assertEqual(obj.groups[2], tertiary)
        for key, value in zip(tertiary_keys, tertiary_values):
            self.assertTrue(obj.groups[2].has_key(key))
            self.assertEqual(obj.groups[2].get(key), value)

    def test_single_secondary_condense_with_transfer_without_overlap(self):
        """
        Tests that a Container can condense a single secondary container into
        the primary container and emptying the secondary containers
        """
        primary = Group.new(3)
        secondary = Group.new(7)
        groups = (primary, secondary)
        obj = container.Container(primary, groups)

        primary_keys = ['0', '1', '2', '3', '4']
        secondary_keys = ['5', '6', '7', '8', '9']

        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0']
        secondary_values = ['val5.1', 'val6.1', 'val7.1', 'val8.1', 'val9.1']

        keys = primary_keys + secondary_keys
        values = primary_values + secondary_values

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)

        # check that none of these keys are in the current primary
        for key in secondary_keys:
            self.assertFalse(obj.primary.has_key(key))

        returned = obj.condense(transfer=True)

        # check that all keys are in the new primary
        for key in keys:
            self.assertTrue(obj.primary.has_key(key))
        # check that all values are correct
        for key, value in zip(keys, values):
            self.assertEquals(obj.primary.get(key), value)

        # check that the original groups have been drained
        empty = 0
        self.assertEqual(secondary.size, empty)

        # check that the primary is the only group
        self.assertEqual(obj.groups, (obj.primary,))

        # check that we received the secondary group back
        self.assertEqual(returned, [secondary,])

    def test_single_secondary_condense_with_transfer_with_overlap(self):
        """
        Tests that a Container can condense a single secondary container into
        the primary container and emptying the secondary containers
        """
        primary = Group.new(3)
        secondary = Group.new(7)
        groups = (primary, secondary)
        obj = container.Container(primary, groups)

        primary_keys = ['0', '1', '2', '3', '4', '5']
        secondary_keys = ['4', '5', '6', '7', '8', '9']

        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0']
        secondary_values = ['val4.1', 'val5.1', 'val6.1', 'val7.1', 'val8.1',
                            'val9.1']

        keys = primary_keys + secondary_keys[2:]
        values = primary_values + secondary_values[2:]

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)

        # check that none of these keys are in the current primary
        for key in secondary_keys[2:]:
            self.assertFalse(obj.primary.has_key(key))

        returned = obj.condense(transfer=True)

        # check that all keys are in the new primary
        for key in keys:
            self.assertTrue(obj.primary.has_key(key))
        # check that all values are correct
        for key, value in zip(keys, values):
            self.assertEquals(obj.primary.get(key), value)

        # check that the original groups have been drained
        empty = 0
        self.assertEqual(secondary.size, empty)

        # check that the primary is the only group
        self.assertEqual(obj.groups, (obj.primary,))

        # check that we received the secondary group back
        self.assertEqual(returned, [secondary])

    def test_multiple_secondary_condense_with_transfer_without_overlap(self):
        """
        Tests that a Container can condense multiple secondary containers into
        the primary container and emptying the secondary containers
        """
        primary = Group.new(3)
        secondary = Group.new(7)
        tertiary = Group.new(11)
        groups = (primary, secondary, tertiary)
        obj = container.Container(primary, groups)

        primary_keys = ['0', '1', '2']
        secondary_keys = ['3', '4', '5']
        tertiary_keys = ['6', '7', '8', '9']

        primary_values = ['val0.0', 'val1.0', 'val2.0']
        secondary_values = ['val3.1', 'val4.1', 'val5.1']
        tertiary_values = ['val6.2', 'val7.2', 'val8.2', 'val9.2']

        keys = primary_keys + secondary_keys + tertiary_keys
        values = primary_values + secondary_values + tertiary_values

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # check that none of these keys are in the current primary
        for key in secondary_keys + tertiary_keys:
            self.assertFalse(obj.primary.has_key(key))

        returned = obj.condense(transfer=True)

        # check that all keys are in the new primary
        for key in keys:
            self.assertTrue(obj.primary.has_key(key))
        # check that all values are correct
        for key, value in zip(keys, values):
            self.assertEquals(obj.primary.get(key), value)

        # check that the original groups have been drained
        empty = 0
        self.assertEqual(secondary.size, empty)
        self.assertEqual(tertiary.size, empty)

        # check that the primary is the only group
        self.assertEqual(obj.groups, (obj.primary,))

        # check that we received the secondary group back
        self.assertEqual(returned, [secondary, tertiary])

    def test_multiple_secondary_condense_with_transfer_with_overlap(self):
        """
        Tests that a Container can condense multiple secondary containers into
        the primary container and emptying the secondary containers
        """
        primary = Group.new(3)
        secondary = Group.new(7)
        tertiary = Group.new(11)
        groups = (primary, secondary, tertiary)
        obj = container.Container(primary, groups)

        primary_keys = ['0', '1', '2', '3']
        secondary_keys = ['2', '3', '4', '5', '6']
        tertiary_keys = ['5', '6', '7', '8', '9']

        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0']
        secondary_values = ['val2.1', 'val3.1', 'val4.1', 'val5.1', 'val6.1']
        tertiary_values = ['val5.2', 'val6.2', 'val7.2', 'val8.2', 'val9.2']

        keys = primary_keys + secondary_keys[2:] + tertiary_keys[2:]
        values = primary_values + secondary_values[2:] + tertiary_values[2:]

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # check that none of these keys are in the current primary
        for key in secondary_keys[2:] + tertiary_keys[2:]:
            self.assertFalse(obj.primary.has_key(key))

        returned = obj.condense(transfer=True)

        # check that all keys are in the new primary
        for key in keys:
            self.assertTrue(obj.primary.has_key(key))
        # check that all values are correct
        for key, value in zip(keys, values):
            self.assertEquals(obj.primary.get(key), value)

        # check that the original groups have been drained
        empty = 0
        self.assertEqual(secondary.size, empty)
        self.assertEqual(tertiary.size, empty)

        # check that the primary is the only group
        self.assertEqual(obj.groups, (obj.primary,))

        # check that we received the secondary group back
        self.assertEqual(returned, [secondary, tertiary])


class ContainerInternalResizeTests(TestCase):
    """
    Tests that a Container can manually and automatically resize its internal
    group in-place.
    """
    def test_single_group_resize_without_transfer_or_condense_no_overlap(self):
        """
        Tests that a Container can create a new primary group and copy all
        existing primary group content into it without emptying the previous
        primary group or including any data from the secondary groups
        """
        primary = Group.new(3)
        obj = container.Container(primary, (primary,))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0', 'val6.0', 'val7.0', 'val8.0', 'val9.0']

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        obj.resize(new_capacity, transfer=False)

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have two groups, the second being the previous primary
        expected_num_groups = 2
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertEqual(obj.groups[1], primary)

        # check the new primary has all of its values
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.primary.has_key(key))
            self.assertTrue(obj.primary.get(key), value)
        # check the old primary has all of its values
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.primary.has_key(key))
            self.assertTrue(obj.primary.get(key), value)

    def test_multiple_group_resize_without_transfer_or_condense_no_overlap(self):
        """
        Tests that a Container can create a new primary group and copy all
        existing primary group content into it without emptying the previous
        primary group or including any data from the secondary groups
        """
        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)
        obj = container.Container(primary, (primary, secondary, tertiary))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0']
        secondary_keys = ['5', '6', '7', '8', '9']
        secondary_values = ['val5.0', 'val6.0', 'val7.0', 'val8.0', 'val9.0']
        tertiary_keys = ['10', '11', '12', '13', '14']
        tertiary_values = ['val10.0', 'val11.0', 'val12.0', 'val13.0', 'val14.0']

        keys = primary_keys + secondary_keys + tertiary_keys
        values = primary_values + secondary_values + tertiary_values

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        removed_groups = obj.resize(new_capacity, transfer=False)

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have two groups, the second being the previous primary
        expected_num_groups = 4
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertEqual(obj.groups[1], primary)

        # check the new primary has all values from the old primary
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.primary.has_key(key))
            self.assertTrue(obj.primary.get(key), value)
        # check the old primary has all of its values
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.groups[1].has_key(key))
            self.assertTrue(obj.groups[1].get(key), value)
        # check the secondary has all of its values
        for key, value in zip(secondary_keys, secondary_values):
            self.assertTrue(obj.groups[2].has_key(key))
            self.assertTrue(obj.groups[2].get(key), value)
        # check the tertiary has all of its values
        for key, value in zip(tertiary_keys, tertiary_values):
            self.assertTrue(obj.groups[3].has_key(key))
            self.assertTrue(obj.groups[3].get(key), value)

    def test_single_group_resize_with_transfer_without_condense_no_overlap(self):
        """
        Tests that a Container can create a new primary group and copy all
        existing primary group content into it, emptying the previous primary,
        and ignoring all secondary groups
        """
        primary = Group.new(3)
        obj = container.Container(primary, (primary,))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0', 'val6.0', 'val7.0', 'val8.0', 'val9.0']

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        returned = obj.resize(new_capacity, transfer=True)

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have only the new primary
        expected_num_groups = 1
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertNotEqual(obj.primary, primary)

        # check the new primary has all of its values
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.primary.has_key(key),
                            f'no key "{key}" in primary: {list(obj.primary.keys())}')
            self.assertTrue(obj.primary.get(key), value)
        # check the old primary has no values
        self.assertEqual(primary.size, 0)

    def test_multiple_group_resize_with_transfer_without_condense_no_overlap(self):
        """
        Tests that a Container can create a new primary group and copy all
        existing primary group content into it, emptying the previous primary,
        and ignoring all secondary groups
        """
        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)
        obj = container.Container(primary, (primary, secondary, tertiary))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0']
        secondary_keys = ['5', '6', '7', '8', '9']
        secondary_values = ['val5.0', 'val6.0', 'val7.0', 'val8.0', 'val9.0']
        tertiary_keys = ['10', '11', '12', '13', '14']
        tertiary_values = ['val10.0', 'val11.0', 'val12.0', 'val13.0',
                           'val14.0']

        keys = primary_keys + secondary_keys + tertiary_keys
        values = primary_values + secondary_values + tertiary_values

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        removed_groups = obj.resize(new_capacity, transfer=True)

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have only the new primary, secondary, and tertiary
        expected_num_groups = 3
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertNotEqual(obj.primary, primary)

        # check the new primary has the values taken from the old primary group
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.primary.has_key(key),
                            f'no key "{key}" in primary: {list(obj.primary.keys())}')
            self.assertTrue(obj.primary.get(key), value)
        # check the old primary has no values
        self.assertEqual(removed_groups[0].size, 0)
        # check the secondary has all of its values
        for key, value in zip(secondary_keys, secondary_values):
            self.assertTrue(obj.groups[1].has_key(key))
            self.assertEqual(obj.groups[1].get(key), value)
        # check the tertiary has all of its values
        for key, value in zip(tertiary_keys, tertiary_values):
            self.assertTrue(obj.groups[2].has_key(key))
            self.assertEqual(obj.groups[2].get(key), value)

    def test_single_group_resize_without_transfer_with_condense_no_overlap(self):
        """
        Tests that a Container can create a new primary group and copy all
        existing primary and secondary group content into it, but leaves the
        previous primary and all secondary groups intact
        """
        primary = Group.new(3)
        obj = container.Container(primary, (primary,))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0', 'val6.0', 'val7.0', 'val8.0', 'val9.0']

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        obj.resize(new_capacity, transfer=False)

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have two groups, the second being the previous primary
        expected_num_groups = 2
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertEqual(obj.groups[1], primary)

        # check the new primary has all of its values
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.primary.has_key(key))
            self.assertEqual(obj.primary.get(key), value)
        # check the old primary has all of its values
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.primary.has_key(key))
            self.assertEqual(obj.primary.get(key), value)

    def test_multiple_group_resize_without_transfer_with_condense_no_overlap(self):
        """
        Tests that a Container can create a new primary group and copy all
        existing primary and secondary group content into it, and leaves the
        former primary and all secondary groups intact
        """
        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)
        obj = container.Container(primary, (primary, secondary, tertiary))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0']
        secondary_keys = ['5', '6', '7', '8', '9']
        secondary_values = ['val5.0', 'val6.0', 'val7.0', 'val8.0', 'val9.0']
        tertiary_keys = ['10', '11', '12', '13', '14']
        tertiary_values = ['val10.0', 'val11.0', 'val12.0', 'val13.0',
                           'val14.0']

        keys = primary_keys + secondary_keys + tertiary_keys
        values = primary_values + secondary_values + tertiary_values

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        removed_groups = obj.resize(new_capacity, transfer=False, condense=True)

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have only the new primary, secondary, and tertiary
        expected_num_groups = 4
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertNotEqual(obj.primary, primary)

        # check the new primary has the values taken from all old groups
        for key, value in zip(keys, values):
            self.assertTrue(obj.primary.has_key(key),
                            f'no key "{key}" in primary: {list(obj.primary.keys())}')
            self.assertTrue(obj.primary.get(key), value)
        # check the old primary has ALL previous values
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.groups[1].has_key(key))
            self.assertEqual(obj.groups[1].get(key), value)
            self.assertEqual(obj.groups[1].size, len(primary_keys))
        # check the secondary has all of its values
        for key, value in zip(secondary_keys, secondary_values):
            self.assertTrue(obj.groups[2].has_key(key))
            self.assertEqual(obj.groups[2].get(key), value)
            self.assertEqual(obj.groups[2].size, len(secondary_keys))
        # check the tertiary has all of its values
        for key, value in zip(tertiary_keys, tertiary_values):
            self.assertTrue(obj.groups[3].has_key(key))
            self.assertEqual(obj.groups[3].get(key), value)
            self.assertEqual(obj.groups[3].size, len(tertiary_keys))

    def test_single_group_resize_with_transfer_with_condense_no_overlap(self):
        """
        Test that a Container can create a new primary group and copy all
        existing primary and secondary group content into it, emptying the
        previous primary and all secondary groups and removing them from the
        group listing
        """
        primary = Group.new(3)
        obj = container.Container(primary, (primary,))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0', 'val6.0', 'val7.0', 'val8.0', 'val9.0']

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        returned = obj.resize(new_capacity, condense=True, transfer=True)

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have only the new primary
        expected_num_groups = 1
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertNotEqual(obj.primary, primary)

        # check the new primary has all of its values
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.primary.has_key(key),
                            f'no key "{key}" in primary: {list(obj.primary.keys())}')
            self.assertTrue(obj.primary.get(key), value)
        # check the old primary has no values
        self.assertEqual(primary.size, 0)

    def test_multiple_group_resize_with_transfer_with_condense_no_overlap(self):
        """
        Test that a Container can create a new primary group and copy all
        existing primary and secondary group content into it, emptying the
        previous primary and all secondary groups and removing them from the
        group listing
        """
        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)
        obj = container.Container(primary, (primary, secondary, tertiary))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0']
        secondary_keys = ['5', '6', '7', '8', '9']
        secondary_values = ['val5.0', 'val6.0', 'val7.0', 'val8.0', 'val9.0']
        tertiary_keys = ['10', '11', '12', '13', '14']
        tertiary_values = ['val10.0', 'val11.0', 'val12.0', 'val13.0',
                           'val14.0']

        keys = primary_keys + secondary_keys + tertiary_keys
        values = primary_values + secondary_values + tertiary_values

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        removed_groups = obj.resize(new_capacity, transfer=True, condense=True)

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have only the new primary
        expected_num_groups = 1
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertNotEqual(obj.primary, primary)

        # we should get back the former groups, emptied of their contents
        self.assertEqual(len(removed_groups), 3)
        for group in removed_groups:
            self.assertIn(group, [primary, secondary, tertiary])
            self.assertEqual(group.size, 0)

        # check the new primary has the values taken from all old groups
        for key, value in zip(keys, values):
            self.assertTrue(obj.primary.has_key(key),
                            f'no key "{key}" in primary: {list(obj.primary.keys())}')
            self.assertTrue(obj.primary.get(key), value)

    def test_multiple_group_resize_without_transfer_or_condense_with_overlap(self):
        """
        Tests that a Container can create a new primary group and copy all
        existing primary group content into it without emptying the previous
        primary group or including any data from the secondary groups
        """
        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)
        obj = container.Container(primary, (primary, secondary, tertiary))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4', '5']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0']
        secondary_keys = ['4', '5', '6', '7', '8', '9', '10']
        secondary_values = ['val4.1', 'val5.1', 'val6.1', 'val7.1', 'val8.1',
                            'val9.1', 'val10.1']
        tertiary_keys = ['9', '10', '11', '12', '13', '14']
        tertiary_values = ['val9.2', 'val10.2', 'val11.2', 'val12.2', 'val13.2',
                           'val14.2']

        keys = primary_keys + secondary_keys[1:-1] + tertiary_keys[1:-1]
        values = primary_values + secondary_values[1:-1] + tertiary_values[1:-1]

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        removed_groups = obj.resize(new_capacity, transfer=False,
                                    condense=False)

        # should have removed nothing
        self.assertEqual(removed_groups, [])

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have all groups plus new primary
        expected_num_groups = 4
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertNotEqual(obj.primary, primary)

        # check the new primary has the values from the old primary
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.primary.has_key(key),
                            f'no key "{key}" in primary: {list(obj.primary.keys())}')
            self.assertTrue(obj.primary.get(key), value)
        # check the old primary has only its own values
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.groups[1].has_key(key))
            self.assertEqual(obj.groups[1].get(key), value)
            self.assertEqual(obj.groups[1].size, len(primary_keys))
        # check the secondary has all of its values
        for key, value in zip(secondary_keys, secondary_values):
            self.assertTrue(obj.groups[2].has_key(key))
            self.assertEqual(obj.groups[2].get(key), value)
            self.assertEqual(obj.groups[2].size, len(secondary_keys))
        # check the tertiary has all of its values
        for key, value in zip(tertiary_keys, tertiary_values):
            self.assertTrue(obj.groups[3].has_key(key))
            self.assertEqual(obj.groups[3].get(key), value)
            self.assertEqual(obj.groups[3].size, len(tertiary_keys))

    def test_multiple_group_resize_with_transfer_without_condense_with_overlap(self):
        """
        Tests that a Container can create a new primary group and copy all
        existing primary group content into it, emptying the previous primary,
        and ignoring all secondary groups
        """
        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)
        obj = container.Container(primary, (primary, secondary, tertiary))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4', '5']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0']
        secondary_keys = ['4', '5', '6', '7', '8', '9', '10']
        secondary_values = ['val4.1', 'val5.1', 'val6.1', 'val7.1', 'val8.1',
                            'val9.1', 'val10.1']
        tertiary_keys = ['9', '10', '11', '12', '13', '14']
        tertiary_values = ['val9.2', 'val10.2', 'val11.2', 'val12.2', 'val13.2',
                           'val14.2']

        keys = primary_keys + secondary_keys[1:-1] + tertiary_keys[1:-1]
        values = primary_values + secondary_values[1:-1] + tertiary_values[1:-1]

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        removed_groups = obj.resize(new_capacity, transfer=True,
                                    condense=False)

        # should have removed old primary
        self.assertEqual(removed_groups, [primary])

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have new primary and former secondaries
        expected_num_groups = 3
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertNotEqual(obj.primary, primary)

        # check the new primary has the values from the old primary
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.primary.has_key(key),
                            f'no key "{key}" in primary: {list(obj.primary.keys())}')
            self.assertTrue(obj.primary.get(key), value)
        # check the secondary has all of its values
        for key, value in zip(secondary_keys, secondary_values):
            self.assertTrue(obj.groups[1].has_key(key))
            self.assertEqual(obj.groups[1].get(key), value)
            self.assertEqual(obj.groups[1].size, len(secondary_keys))
        # check the tertiary has all of its values
        for key, value in zip(tertiary_keys, tertiary_values):
            self.assertTrue(obj.groups[2].has_key(key))
            self.assertEqual(obj.groups[2].get(key), value)
            self.assertEqual(obj.groups[2].size, len(tertiary_keys))

    def test_multiple_group_resize_without_transfer_with_condense_with_overlap(self):
        """
        Tests that a Container can create a new primary group and copy all
        existing primary and secondary group content into it, but leaves the
        previous primary and all secondary groups intact
        """
        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)
        obj = container.Container(primary, (primary, secondary, tertiary))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4', '5']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0']
        secondary_keys = ['4', '5', '6', '7', '8', '9', '10']
        secondary_values = ['val4.1', 'val5.1', 'val6.1', 'val7.1', 'val8.1',
                            'val9.1', 'val10.1']
        tertiary_keys = ['9', '10', '11', '12', '13', '14']
        tertiary_values = ['val9.2', 'val10.2', 'val11.2', 'val12.2', 'val13.2',
                           'val14.2']

        keys = primary_keys + secondary_keys[1:-1] + tertiary_keys[1:-1]
        values = primary_values + secondary_values[1:-1] + tertiary_values[1:-1]

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        removed_groups = obj.resize(new_capacity, transfer=False,
                                    condense=True)

        # should have removed nothing
        self.assertEqual(removed_groups, [])

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have all groups plus new primary
        expected_num_groups = 4
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertNotEqual(obj.primary, primary)

        # check the new primary has the values from all previous groups with
        # correct priority
        for key, value in zip(keys, values):
            self.assertTrue(obj.primary.has_key(key),
                            f'no key "{key}" in primary: {list(obj.primary.keys())}')
            self.assertTrue(obj.primary.get(key), value)
        # check the old primary has only its own values
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.groups[1].has_key(key))
            self.assertEqual(obj.groups[1].get(key), value)
            self.assertEqual(obj.groups[1].size, len(primary_keys))
        # check the secondary has all of its values
        for key, value in zip(secondary_keys, secondary_values):
            self.assertTrue(obj.groups[2].has_key(key))
            self.assertEqual(obj.groups[2].get(key), value)
            self.assertEqual(obj.groups[2].size, len(secondary_keys))
        # check the tertiary has all of its values
        for key, value in zip(tertiary_keys, tertiary_values):
            self.assertTrue(obj.groups[3].has_key(key))
            self.assertEqual(obj.groups[3].get(key), value)
            self.assertEqual(obj.groups[3].size, len(tertiary_keys))

    def test_multiple_group_resize_with_transfer_with_condense_with_overlap(self):
        """
        Test that a Container can create a new primary group and copy all
        existing primary and secondary group content into it, emptying the
        previous primary and all secondary groups and removing them from the
        group listing
        """
        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)
        obj = container.Container(primary, (primary, secondary, tertiary))

        self.assertEqual(len(primary.collections), 3)
        self.assertEqual(primary.max_size, 15000)

        primary_keys = ['0', '1', '2', '3', '4', '5']
        primary_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0']
        secondary_keys = ['4', '5', '6', '7', '8', '9', '10']
        secondary_values = ['val4.1', 'val5.1', 'val6.1', 'val7.1', 'val8.1',
                            'val9.1', 'val10.1']
        tertiary_keys = ['9', '10', '11', '12', '13', '14']
        tertiary_values = ['val9.2', 'val10.2', 'val11.2', 'val12.2', 'val13.2',
                           'val14.2']

        keys = primary_keys + secondary_keys[1:-1] + tertiary_keys[1:-1]
        values = primary_values + secondary_values[1:-1] + tertiary_values[1:-1]

        for key, value in zip(primary_keys, primary_values):
            primary.insert(key, value)
        for key, value in zip(secondary_keys, secondary_values):
            secondary.insert(key, value)
        for key, value in zip(tertiary_keys, tertiary_values):
            tertiary.insert(key, value)

        # should create 5 collections
        new_capacity = 25000
        removed_groups = obj.resize(new_capacity, transfer=True, condense=True)

        # should have removed all three prior groups
        self.assertEqual(len(removed_groups), 3)
        for group in removed_groups:
            self.assertIn(group, [primary, secondary, tertiary])

        expected_collections = 5
        self.assertEqual(obj.primary.max_size, new_capacity)
        self.assertEqual(len(obj.primary.collections), expected_collections)

        # should have all groups plus new primary
        expected_num_groups = 1
        self.assertEqual(len(obj.groups), expected_num_groups)
        self.assertNotEqual(obj.primary, primary)

        # check the new primary has the values from the old primary
        for key, value in zip(primary_keys, primary_values):
            self.assertTrue(obj.primary.has_key(key),
                            f'no key "{key}" in primary: {list(obj.primary.keys())}')
            self.assertTrue(obj.primary.get(key), value)


class ContainerPersistenceTests(TestCase):
    """
    Tests for ensuring that Container objects can be persisted to a ZODB.DB
    or DB-like object
    """
    # fsdb = filesystem database
    # memdb = in-memory database

    def setUp(self):
        # set up a temporary filesystem database
        self.temp_directory = TemporaryDirectory()
        self.temp_db_file = NamedTemporaryFile(dir=self.temp_directory.name)
        self.fs_db = DB(self.temp_db_file.name)

        # set up a memorydb
        self.memdb = DB(None)

    def tearDown(self):
        # safely close the filesystem db and cleanup the temporary directory
        self.fs_db.close()
        self.temp_db_file.close()
        self.temp_directory.cleanup()

        # close the memory db and explicitly clear it from memory
        self.memdb.close()
        del self.memdb

    def test_write_empty_container_memdb(self):
        """
        Tests that an empty container can be written to an in-memory database
        """
        # ensures primary group will be three collections with 100 max_size each
        obj = container.Container.new(capacity=300, collection_max_size=100)
        expected_capacity = 300
        expected_num_collections = 3
        expected_collection_size = 100

        # check that the object has the expected sizing
        self.assertEqual(obj.capacity, expected_capacity)
        self.assertEqual(len(obj.primary.collections), expected_num_collections)
        for collection in obj.primary.collections:
            self.assertEqual(collection.max_size, expected_collection_size)

        write_connection = self.memdb.open()
        read_connection = self.memdb.open()

        # check first that the read connection does NOT have a container
        self.assertIsNone(getattr(read_connection.root, 'container', None))

        with write_connection.transaction_manager as tm:
            write_connection.root.container = obj
            tm.commit()

        # remove obj
        write_connection.close()
        del obj

        # check that the read connection now has a container AND that the
        # container is the correct type
        loaded = getattr(read_connection.root, 'container', None)
        self.assertIsNotNone(loaded)
        self.assertIsInstance(loaded, container.Container)

        # check that the primary group has the expected sizing
        self.assertEqual(loaded.capacity, expected_capacity)
        self.assertEqual(len(loaded.primary.collections),
                         expected_num_collections)
        for collection in loaded.primary.collections:
            self.assertEqual(collection.max_size, expected_collection_size)

    def test_write_empty_container_fsdb(self):
        """
        Tests that an empty container can be written to a filesystem database
        """
        obj = container.Container.new(capacity=300, collection_max_size=100)
        expected_capacity = 300
        expected_num_collections = 3
        expected_collection_size = 100

        # check that the object has the expected sizing
        self.assertEqual(obj.capacity, expected_capacity)
        self.assertEqual(len(obj.primary.collections), expected_num_collections)
        for collection in obj.primary.collections:
            self.assertEqual(collection.max_size, expected_collection_size)

        write_connection = self.fs_db.open()
        read_connection = self.fs_db.open()

        # check first that the read connection does NOT have a container
        self.assertIsNone(getattr(read_connection.root, 'container', None))

        with write_connection.transaction_manager as tm:
            write_connection.root.container = obj
            tm.commit()

        # remove obj
        write_connection.close()
        del obj

        # check that the read connection now has a container AND that the
        # container is the correct type
        loaded = getattr(read_connection.root, 'container', None)
        self.assertIsNotNone(loaded)
        self.assertIsInstance(loaded, container.Container)

        # check that the primary group has the expected sizing
        self.assertEqual(loaded.capacity, expected_capacity)
        self.assertEqual(len(loaded.primary.collections), expected_num_collections)
        for collection in loaded.primary.collections:
            self.assertEqual(collection.max_size, expected_collection_size)

    def test_write_populated_container_memdb(self):
        """
        Tests that a container with objects can be written to an in-memory
        database
        """
        keys = ['0', '1', '2', '3', '4', '5']
        values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0', ]
        items = {k: v for k, v in zip(keys, values)}

        obj = container.Container.new(capacity=300, collection_max_size=100)

        for key, value in items.items():
            obj.write(key, value)

        write_connection = self.memdb.open()
        read_connection = self.memdb.open()

        # check first that the read connection does NOT have a container
        self.assertIsNone(getattr(read_connection.root, 'container', None))

        with write_connection.transaction_manager as tm:
            write_connection.root.container = obj
            tm.commit()

        # remove obj
        write_connection.close()
        del obj

        # check that the read connection now has a container AND that the
        # container is the correct type
        loaded = getattr(read_connection.root, 'container', None)
        self.assertIsNotNone(loaded)
        self.assertIsInstance(loaded, container.Container)

        # check that the container has all key-value pairs
        for key, value in items.items():
            self.assertTrue(loaded.has(key))
            self.assertEqual(loaded.read(key), value)

    def test_write_populated_container_fsdb(self):
        """
        Tests that a container with objects can be written to a filesystem
        database
        """
        keys = ['0', '1', '2', '3', '4', '5']
        values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',]
        items = {k: v for k, v in zip(keys, values)}

        obj = container.Container.new(capacity=300, collection_max_size=100)

        for key, value in items.items():
            obj.write(key, value)

        write_connection = self.fs_db.open()
        read_connection = self.fs_db.open()

        # check first that the read connection does NOT have a container
        self.assertIsNone(getattr(read_connection.root, 'container', None))

        with write_connection.transaction_manager as tm:
            write_connection.root.container = obj
            tm.commit()

        # remove obj
        write_connection.close()
        del obj

        # check that the read connection now has a container AND that the
        # container is the correct type
        loaded = getattr(read_connection.root, 'container', None)
        self.assertIsNotNone(loaded)
        self.assertIsInstance(loaded, container.Container)

        # check that the container has all key-value pairs
        for key, value in items.items():
            self.assertTrue(loaded.has(key))
            self.assertEqual(loaded.read(key), value)

    def test_write_and_load_empty_container_memdb(self):
        """
        Tests that an empty container can be created, saved to an in-memory
        database, loaded, written to, and saved again
        """
        keys = ['0', '1', '2', '3', '4', '5']
        values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0', 'val5.0']
        items = {k: v for k, v in zip(keys, values)}

        obj = container.Container.new(capacity=300, collection_max_size=100)

        write_connection = self.memdb.open()
        read_connection = self.memdb.open()

        # check first that the read connection does NOT have a container
        self.assertIsNone(getattr(read_connection.root, 'container', None))

        with write_connection.transaction_manager as tm:
            write_connection.root.container = obj
            tm.commit()

        # remove obj
        write_connection.close()
        del obj

        # check that the loaded collection is as empty as it was when it went in
        loaded = getattr(read_connection.root, 'container', None)
        self.assertEqual(loaded.size, 0)

        # insert the values
        write_connection = self.memdb.open()
        with write_connection.transaction_manager as tm:
            for key, value in items.items():
                loaded.write(key, value)
            tm.commit()

        # check that the object has all key-value pairs
        self.assertEqual(loaded.size, len(keys))
        for key, value in items.items():
            self.assertTrue(loaded.has(key))
            self.assertEqual(loaded.read(key), value)

        # remove obj
        write_connection.close()
        del loaded

        # reload the object and check that everything was saved
        reloaded = getattr(read_connection.root, 'container', None)
        self.assertEqual(reloaded.size, len(keys))
        for key, value in items.items():
            self.assertTrue(reloaded.has(key))
            self.assertEqual(reloaded.read(key), value)

    def test_write_and_load_empty_container_fsdb(self):
        """
        Tests that an empty container can be created, saved to a filesystem
        database, loaded, written to, and saved again
        """
        keys = ['0', '1', '2', '3', '4', '5']
        values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0', 'val5.0']
        items = {k: v for k, v in zip(keys, values)}

        obj = container.Container.new(capacity=300, collection_max_size=100)

        write_connection = self.fs_db.open()
        read_connection = self.fs_db.open()

        # check first that the read connection does NOT have a container
        self.assertIsNone(getattr(read_connection.root, 'container', None))

        with write_connection.transaction_manager as tm:
            write_connection.root.container = obj
            tm.commit()

        # remove obj
        write_connection.close()
        del obj

        # check that the loaded collection is as empty as it was when it went in
        loaded = getattr(read_connection.root, 'container', None)
        self.assertEqual(loaded.size, 0)

        # insert the values
        write_connection = self.fs_db.open()
        with write_connection.transaction_manager as tm:
            for key, value in items.items():
                loaded.write(key, value)
            tm.commit()

        # check that the object has all key-value pairs
        self.assertEqual(loaded.size, len(keys))
        for key, value in items.items():
            self.assertTrue(loaded.has(key))
            self.assertEqual(loaded.read(key), value)

        # remove obj
        write_connection.close()
        del loaded

        # reload the object and check that everything was saved
        loaded = getattr(read_connection.root, 'container', None)
        self.assertEqual(loaded.size, len(keys))
        for key, value in items.items():
            self.assertTrue(loaded.has(key))
            self.assertEqual(loaded.read(key), value)

    def test_write_and_load_populated_container_memdb(self):
        """
        Tests that a container with objects can be created, saved to an
        in-memory database, loaded, written to, and saved again
        """
        initial_keys = ['0', '1', '2', '3', '4', '5']
        initial_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0']
        initial_items = {k: v for k, v in zip(initial_keys, initial_values)}
        added_keys = ['6', '7', '8', '9', '10', '11']
        added_values = ['val6.0', 'val7.0', 'val8.0', 'val9.0', 'val10.0',
                        'val11.0']
        added_items = {k: v for k, v in zip(added_keys, added_values)}

        all_keys = initial_keys + added_keys
        all_values = initial_values + added_values
        all_items = {k: v for k, v in zip(all_keys, all_values)}

        obj = container.Container.new(capacity=300, collection_max_size=100)

        for key, value in initial_items.items():
            obj.write(key, value)

        write_connection = self.memdb.open()
        read_connection = self.memdb.open()

        # check first that the read connection does NOT have a container
        self.assertIsNone(getattr(read_connection.root, 'container', None))

        with write_connection.transaction_manager as tm:
            write_connection.root.container = obj
            tm.commit()

        # remove obj
        write_connection.close()
        del obj

        # check that the loaded collection is as empty as it was when it went in
        loaded = getattr(read_connection.root, 'container', None)
        self.assertEqual(loaded.size, len(initial_keys))

        # check that the object has the initial set of values
        self.assertEqual(loaded.size, len(initial_keys))
        for key, value in initial_items.items():
            self.assertTrue(loaded.has(key))
            self.assertEqual(loaded.read(key), value)

        # insert the second set of values
        write_connection = self.memdb.open()
        with write_connection.transaction_manager as tm:
            for key, value in added_items.items():
                loaded.write(key, value)
            tm.commit()

        # check that the object has all key-value pairs
        self.assertEqual(loaded.size, len(all_keys))
        for key, value in all_items.items():
            self.assertTrue(loaded.has(key))
            self.assertEqual(loaded.read(key), value)

        # remove obj
        write_connection.close()
        del loaded

        # reload the object and check that everything was saved
        reloaded = getattr(read_connection.root, 'container', None)
        self.assertEqual(reloaded.size, len(all_keys))
        for key, value in all_items.items():
            self.assertTrue(reloaded.has(key))
            self.assertEqual(reloaded.read(key), value)

    def test_write_and_load_populated_container_fsdb(self):
        """
        Tests that a container with objects can be created, saved to a
        filesystem database, loaded, written to, and saved again
        """
        initial_keys = ['0', '1', '2', '3', '4', '5']
        initial_values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0']
        initial_items = {k: v for k, v in zip(initial_keys, initial_values)}
        added_keys = ['6', '7', '8', '9', '10', '11']
        added_values = ['val6.0', 'val7.0', 'val8.0', 'val9.0', 'val10.0',
                        'val11.0']
        added_items = {k: v for k, v in zip(added_keys, added_values)}

        all_keys = initial_keys + added_keys
        all_values = initial_values + added_values
        all_items = {k: v for k, v in zip(all_keys, all_values)}

        obj = container.Container.new(capacity=300, collection_max_size=100)

        for key, value in initial_items.items():
            obj.write(key, value)

        write_connection = self.fs_db.open()
        read_connection = self.fs_db.open()

        # check first that the read connection does NOT have a container
        self.assertIsNone(getattr(read_connection.root, 'container', None))

        with write_connection.transaction_manager as tm:
            write_connection.root.container = obj
            tm.commit()

        # remove obj
        write_connection.close()
        del obj

        # check that the loaded collection is as empty as it was when it went in
        loaded = getattr(read_connection.root, 'container', None)
        self.assertEqual(loaded.size, len(initial_keys))

        # check that the object has the initial set of values
        self.assertEqual(loaded.size, len(initial_keys))
        for key, value in initial_items.items():
            self.assertTrue(loaded.has(key))
            self.assertEqual(loaded.read(key), value)

        # insert the second set of values
        write_connection = self.fs_db.open()
        with write_connection.transaction_manager as tm:
            for key, value in added_items.items():
                loaded.write(key, value)
            tm.commit()

        # check that the object has all key-value pairs
        self.assertEqual(loaded.size, len(all_keys))
        for key, value in all_items.items():
            self.assertTrue(loaded.has(key))
            self.assertEqual(loaded.read(key), value)

        # remove obj
        write_connection.close()
        del loaded

        # reload the object and check that everything was saved
        reloaded = getattr(read_connection.root, 'container', None)
        self.assertEqual(reloaded.size, len(all_keys))
        for key, value in all_items.items():
            self.assertTrue(reloaded.has(key))
            self.assertEqual(reloaded.read(key), value)

    def test_delete_from_populated_container_memdb(self):
        """
        Tests that a container with objects can be loaded from an in-memory
        database, have objects deleted from it, and be saved again
        """
        keys = ['0', '1', '2', '3', '4', '5']
        values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0', 'val5.0']
        items = {k: v for k, v in zip(keys, values)}

        selected_key = '2'
        expected_keys = ['0', '1', '3', '4', '5']
        expected_values = ['val0.0', 'val1.0', 'val3.0', 'val4.0', 'val5.0']
        expected_items = {k: v for k, v in zip(expected_keys, expected_values)}

        obj = container.Container.new(capacity=300, collection_max_size=100)

        for key, value in items.items():
            obj.write(key, value)

        write_connection = self.memdb.open()
        read_connection = self.memdb.open()

        # check first that the read connection does NOT have a container
        self.assertIsNone(getattr(read_connection.root, 'container', None))

        with write_connection.transaction_manager as tm:
            write_connection.root.container = obj
            tm.commit()

        # remove obj
        write_connection.close()
        del obj

        # check that the read connection now has a container AND that the
        # container is the correct type
        loaded = getattr(read_connection.root, 'container', None)
        write_connection = self.memdb.open()

        # delete a key
        with write_connection.transaction_manager as tm:
            loaded.delete(selected_key)

        # test that object in memory has had the key removed
        self.assertEqual(loaded.size, len(expected_keys))
        self.assertFalse(loaded.has(selected_key))
        for key, value in expected_items.items():
            self.assertTrue(loaded.has(key))
            self.assertEqual(loaded.read(key), value)

        # reload the object from the db
        write_connection.close()
        del loaded

        # check that the reloaded object has the expected values
        reloaded = getattr(read_connection.root, 'container', None)
        self.assertEqual(reloaded.size, len(expected_keys))
        for key, value in expected_items.items():
            self.assertTrue(reloaded.has(key))
            self.assertEqual(reloaded.read(key), value)

    def test_delete_from_populated_container_fsdb(self):
        """
        Tests that a container with objects can be loaded from a filesystem
        database, have objects deleted from it, and be saved again
        """
        keys = ['0', '1', '2', '3', '4', '5']
        values = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0', 'val5.0']
        items = {k: v for k, v in zip(keys, values)}

        selected_key = '2'
        expected_keys = ['0', '1', '3', '4', '5']
        expected_values = ['val0.0', 'val1.0', 'val3.0', 'val4.0', 'val5.0']
        expected_items = {k: v for k, v in zip(expected_keys, expected_values)}

        obj = container.Container.new(capacity=300, collection_max_size=100)

        for key, value in items.items():
            obj.write(key, value)

        write_connection = self.fs_db.open()
        read_connection = self.fs_db.open()

        # check first that the read connection does NOT have a container
        self.assertIsNone(getattr(read_connection.root, 'container', None))

        with write_connection.transaction_manager as tm:
            write_connection.root.container = obj
            tm.commit()

        # remove obj
        write_connection.close()
        del obj

        # check that the read connection now has a container AND that the
        # container is the correct type
        loaded = getattr(read_connection.root, 'container', None)
        write_connection = self.fs_db.open()

        # delete a key
        with write_connection.transaction_manager as tm:
            loaded.delete(selected_key)

        # test that object in memory has had the key removed
        self.assertEqual(loaded.size, len(expected_keys))
        self.assertFalse(loaded.has(selected_key))
        for key, value in expected_items.items():
            self.assertTrue(loaded.has(key))
            self.assertEqual(loaded.read(key), value)

        # reload the object from the db
        write_connection.close()
        del loaded

        # check that the reloaded object has the expected values
        reloaded = getattr(read_connection.root, 'container', None)
        self.assertEqual(reloaded.size, len(expected_keys))
        for key, value in expected_items.items():
            self.assertTrue(reloaded.has(key))
            self.assertEqual(reloaded.read(key), value)

    def test_transaction_manager_for_condense_one_secondary_no_transfer(self):
        """
        Tests that a container with a single secondary group can use a
        transaction manager for moving each object during a condense operation
        """
        keys0 = ['0', '1', '2', '3', '4', '5']
        values0 = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0']
        items0 = {k: v for k, v in zip(keys0, values0)}

        keys1 = ['6', '7', '8', '9', '10', '11']
        values1 = ['val6.1', 'val7.1', 'val8.1', 'val9.1', 'val10.1',
                        'val11.1']
        items1 = {k: v for k, v in zip(keys1, values1)}

        keys = keys0+keys1
        values = values0 + values1
        items = {k: v for k, v in zip(keys, values)}

        primary = Group.new(3)
        secondary = Group.new(3)

        for key, value in items0.items():
            primary.insert(key, value)
        for key, value in items1.items():
            secondary.insert(key, value)

        obj = container.Container(primary_group=primary,
                                  groups=(primary, secondary))

        transaction_mock = MagicMock()

        # test when transfer is False (keep groups)
        obj.condense(transfer=False, transaction_manager=transaction_mock)

        # commit on every key transfer plus the primary group change
        expected_num_calls = len(keys1)
        self.assertEqual(
            transaction_mock.__enter__.return_value.commit.call_count,
            expected_num_calls,
            f'Called {transaction_mock.__enter__.return_value.commit.call_count} times; ' +
            f'expected {expected_num_calls}'
        )

        # check that all values are found
        for key, value in items.items():
            self.assertTrue(obj.has(key))
            self.assertEqual(obj.read(key), value)

    def test_transaction_manager_for_condense_one_secondary_with_transfer(self):
        """
        Tests that a container with a single secondary group can use a
        transaction manager for moving each object during a condense operation
        """
        keys0 = ['0', '1', '2', '3', '4', '5']
        values0 = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                          'val5.0']
        items0 = {k: v for k, v in zip(keys0, values0)}

        keys1 = ['6', '7', '8', '9', '10', '11']
        values1 = ['val6.1', 'val7.1', 'val8.1', 'val9.1', 'val10.1',
                        'val11.1']
        items1 = {k: v for k, v in zip(keys1, values1)}

        keys = keys0+keys1
        values = values0 + values1
        items = {k: v for k, v in zip(keys, values)}

        primary = Group.new(3)
        secondary = Group.new(3)

        for key, value in items0.items():
            primary.insert(key, value)
        for key, value in items1.items():
            secondary.insert(key, value)

        obj = container.Container(primary_group=primary,
                                  groups=(primary, secondary))

        transaction_mock = MagicMock()

        # test when transfer is True (remove groups)
        obj.condense(transfer=True, transaction_manager=transaction_mock)

        # commit on every key transfer plus the primary group change
        expected_num_calls = len(keys1) + 1
        self.assertEqual(
            transaction_mock.__enter__.return_value.commit.call_count,
            expected_num_calls,
            f'Called {transaction_mock.__enter__.return_value.commit.call_count} times; ' +
            f'expected {expected_num_calls}'
        )

        # check that all values are found
        for key, value in items.items():
            self.assertTrue(obj.has(key))
            self.assertEqual(obj.read(key), value)

    def test_transaction_manager_for_condense_multiple_secondary_no_transfer(self):
        """
        Tests that a container with multiple secondary groups can use a
        transaction manager for moving each object during a condense operation
        """
        keys0 = ['0', '1', '2', '3', '4', '5']
        values0 = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                   'val5.0']
        items0 = {k: v for k, v in zip(keys0, values0)}

        keys1 = ['6', '7', '8', '9', '10', '11']
        values1 = ['val6.1', 'val7.1', 'val8.1', 'val9.1', 'val10.1',
                   'val11.1']
        items1 = {k: v for k, v in zip(keys1, values1)}

        keys2 = ['12', '13', '14', '15', '16', '17']
        values2 = ['val12.2', 'val13.2', 'val14.2', 'val15.2', 'val16.2',
                   'val17.2']
        items2 = {k: v for k, v in zip(keys2, values2)}

        keys = keys0 + keys1 + keys2
        values = values0 + values1 + values2
        items = {k: v for k, v in zip(keys, values)}

        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)

        for key, value in items0.items():
            primary.insert(key, value)
        for key, value in items1.items():
            secondary.insert(key, value)
        for key, value in items2.items():
            tertiary.insert(key, value)

        obj = container.Container(primary_group=primary,
                                  groups=(primary, secondary, tertiary))

        transaction_mock = MagicMock()

        # test when transfer is False (keep groups)
        obj.condense(transfer=False, transaction_manager=transaction_mock)

        # commit on every key transfer plus the primary group change
        expected_num_calls = len(keys1 + keys2)
        self.assertEqual(
            transaction_mock.__enter__.return_value.commit.call_count,
            expected_num_calls,
            f'Called {transaction_mock.__enter__.return_value.commit.call_count} times; ' +
            f'expected {expected_num_calls}'
        )

        # check that all values are found
        for key, value in items.items():
            self.assertTrue(obj.has(key))
            self.assertEqual(obj.read(key), value)

    def test_transaction_manager_for_condense_multiple_secondary_with_transfer(self):
        """
        Tests that a container with multiple secondary groups can use a
        transaction manager for moving each object during a condense operation
        """
        keys0 = ['0', '1', '2', '3', '4', '5']
        values0 = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                   'val5.0']
        items0 = {k: v for k, v in zip(keys0, values0)}

        keys1 = ['6', '7', '8', '9', '10', '11']
        values1 = ['val6.1', 'val7.1', 'val8.1', 'val9.1', 'val10.1',
                   'val11.1']
        items1 = {k: v for k, v in zip(keys1, values1)}

        keys2 = ['12', '13', '14', '15', '16', '17']
        values2 = ['val12.2', 'val13.2', 'val14.2', 'val15.2', 'val16.2',
                   'val17.2']
        items2 = {k: v for k, v in zip(keys2, values2)}

        keys = keys0 + keys1 + keys2
        values = values0 + values1 + values2
        items = {k: v for k, v in zip(keys, values)}

        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)

        for key, value in items0.items():
            primary.insert(key, value)
        for key, value in items1.items():
            secondary.insert(key, value)
        for key, value in items2.items():
            tertiary.insert(key, value)

        obj = container.Container(primary_group=primary,
                                  groups=(primary, secondary, tertiary))

        transaction_mock = MagicMock()

        # test when transfer is True (remove groups)
        obj.condense(transfer=True, transaction_manager=transaction_mock)

        # commit on every key transfer plus the primary group change
        expected_num_calls = len(keys1 + keys2) + 1
        self.assertEqual(
            transaction_mock.__enter__.return_value.commit.call_count,
            expected_num_calls,
            f'Called {transaction_mock.__enter__.return_value.commit.call_count} times; ' +
            f'expected {expected_num_calls}'
        )

        # check that all values are found
        for key, value in items.items():
            self.assertTrue(obj.has(key))
            self.assertEqual(obj.read(key), value)

    def test_transaction_manager_for_resize_no_secondary_no_transfer(self):
        """
        Tests that a container with no secondary groups can use a transaction
        manager for moving each object during a resize operation
        """
        keys0 = ['0', '1', '2', '3', '4', '5']
        values0 = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                   'val5.0']
        items0 = {k: v for k, v in zip(keys0, values0)}

        keys = keys0
        values = values0
        items = {k: v for k, v in zip(keys, values)}

        primary = Group.new(3)

        for key, value in items0.items():
            primary.insert(key, value)

        obj = container.Container(primary_group=primary,
                                  groups=(primary,))

        transaction_mock = MagicMock()

        # test when transfer is False (keep groups) and condense is True
        obj.resize(capacity=300, max_collection_size=100,
                   transfer=False, condense=True,
                   transaction_manager=transaction_mock)
        # commit on every key transfer plus the primary group change
        expected_num_calls = len(keys0) + 1
        self.assertEqual(
            transaction_mock.__enter__.return_value.commit.call_count,
            expected_num_calls,
            f'Called {transaction_mock.__enter__.return_value.commit.call_count} times; ' +
            f'expected {expected_num_calls}'
        )

        # check that all values are found
        for key, value in items.items():
            self.assertTrue(obj.has(key))
            self.assertEqual(obj.read(key), value)

    def test_transaction_manager_for_resize_no_secondary_with_transfer(self):
        """
        Tests that a container with no secondary groups can use a transaction
        manager for moving each object during a resize operation
        """
        keys0 = ['0', '1', '2', '3', '4', '5']
        values0 = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                   'val5.0']
        items0 = {k: v for k, v in zip(keys0, values0)}

        keys = keys0
        values = values0
        items = {k: v for k, v in zip(keys, values)}

        primary = Group.new(3)

        for key, value in items0.items():
            primary.insert(key, value)

        obj = container.Container(primary_group=primary,
                                  groups=(primary,))

        transaction_mock = MagicMock()

        # test when transfer is False (keep groups) and condense is True
        obj.resize(capacity=300, max_collection_size=100,
                   transfer=True, condense=True,
                   transaction_manager=transaction_mock)
        # commit on every key transfer plus the primary group change plus the
        # removal of non-primary groups
        expected_num_calls = len(keys0) + 2
        self.assertEqual(
            transaction_mock.__enter__.return_value.commit.call_count,
            expected_num_calls,
            f'Called {transaction_mock.__enter__.return_value.commit.call_count} times; ' +
            f'expected {expected_num_calls}'
        )

        # check that all values are found
        for key, value in items.items():
            self.assertTrue(obj.has(key))
            self.assertEqual(obj.read(key), value)

    def test_transaction_manager_for_resize_one_secondary_no_transfer(self):
        """
        Tests that a container with no secondary groups can use a transaction
        manager for moving each object during a resize operation
        """
        keys0 = ['0', '1', '2', '3', '4', '5']
        values0 = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                   'val5.0']
        items0 = {k: v for k, v in zip(keys0, values0)}

        keys1 = ['6', '7', '8', '9', '10', '11']
        values1 = ['val6.1', 'val7.1', 'val8.1', 'val9.1', 'val10.1',
                   'val11.1']
        items1 = {k: v for k, v in zip(keys1, values1)}

        keys = keys0 + keys1
        values = values0 + values1
        items = {k: v for k, v in zip(keys, values)}

        primary = Group.new(3)
        secondary = Group.new(3)

        for key, value in items0.items():
            primary.insert(key, value)
        for key, value in items1.items():
            secondary.insert(key, value)

        obj = container.Container(primary_group=primary,
                                  groups=(primary, secondary))

        transaction_mock = MagicMock()

        # test when transfer is False (keep groups) and condense is True
        obj.resize(capacity=300, max_collection_size=100,
                   transfer=False, condense=True,
                   transaction_manager=transaction_mock)
        # commit on every key transfer plus the primary group change
        self.assertEqual(
            transaction_mock.__enter__.return_value.commit.call_count,
            len(keys0) + len(keys1) + 1,
            f'Called {transaction_mock.__enter__.return_value.commit.call_count} times; ' +
            f'expected {len(keys0) + len(keys1) + 1}'
        )

        # check that all values are found
        for key, value in items.items():
            self.assertTrue(obj.has(key))
            self.assertEqual(obj.read(key), value)

    def test_transaction_manager_for_resize_one_secondary_with_transfer(self):
        """
        Tests that a container with one secondary group can use a transaction
        manager for moving each object during a resize operation
        """
        keys0 = ['0', '1', '2', '3', '4', '5']
        values0 = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                   'val5.0']
        items0 = {k: v for k, v in zip(keys0, values0)}

        keys1 = ['6', '7', '8', '9', '10', '11']
        values1 = ['val6.1', 'val7.1', 'val8.1', 'val9.1', 'val10.1',
                   'val11.1']
        items1 = {k: v for k, v in zip(keys1, values1)}

        keys = keys0 + keys1
        values = values0 + values1
        items = {k: v for k, v in zip(keys, values)}

        primary = Group.new(3)
        secondary = Group.new(3)

        for key, value in items0.items():
            primary.insert(key, value)
        for key, value in items1.items():
            secondary.insert(key, value)

        obj = container.Container(primary_group=primary,
                                  groups=(primary, secondary))

        transaction_mock = MagicMock()

        # test when transfer is True (remove groups) and condense is True
        obj.resize(capacity=300, max_collection_size=100,
                   transfer=True, condense=True,
                   transaction_manager=transaction_mock)

        # commit on every key transfer plus the primary group change
        expected_num_calls = len(keys0 + keys1) + 2
        self.assertEqual(
            transaction_mock.__enter__.return_value.commit.call_count,
            expected_num_calls,
            f'Called {transaction_mock.__enter__.return_value.commit.call_count} times; ' +
            f'expected {expected_num_calls}'
        )

        # check that all values are found
        for key, value in items.items():
            self.assertTrue(obj.has(key))
            self.assertEqual(obj.read(key), value)

    def test_transaction_manager_for_resize_multiple_secondary_no_transfer(self):
        """
        Tests that a container with multiple secondary groups can use a
        transaction manager for moving each object during a resize operation
        """
        keys0 = ['0', '1', '2', '3', '4', '5']
        values0 = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                   'val5.0']
        items0 = {k: v for k, v in zip(keys0, values0)}

        keys1 = ['6', '7', '8', '9', '10', '11']
        values1 = ['val6.1', 'val7.1', 'val8.1', 'val9.1', 'val10.1',
                   'val11.1']
        items1 = {k: v for k, v in zip(keys1, values1)}

        keys2 = ['12', '13', '14', '15', '16', '17']
        values2 = ['val12.2', 'val13.2', 'val14.2', 'val15.2', 'val16.2',
                   'val17.2']
        items2 = {k: v for k, v in zip(keys2, values2)}

        keys = keys0 + keys1 + keys2
        values = values0 + values1 + values2
        items = {k: v for k, v in zip(keys, values)}

        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)

        for key, value in items0.items():
            primary.insert(key, value)
        for key, value in items1.items():
            secondary.insert(key, value)
        for key, value in items2.items():
            tertiary.insert(key, value)

        obj = container.Container(primary_group=primary,
                                  groups=(primary, secondary, tertiary))

        transaction_mock = MagicMock()

        # test when transfer is False (keep groups) and condense is True
        obj.resize(capacity=300, max_collection_size=100,
                   transfer=False, condense=True,
                   transaction_manager=transaction_mock)

        # commit on every key transfer plus the primary group change
        expected_num_calls = len(keys0 + keys1 + keys2) + 1
        self.assertEqual(
            transaction_mock.__enter__.return_value.commit.call_count,
            expected_num_calls,
            f'Called {transaction_mock.__enter__.return_value.commit.call_count} times; ' +
            f'expected {expected_num_calls}'
        )

        # check that all values are found
        for key, value in items.items():
            self.assertTrue(obj.has(key))
            self.assertEqual(obj.read(key), value)

    def test_transaction_manager_for_resize_multiple_secondary_with_transfer(self):
        """
        Tests that a container with multiple secondary groups can use a
        transaction manager for moving each object during a resize operation
        """
        keys0 = ['0', '1', '2', '3', '4', '5']
        values0 = ['val0.0', 'val1.0', 'val2.0', 'val3.0', 'val4.0',
                   'val5.0']
        items0 = {k: v for k, v in zip(keys0, values0)}

        keys1 = ['6', '7', '8', '9', '10', '11']
        values1 = ['val6.1', 'val7.1', 'val8.1', 'val9.1', 'val10.1',
                   'val11.1']
        items1 = {k: v for k, v in zip(keys1, values1)}

        keys2 = ['12', '13', '14', '15', '16', '17']
        values2 = ['val12.2', 'val13.2', 'val14.2', 'val15.2', 'val16.2',
                   'val17.2']
        items2 = {k: v for k, v in zip(keys2, values2)}

        keys = keys0 + keys1 + keys2
        values = values0 + values1 + values2
        items = {k: v for k, v in zip(keys, values)}

        primary = Group.new(3)
        secondary = Group.new(3)
        tertiary = Group.new(3)

        for key, value in items0.items():
            primary.insert(key, value)
        for key, value in items1.items():
            secondary.insert(key, value)
        for key, value in items2.items():
            tertiary.insert(key, value)

        obj = container.Container(primary_group=primary,
                                  groups=(primary, secondary, tertiary))

        transaction_mock = MagicMock()

        # test when transfer is True (remove groups) and condense is True
        obj.resize(capacity=300, max_collection_size=100,
                   transfer=True, condense=True,
                   transaction_manager=transaction_mock)

        # commit on every key transfer plus the primary group change plus the
        # removal of non-primary groups
        expected_num_calls = len(keys0 + keys1 + keys2) + 2
        self.assertEqual(
            transaction_mock.__enter__.return_value.commit.call_count,
            expected_num_calls,
            f'Called {transaction_mock.__enter__.return_value.commit.call_count} times; ' +
            f'expected {expected_num_calls}'
        )

        # check that all values are found
        for key, value in items.items():
            self.assertTrue(obj.has(key))
            self.assertEqual(obj.read(key), value)


if __name__ == '__main__':
    main()

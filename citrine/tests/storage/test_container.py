from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from uuid import uuid4

from ZODB import DB

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


class ContainerInternalResizeTests(TestCase):
    """
    Tests that a Container can manually and automatically resize its internal
    group in-place.
    """


if __name__ == '__main__':
    main()

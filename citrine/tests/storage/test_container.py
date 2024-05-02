from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from uuid import uuid4

from ZODB import DB

from citrine.storage import container

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
        mock_container.groups = (primary, MagicMock(size=10), MagicMock(size=10))

        meta = container.ContainerMeta(mock_container)
        self.assertEqual(meta.size, 20)

        # test against multiple groups, all w/ items
        mock_container = MagicMock()
        primary = MagicMock(size=10)
        mock_container.primary = primary
        mock_container.groups = (primary, MagicMock(size=10), MagicMock(size=10))

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
        self.assertEqual(int(meta.usage*100), 55)

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
        obj = container.Container(groups, primary)

        self.assertEqual(metamock.return_value, obj.meta)

    def test_primary(self):
        """
        Tests that the ``primary`` property will return the primary group
        """
        # test when primary is only group
        primary = MagicMock()
        groups = (primary,)
        obj = container.Container(groups, primary)

        self.assertEqual(primary, obj.primary)

        # test when multiple groups are present
        primary = MagicMock()
        groups = (primary, MagicMock(max_size=20), MagicMock(max_size=30))
        obj = container.Container(groups, primary)

        self.assertEqual(primary, obj.primary)

    def test_groups(self):
        """
        Tests that the ``groups`` property will return the groups iterable
        """
        # test when primary is only group
        primary = MagicMock()
        groups = (primary,)
        obj = container.Container(groups, primary)

        self.assertEqual(groups, obj.groups)

        # test when multiple groups are present
        primary = MagicMock()
        groups = (primary, MagicMock(max_size=20), MagicMock(max_size=30))
        obj = container.Container(groups, primary)

        self.assertEqual(groups, obj.groups)

    def test_size(self):
        """
        Tests that the ``size`` property will return the number of items
        in all groups
        """
        # test when primary is only group and empty
        primary = MagicMock(size=0)
        groups = (primary,)
        obj = container.Container(groups, primary)

        expected = 0
        self.assertEqual(obj.size, expected)

        # test when primary is only group and has items
        primary = MagicMock(size=10)
        groups = (primary,)
        obj = container.Container(groups, primary)

        expected = 10
        self.assertEqual(obj.size, expected)

        # test with multiple groups; all empty
        primary = MagicMock(size=0)
        groups = (primary, MagicMock(size=0), MagicMock(size=0))
        obj = container.Container(groups, primary)

        expected = 0
        self.assertEqual(obj.size, expected)

        # test with multiple groups; only primary has items
        primary = MagicMock(size=5)
        groups = (primary, MagicMock(size=0), MagicMock(size=0))
        obj = container.Container(groups, primary)

        expected = 5
        self.assertEqual(obj.size, expected)

        # test with multiple groups; only secondary have items
        primary = MagicMock(size=0)
        groups = (primary, MagicMock(size=5), MagicMock(size=10))
        obj = container.Container(groups, primary)

        expected = 15
        self.assertEqual(obj.size, expected)

        # test with multiple groups; primary and secondary have items
        primary = MagicMock(size=5)
        groups = (primary, MagicMock(size=5), MagicMock(size=10))
        obj = container.Container(groups, primary)

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
        obj = container.Container(groups, primary)

        expected = 5
        self.assertEqual(obj.max_size, expected)

        # test with multiple groups; all same size
        primary = MagicMock(max_size=5)
        groups = (primary, MagicMock(max_size=5), MagicMock(max_size=5))
        obj = container.Container(groups, primary)

        expected = 15
        self.assertEqual(obj.max_size, expected)

        # test with multiple groups; different sizes
        primary = MagicMock(max_size=5)
        groups = (primary, MagicMock(max_size=10), MagicMock(max_size=15))
        obj = container.Container(groups, primary)

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
        obj = container.Container(groups, primary)

        expected = 5
        self.assertEqual(obj.used, expected)

        # test with multiple groups; all same used
        primary = MagicMock(size=10)
        groups = (primary, MagicMock(size=10), MagicMock(size=10))
        obj = container.Container(groups, primary)

        expected = 10
        self.assertEqual(obj.used, expected)

        # test with multiple groups; different used
        primary = MagicMock(size=15)
        groups = (primary, MagicMock(size=18), MagicMock(size=25))
        obj = container.Container(groups, primary)

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
        obj = container.Container(groups, primary)

        expected = 35
        self.assertEqual(int(obj.usage*100), expected)

        # test with multiple groups; all same usage rate
        primary = MagicMock(usage=.24)
        groups = (primary, MagicMock(usage=.11), MagicMock(usage=.80))
        obj = container.Container(groups, primary)

        expected = 24
        self.assertEqual(int(obj.usage*100), expected)

        # test with multiple groups; different usage rates
        primary = MagicMock(usage=.55)
        groups = (primary, MagicMock(usage=.65), MagicMock(usage=.14))
        obj = container.Container(groups, primary)

        expected = 55
        self.assertEqual(int(obj.usage*100), expected)

    def test_status(self):
        """
        Tests that the ``status`` property will return the status of the primary
        group
        """
        # test when primary is only group
        primary = MagicMock(status=HEALTHY)
        groups = (primary,)
        obj = container.Container(groups, primary)

        expected = HEALTHY
        self.assertEqual(obj.status, expected)

        # test with multiple groups; all same status
        primary = MagicMock(status=WARNING)
        groups = (primary, MagicMock(status=WARNING), MagicMock(status=WARNING))
        obj = container.Container(groups, primary)

        expected = WARNING
        self.assertEqual(obj.status, expected)

        # test with multiple groups; different statuses
        primary = MagicMock(status=CRITICAL)
        groups = (primary, MagicMock(status=ALERT), MagicMock(status=HEALTHY))
        obj = container.Container(groups, primary)

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
        obj = container.Container(groups, primary)

        self.assertFalse(obj.strict)

        primary.strict = True
        self.assertTrue(obj.strict)

        # test with multiple groups; different strictnesses
        primary = MagicMock(strict=False)
        secondary0 = MagicMock(strict=False)
        groups = (primary, secondary0, MagicMock(strict=False))
        obj = container.Container(groups, primary)

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

    def test_sets_all_groups(self):
        """
        Tests that the default init will add one or more groups to the
        ``groups`` property in the order they were provided in
        """

    def test_sets_strictness(self):
        """
        Tests that the default init will set the ``strict`` property correctly
        """

    def test_new_default_constructors(self):
        """
        Tests that ``Container.new`` creates a container with the correct
        sizing and groups with the default parameters.
        """

    def test_new_custom_capacity(self):
        """
        Tests that ``Container.new`` creates a container with a provided
        ``capacity`` parameter and the default ``collection_max_size``
        """

    def test_new_custom_collection_max_size(self):
        """
        Tests that ``Container.new`` creates a container with a provided
        ``collection_max_size`` parameter and the default ``capacity``
        """

    def test_new_custom_capacity_and_collection_max_size(self):
        """
        Tests that ``Container.new`` creates a container with provided
        ``capacity`` and ``collection_max_size`` parameters
        """

    def test_new_custom_strict(self):
        """
        Tests that ``Container.new`` creates a container with a provided
        ``strict`` parameter
        """


class ContainerReadWriteTests(TestCase):
    """
    Tests that a Container can use the standard ``read``, ``write``, ``has``,
    and ``delete`` methods for reading and writing to the internal group.
    """


class ContainerInternalResizeTests(TestCase):
    """
    Tests that a Container can manually and automatically resize its internal
    group in-place.
    """


if __name__ == '__main__':
    main()

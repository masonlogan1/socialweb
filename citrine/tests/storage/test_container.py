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


class ContainerConstructorTests(TestCase):
    """
    Tests that a Container can be constructed either by passing in an
    existing group or through the use of ``Container.new`` to automatically
    generate an internal group prepared for a certain initial capacity.
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

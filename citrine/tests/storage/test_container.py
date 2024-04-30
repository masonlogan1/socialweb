from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from uuid import uuid4

from ZODB import DB

from citrine.storage import container


class ContainerMetaTests(TestCase):
    """
    Tests that a Container's metadata is a reflection of the groups stored
    inside.
    """


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

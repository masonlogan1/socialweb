from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from uuid import uuid4

from ZODB import DB

from citrine.storage import collection as container


class GroupMetaTests(TestCase):
    """
    Test cases for citrine.storage.group.GroupMeta that ensure a GroupMeta
    object combines the metadata information from the group's component parts
    """


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


class GroupStorageTests(TestCase):
    """
    Test cases for citrine.storage.group.Group that ensure the standard
    Collection interface is distributed across multiple collections without
    manual intervention
    """


if __name__ == '__main__':
    main()

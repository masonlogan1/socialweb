from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from uuid import uuid4

from ZODB import DB

from citrine.storage import container


class TestObject:
    """
    Generic class for testing storage with
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class CollectionTests(TestCase):
    """
    Tests for the citrine.storage.container.Collection class
    """

    def setUp(self):
        self.memdb = DB(None)
        self.connection = self.memdb.open()

    def tearDown(self):
        self.connection.close()
        self.memdb.close()
        self.memdb = None

    def test_accepts_uuid_value(self):
        """
        Test that a Collection object will take an assigned UUID value
        """
        prepared_uuid = '108002d1-1568-4ac2-9944-db08cfa708ff'
        collection = container.Collection(uuid=prepared_uuid)

        self.assertEqual(prepared_uuid, collection.uuid)

    @patch.object(container, 'uuid4',
                  return_value='108002d1-1568-4ac2-9944-db08cfa708ff')
    def test_generates_new_uuid_value(self, mock_uuid4):
        """
        Tests that a Collection object will assign itself a UUID value if one
        is not provided. Also ensures that the uuid4 function is used
        """
        expected_uuid = '108002d1-1568-4ac2-9944-db08cfa708ff'
        collection = container.Collection()

        self.assertEqual(expected_uuid, collection.uuid)

    def test_persistent_uuid(self):
        """
        Tests that a Collection's uuid value will be kept after storing it
        :return:
        """
        prepared_uuid = '108002d1-1568-4ac2-9944-db08cfa708ff'
        collection = container.Collection(uuid=prepared_uuid)

        with self.connection.transaction_manager as tm:
            self.connection.root.test_object = collection
            tm.commit()

        self.assertEqual(prepared_uuid, self.connection.root.test_object.uuid)

    def test_access_stored_values(self):
        """
        Tests that a Collection's values can be stored with the OOBTree
        ``insert`` method and accessed using the OOBTree ``get`` method
        :return:
        """
        prepared_uuid = '108002d1-1568-4ac2-9944-db08cfa708ff'
        collection = container.Collection(uuid=prepared_uuid)

        objects = {num: TestObject(id='_'+str(uuid4()).replace('-', '_'), num=num) for num in range(10)}

        for value in objects.values():
            collection.insert(value.id, value)

        for key, value in objects.items():
            self.assertEqual(collection.get(value.id).num, key)

    def test_access_stored_values_as_attributes(self):
        """
        Tests that a Collection's values can be accessed when the key is treated
        like an attribute of the collection
        :return:
        """
        prepared_uuid = '108002d1-1568-4ac2-9944-db08cfa708ff'
        collection = container.Collection(uuid=prepared_uuid)

        objects = {num: TestObject(id='_'+str(uuid4()).replace('-', '_'), num=num) for num in range(10)}

        for value in objects.values():
            collection.insert(value.id, value)

        for key, value in objects.items():
            self.assertEqual(getattr(collection, value.id).num, key)

    def test_access_stored_values_after_persisting(self):
        prepared_uuid = '108002d1-1568-4ac2-9944-db08cfa708ff'
        collection = container.Collection(uuid=prepared_uuid)

        objects = {
            num: TestObject(id='_' + str(uuid4()).replace('-', '_'), num=num)
            for num in range(10)
        }
        for value in objects.values():
            collection.insert(value.id, value)

        with self.connection.transaction_manager as tm:
            self.connection.root.test_object = collection
            tm.commit()
        persisted = self.connection.root.test_object

        for key, value in objects.items():
            self.assertEqual(persisted.get(value.id).num, key)


if __name__ == '__main__':
    main()

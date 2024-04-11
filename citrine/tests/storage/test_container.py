from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from uuid import uuid4

from ZODB import DB

from citrine.storage import container


class TestObject:
    """
    Generic class for testing storage with
    """
    def __init__(self, id, **kwargs):
        self.id = id
        for key, value in kwargs.items():
            setattr(self, key, value)


class CollectionMetaTests(TestCase):
    """
    Tests for the citrine.storage.container.CollectionMeta class
    """

    def test_init(self):
        # meta calculates size based on length of .keys()
        collection = MagicMock(keys=lambda: [0 for _ in range(10)])
        uuid = '108002d1-1568-4ac2-9944-db08cfa708ff'
        max_size = 5000
        strict = False

        meta = container.CollectionMeta(collection, uuid=uuid, max_size=max_size,
                                        strict=strict)

        self.assertEqual(meta.size, 10)
        self.assertEqual(meta.uuid, uuid)
        self.assertEqual(meta.max_size, max_size)
        self.assertEqual(meta.strict, strict)


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
        new_connection = self.memdb.open()
        persisted = new_connection.root.test_object

        for key, value in objects.items():
            self.assertEqual(persisted.get(value.id).num, key)

    def test_raises_indexerror_if_max_exceeded(self):
        prepared_uuid = '108002d1-1568-4ac2-9944-db08cfa708ff'
        collection = container.Collection(uuid=prepared_uuid)

        objects = {
            num: TestObject(id='_' + str(uuid4()).replace('-', '_'), num=num)
            for num in range(5001)
        }
        with self.assertRaises(IndexError):
            for value in objects.values():
                collection.insert(value.id, value)


if __name__ == '__main__':
    main()

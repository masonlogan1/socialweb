from unittest import TestCase, main
from unittest.mock import MagicMock

from tempfile import NamedTemporaryFile, TemporaryDirectory

from persistent import Persistent
from ZODB import DB

from citrine.connection import container_connection
from citrine.connection.container_connection import \
    ContainerConnectionMeta
from citrine.storage.container import Container
from citrine.client.container_client import ContainerDb

from citrine.exceptions import IncompatibleDatabaseError


class TestType(Persistent):
    """
    Class for testing persistence. Should be able to be stored and retrieved
    without losing any data
    """

    def __init__(self, val0, val1='val1', val2=None):
        super().__init__()
        self.val0 = val0
        self.val1 = val1
        self.val2 = val2
        self.val3 = 'val3'


class ContainerConnectionMetaTests(TestCase):
    """
    Tests that the ContainerConnectionMeta object is able to accurately
    represent data about the Container object
    """
    # these tests are extremely basic, the meta should really just be passing
    # forward the values from the container, we just need to make sure that
    # is actually happening

    def setUp(self):
        """Create new mock objects for each test"""
        self.sample_container = Container.new(100)
        self.mock_connection = MagicMock(container=self.sample_container)

    def tearDown(self):
        """"""

    def test_container(self):
        """
        Tests that the Container object is accurately provided
        """
        meta = ContainerConnectionMeta(self.mock_connection)
        self.assertEqual(meta.container, self.sample_container)

    def test_capacity(self):
        """
        Tests that an accurate capacity value is provided
        """
        meta = ContainerConnectionMeta(self.mock_connection)
        self.assertEqual(meta.capacity, self.sample_container.capacity)

    def test_used(self):
        """
        Tests that an accurate used value is provided
        """
        meta = ContainerConnectionMeta(self.mock_connection)
        self.assertEqual(meta.used, self.sample_container.used)

    def test_usage(self):
        """
        Tests that an accurate usage percentage is provided
        """
        meta = ContainerConnectionMeta(self.mock_connection)
        self.assertEqual(meta.usage, self.sample_container.usage)

    def test_status(self):
        """
        Tests that an accurate status value is provided
        """
        meta = ContainerConnectionMeta(self.mock_connection)
        self.assertEqual(meta.status, self.sample_container.status)

    def test_strict(self):
        """
        Tests that an accurate strict value is provided
        """
        meta = ContainerConnectionMeta(self.mock_connection)
        self.assertEqual(meta.strict, self.sample_container.strict)


class ContainerConnectionPropertiesTests(TestCase):
    """
    Tests that the ContainerConnection has accurate metadata passthrough
    properties
    """
    # these are pretty much a duplicate of the Meta object tests but ensure
    # we are passing through correctly

    def setUp(self):
        """
        Creates a temporary database for each test
        """
        self.temp_directory = TemporaryDirectory()
        self.temp_db_file = NamedTemporaryFile(dir=self.temp_directory.name)
        self.temp_db = ContainerDb.new(self.temp_db_file.name)

    def tearDown(self):
        """
        Deletes the temporary database
        """
        self.temp_db.close()
        self.temp_db_file.close()
        self.temp_directory.cleanup()

    def test_container(self):
        """
        Tests that the Container object is accurately provided
        """
        conn = container_connection.ContainerConnection(self.temp_db)
        self.assertIsInstance(conn.container, Container)
        self.assertEqual(conn.container, conn.root.container)

    def test_capacity(self):
        """
        Tests that an accurate capacity value is provided
        """
        conn = container_connection.ContainerConnection(self.temp_db)
        self.assertEqual(conn.capacity, conn.root.container.capacity)

    def test_used(self):
        """
        Tests that an accurate used value is provided
        """
        conn = container_connection.ContainerConnection(self.temp_db)
        self.assertEqual(conn.used, conn.root.container.used)

    def test_usage(self):
        """
        Tests that an accurate usage percentage is provided
        """
        conn = container_connection.ContainerConnection(self.temp_db)
        self.assertEqual(conn.usage, conn.root.container.usage)

    def test_status(self):
        """
        Tests that an accurate status value is provided
        """
        conn = container_connection.ContainerConnection(self.temp_db)
        self.assertEqual(conn.status, conn.root.container.status)

    def test_strict(self):
        """
        Tests that an accurate strict value is provided
        """
        conn = container_connection.ContainerConnection(self.temp_db)
        self.assertEqual(conn.strict, conn.root.container.strict)


class ContainerConnectionConstructorTests(TestCase):
    """
    Tests that the ContainerConnection can be constructed from a database
    and will raise an exception if the db is missing a Container
    """

    def setUp(self):
        """
        Creates a temporary database for each test
        """
        self.temp_directory = TemporaryDirectory()
        self.temp_db_file = NamedTemporaryFile(dir=self.temp_directory.name)

    def tearDown(self):
        """
        Deletes the temporary database
        """
        self.temp_db_file.close()
        self.temp_directory.cleanup()

    def test_construction_with_containerdb(self):
        """
        Test that a connection can be created using a ContainerDb object
        """
        db = ContainerDb.new(self.temp_db_file.name)

        # as long as this doesn't throw an exception, it passes
        connection = container_connection.ContainerConnection(db)

    def test_construction_with_compatible_database(self):
        """
        Test that a connection can be created using a database that has a
        Container object at root.container
        """
        db = DB(self.temp_db_file.name)
        conn = db.open()
        with conn.transaction_manager as tm:
            conn.root.container = Container.new()
            tm.commit()
        conn.close()

        # as long as this doesn't throw an exception, it passes
        connection = container_connection.ContainerConnection(db)

    def test_construction_with_incompatible_database(self):
        """
        Test that a connection cannot be made using a database that lacks
        a Container object, or at least lacks a Container object at
        root.container
        """
        db = DB(self.temp_db_file.name)

        # as long as this raises an IncompatibleDatabaseError, it passes
        with self.assertRaises(IncompatibleDatabaseError):
            connection = container_connection.ContainerConnection(db)


class ContainerConnectionCreateReadUpdateDeleteTests(TestCase):
    """
    Tests that the ContainerConnection can Create, Read, Update, and Delete
    values from the container, that the actions are automatically transactional,
    and that the autotransaction functionality can be disabled
    """

    def setUp(self):
        """
        Creates a temporary database for each test
        """
        self.temp_directory = TemporaryDirectory()
        self.temp_db_file = NamedTemporaryFile(dir=self.temp_directory.name)

    def tearDown(self):
        """
        Deletes the temporary database
        """
        self.temp_db_file.close()
        self.temp_directory.cleanup()

    def test_create_builtin_type(self):
        """
        Tests the create method by storing and retrieving string values.
        Should auto-commit.
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['key0', 'key1', 'key2', 'key3']
        values = ['val0', 'val1', 'val2', 'val3']
        items = {k: v for k, v in zip(keys, values)}

        for key, value in items.items():
            connection.create(key, value)

        # check that all key-value pairs are present
        for key, value in items.items():
            self.assertTrue(connection.root.container.has(key))
            self.assertEqual(connection.root.container.read(key), value)

    def test_create_custom_type(self):
        """
        Tests the create method by storing and retrieving values with a custom
        class. Should auto-commit.
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['0', '1', '2', '3']
        values = [
            TestType('val0.0', 'val1.0', 'val2.0'),
            TestType('val0.1', 'val1.1', 'val2.1'),
            TestType('val0.2', 'val1.2', 'val2.2'),
            TestType('val0.3', 'val1.3', 'val2.3')
        ]
        items = {k: v for k, v in zip(keys, values)}

        # check that the values are unsaved
        for value in values:
            self.assertEqual(value._p_status, 'unsaved')

        for key, value in items.items():
            connection.create(key, value)

        # check that the values are now saved
        for value in values:
            self.assertEqual(value._p_status, 'saved')

        # check that all values are present and accurate
        for key, value in items.items():
            self.assertTrue(connection.root.container.has(key))
            self.assertEqual(connection.root.container.read(key), value)

    def test_read_builtin_type(self):
        """
        Tests the read method by retrieving string values from the container.
        Should auto-commit.
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['key0', 'key1', 'key2', 'key3']
        values = ['val0', 'val1', 'val2', 'val3']
        items = {k: v for k, v in zip(keys, values)}

        # write values directly to container
        with connection.transaction_manager as tm:
            for key, value in items.items():
                connection.root.container.write(key, value)
            tm.commit()

        for key, value in items.items():
            self.assertEqual(connection.read(key), value)

    def test_read_custom_type(self):
        """
        Tests the read method by retrieving values with a custom class.
        Should auto-commit.
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['0', '1', '2', '3']
        values = [
            TestType('val0.0', 'val1.0', 'val2.0'),
            TestType('val0.1', 'val1.1', 'val2.1'),
            TestType('val0.2', 'val1.2', 'val2.2'),
            TestType('val0.3', 'val1.3', 'val2.3')
        ]
        items = {k: v for k, v in zip(keys, values)}

        # write values directly to container
        with connection.transaction_manager as tm:
            for key, value in items.items():
                connection.root.container.write(key, value)
            tm.commit()

        for key, value in items.items():
            self.assertEqual(connection.read(key), value)

    def test_update_builtin_type(self):
        """
        Tests the update method by storing and retrieving string values from
        the container. Should auto-commit.
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['key0', 'key1', 'key2', 'key3']
        initial_values = ['val0', 'val1', 'val2', 'val3']
        updated_values = ['val0.1', 'val1.1', 'val2.1', 'val3.1']
        initial_items = {k: v for k, v in zip(keys, initial_values)}
        updated_items = {k: v for k, v in zip(keys, updated_values)}

        # insert directly with container's write method
        with connection.transaction_manager as tm:
            for key, value in initial_items.items():
                connection.root.container.write(key, value)
            tm.commit()

        # check that initial insert worked
        for key, value in initial_items.items():
            self.assertTrue(connection.root.container.has(key))
            self.assertEqual(connection.root.container.read(key), value)

        # update values using connection method
        for key, value in updated_items.items():
            connection.update(key, value)

        # check that update worked
        for key, value in updated_items.items():
            self.assertTrue(connection.root.container.has(key))
            self.assertEqual(connection.root.container.read(key), value)

    def test_update_custom_type(self):
        """
        Tests the update method by storing and retrieving values with a custom
        class. Should auto-commit.
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['key0', 'key1', 'key2', 'key3']
        initial_values = values = [
            TestType('val0.0', 'val1.0', 'val2.0'),
            TestType('val0.1', 'val1.1', 'val2.1'),
            TestType('val0.2', 'val1.2', 'val2.2'),
            TestType('val0.3', 'val1.3', 'val2.3')
        ]
        updated_values = values = [
            TestType('val0.0upd', 'val1.0upd', 'val2.0upd'),
            TestType('val0.1upd', 'val1.1upd', 'val2.1upd'),
            TestType('val0.2upd', 'val1.2upd', 'val2.2upd'),
            TestType('val0.3upd', 'val1.3upd', 'val2.3upd')
        ]
        initial_items = {k: v for k, v in zip(keys, initial_values)}
        updated_items = {k: v for k, v in zip(keys, updated_values)}

        # insert directly with container's write method
        with connection.transaction_manager as tm:
            for key, value in initial_items.items():
                connection.root.container.write(key, value)
            tm.commit()

        # check that initial insert worked
        for key, value in initial_items.items():
            self.assertTrue(connection.root.container.has(key))
            self.assertEqual(connection.root.container.read(key), value)

        # update values using connection method
        for key, value in updated_items.items():
            connection.update(key, value)

        # check that update worked
        for key, value in updated_items.items():
            self.assertTrue(connection.root.container.has(key))
            self.assertEqual(connection.root.container.read(key), value)

    def test_delete_builtin_type(self):
        """
        Tests the delete method by removing and returning a string value.
        Should auto-commit.
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['key0', 'key1', 'key2', 'key3']
        values = ['val0', 'val1', 'val2', 'val3']
        items = {k: v for k, v in zip(keys, values)}

        expected_items = {k: v for k, v in
                          zip(keys[:1] + keys[2:], values[:1] + values[2:])}

        # write values directly to container
        with connection.transaction_manager as tm:
            for key, value in items.items():
                connection.root.container.write(key, value)
            tm.commit()

        connection.delete(keys[1])

        # check keys[1] is gone and that everything else is still there
        self.assertFalse(connection.root.container.has(keys[1]))
        for key, value in expected_items.items():
            self.assertEqual(connection.root.container.read(key), value)

    def test_delete_custom_type(self):
        """
        Tests the delete method by removing and returning a value with a custom
        class. Should auto-commit.
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['key0', 'key1', 'key2', 'key3']
        values = [
            TestType('val0.0', 'val1.0', 'val2.0'),
            TestType('val0.1', 'val1.1', 'val2.1'),
            TestType('val0.2', 'val1.2', 'val2.2'),
            TestType('val0.3', 'val1.3', 'val2.3')
        ]
        items = {k: v for k, v in zip(keys, values)}

        expected_items = {k: v for k, v in
                          zip(keys[:1] + keys[2:], values[:1] + values[2:])}

        # write values directly to container
        with connection.transaction_manager as tm:
            for key, value in items.items():
                connection.root.container.write(key, value)
            tm.commit()

        connection.delete(keys[1])

        # check keys[1] is gone and that everything else is still there
        self.assertFalse(connection.root.container.has(keys[1]))
        for key, value in expected_items.items():
            self.assertEqual(connection.root.container.read(key), value)

    def test_no_autocommit(self):
        """
        Tests that the autocommit can be disabled
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)
        connection.autocommit = False

        keys = ['key0', 'key1', 'key2', 'key3']
        initial_values = [
            TestType('val0.0', 'val1.0', 'val2.0'),
            TestType('val0.1', 'val1.1', 'val2.1'),
            TestType('val0.2', 'val1.2', 'val2.2'),
            TestType('val0.3', 'val1.3', 'val2.3')
        ]
        updated_values = [
            TestType('val0.0upd', 'val1.0upd', 'val2.0upd'),
            TestType('val0.1upd', 'val1.1upd', 'val2.1upd'),
            TestType('val0.2upd', 'val1.2upd', 'val2.2upd'),
            TestType('val0.3upd', 'val1.3upd', 'val2.3upd')
        ]
        initial_items = {k: v for k, v in zip(keys, initial_values)}
        updated_items = {k: v for k, v in zip(keys, updated_values)}

        # check that the values are unsaved
        for value in initial_values:
            self.assertEqual(value._p_status, 'unsaved')

        for key, value in initial_items.items():
            connection.create(key, value)

        # check that the values remain unsaved
        for key in keys:
            self.assertEqual(connection.read(key)._p_status, 'unsaved')

        for key, value in updated_items.items():
            connection.update(key, value)

        # check that the values remain unsaved
        for key in keys:
            self.assertEqual(connection.read(key)._p_status, 'unsaved')


class ContainerConnectionGetItemTests(TestCase):
    """
    Tests that the ContainerConnection can get one or more items using index
    syntax
    """

    def setUp(self):
        """
        Creates a temporary database for each test
        """
        self.temp_directory = TemporaryDirectory()
        self.temp_db_file = NamedTemporaryFile(dir=self.temp_directory.name)

    def tearDown(self):
        """
        Deletes the temporary database
        """
        self.temp_db_file.close()
        self.temp_directory.cleanup()

    def test_single_value(self):
        """
        Tests that a single value can be retrieved using index syntax
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['0', '1', '2', '3']
        values = [
            TestType('val0.0', 'val1.0', 'val2.0'),
            TestType('val0.1', 'val1.1', 'val2.1'),
            TestType('val0.2', 'val1.2', 'val2.2'),
            TestType('val0.3', 'val1.3', 'val2.3')
        ]
        items = {k: v for k, v in zip(keys, values)}

        for key, value in items.items():
            connection.create(key, value)

        for key, value in items.items():
            self.assertEqual(connection[key], value)

    def test_multiple_values(self):
        """
        Tests that multiple values can be retrieved using comma-separated index
        syntax
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['0', '1', '2', '3']
        values = [
            TestType('val0.0', 'val1.0', 'val2.0'),
            TestType('val0.1', 'val1.1', 'val2.1'),
            TestType('val0.2', 'val1.2', 'val2.2'),
            TestType('val0.3', 'val1.3', 'val2.3')
        ]
        items = {k: v for k, v in zip(keys, values)}

        for key, value in items.items():
            connection.create(key, value)

        # get two values as a list by their keys
        expected_vals = [values[0], values[2]]
        self.assertEqual(connection[keys[0], keys[2]], expected_vals)

    def test_single_nonexistent_value(self):
        """
        Tests that a KeyError will be raised for a single nonexistent value
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['0', '1', '2', '3']
        values = [
            TestType('val0.0', 'val1.0', 'val2.0'),
            TestType('val0.1', 'val1.1', 'val2.1'),
            TestType('val0.2', 'val1.2', 'val2.2'),
            TestType('val0.3', 'val1.3', 'val2.3')
        ]
        items = {k: v for k, v in zip(keys, values)}

        for key, value in items.items():
            connection.create(key, value)

        with self.assertRaises(KeyError):
            bad_value = connection['bad_key']

    def test_multiple_nonexistent_values_all_nonexistent(self):
        """
        Tests that a list of all None will be returned for multiple nonexistent
        values when all values do not exist
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['0', '1', '2', '3']
        values = [
            TestType('val0.0', 'val1.0', 'val2.0'),
            TestType('val0.1', 'val1.1', 'val2.1'),
            TestType('val0.2', 'val1.2', 'val2.2'),
            TestType('val0.3', 'val1.3', 'val2.3')
        ]
        items = {k: v for k, v in zip(keys, values)}

        for key, value in items.items():
            connection.create(key, value)

        with self.assertRaises(KeyError):
            bad_value = connection['bad_key0', 'bad_key1']

    def test_multiple_nonexistent_values_partial_missing(self):
        """
        Tests that a list with None values will be returned alongside existing
        values when some values in a multiple-index selection are present
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        keys = ['0', '1', '2', '3']
        values = [
            TestType('val0.0', 'val1.0', 'val2.0'),
            TestType('val0.1', 'val1.1', 'val2.1'),
            TestType('val0.2', 'val1.2', 'val2.2'),
            TestType('val0.3', 'val1.3', 'val2.3')
        ]
        items = {k: v for k, v in zip(keys, values)}

        for key, value in items.items():
            connection.create(key, value)

        # get two values as a list by their keys
        expected_vals = [values[0], None, values[2]]
        self.assertEqual(connection[keys[0], 'bad_key', keys[2]], expected_vals)


class ContainerConnectionContextManagerTests(TestCase):
    """
    Tests that the ContainerConnection can act as a transaction manager that
    commits a block of actions when the block ends
    """

    def setUp(self):
        """
        Creates a temporary database for each test
        """
        self.temp_directory = TemporaryDirectory()
        self.temp_db_file = NamedTemporaryFile(dir=self.temp_directory.name)

    def tearDown(self):
        """
        Deletes the temporary database
        """
        self.temp_db_file.close()
        self.temp_directory.cleanup()

    def test_context_transaction_block_success(self):
        """
        Tests that a block of actions will succeed and update the database
        if the entire context-managed block succeeds
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        expected = {'key0': 'val0.2', 'key1': 'val1.1', 'key3': 'val0.3'}

        with connection as transaction:
            connection.create('key0', 'val0.0')
            connection.create('key1', 'val1.0')
            connection.create('key2', 'val2.0')
            connection.update('key0', 'val0.1')
            connection.update('key1', 'val1.1')
            connection.update('key0', 'val0.2')
            connection.create('key3', 'val0.3')
            connection.delete('key2')

        for key, value in expected.items():
            self.assertEqual(connection.root.container.read(key), value)

        with connection as transaction:
            connection.update('key0', TestType('val0.0', 'val0.1', 'val0.2'))
            connection.update('key1', TestType('val1.0', 'val1.1', 'val1.2'))
            connection.create('key2', TestType('val2.0', 'val2.1', 'val2.2'))
            connection.update('key3', TestType('val3.0', 'val3.1', 'val3.3'))

        for key in ['key0', 'key1', 'key2', 'key3']:
            self.assertTrue(connection.root.container.read(key)._p_status, 'saved')

    def test_context_transaction_block_failure(self):
        """
        Tests that a block of actions will fail and no update will occur
        if the entire context-managed block fails
        """
        db = ContainerDb.new(self.temp_db_file.name)
        connection = container_connection.ContainerConnection(db)

        expected = {'key0': 'val0.2', 'key1': 'val1.1', 'key3': 'val3.0'}

        with connection as transaction:
            connection.create('key0', 'val0.0')
            connection.create('key1', 'val1.0')
            connection.create('key2', 'val2.0')
            connection.update('key0', 'val0.1')
            connection.update('key1', 'val1.1')
            connection.update('key0', 'val0.2')
            connection.delete('key2')
            transaction.abort()

        for key, value in expected.items():
            self.assertFalse(connection.root.container.has(key))


if __name__ == '__main__':
    main()

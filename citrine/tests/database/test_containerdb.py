from unittest import TestCase, main

from tempfile import NamedTemporaryFile, TemporaryDirectory

from ZODB import DB
from ZODB.FileStorage import FileStorage

from citrine.connection.container_connection import ContainerConnection
from citrine.database import containerdb
from citrine.storage.container import Container


# If the tests seem sparce, it's because the ContainerDb class is intended to
#   serve as a representation of the object in storage. The database object
#   itself does not have methods or functions used to directly modifying its
#   contents; to do that a connection must first be made.
#
# The context manager for opening a temporary connection is only tested
#   insofar as it is capable of creating a temporary connection and closing it
#   at the end of the with statement. The actual functionality of the connection
#   is not considered part of these tests.


# FUTURE: it would be great if we could test every parameter for the
#   ContainerDb however most of these are implemented by Zope, and it would be
#   an unhelpful use of time to create 20+ tests

class ContainerDbConstructorTests(TestCase):
    """
    Tests that the ``ContainerDb`` class is able to load an existing database
    with ``load``, create new ones using ``create``, and able to perform both
    of these actions at once using ``new``
    """

    def setUp(self):
        # set up a temporary directory and file
        self.temp_directory = TemporaryDirectory()
        self.temp_db_file = NamedTemporaryFile(dir=self.temp_directory.name)

    def tearDown(self):
        # safely close the filestorage file
        self.temp_db_file.close()
        self.temp_directory.cleanup()

    def test_basic_constructor_from_filestorage(self):
        """
        Tests that the standard __init__ constructor creates a ContainerDb
        object from a FileStorage object
        """
        storage = FileStorage(self.temp_db_file.name)

        db = containerdb.ContainerDb(storage)

        # check that we are getting the correct connection type
        self.assertIsInstance(db.open(), ContainerConnection)

        conn = db.open()
        container = Container.new()
        with conn.transaction_manager as tm:
            conn.root.container = container
            tm.commit()

        # assuming the connection works, check that the db has the container
        self.assertIsInstance(db.open().root.container, Container)

    def test_basic_constructor_from_path_string(self):
        """
        Tests that the standard __init__ constructor creates a ContainerDb
        object from a path string
        """
        storage = self.temp_db_file.name

        db = containerdb.ContainerDb(storage)

        # check that we are getting the correct connection type
        self.assertIsInstance(db.open(), ContainerConnection)

        conn = db.open()
        container = Container.new()
        with conn.transaction_manager as tm:
            conn.root.container = container
            tm.commit()

        # assuming the connection works, check that the db has the container
        self.assertIsInstance(db.open().root.container, Container)

    def test_create_default_capacity(self):
        """
        Tests that the create method will create a new ContainerDb at the
        provided path with the default capacity
        """
        expected_capacity = 115000
        storage = containerdb.ContainerDb.create(self.temp_db_file.name)
        db = containerdb.ContainerDb(storage)

        conn = db.open()
        self.assertEqual(conn.root.container.capacity, expected_capacity)

    def test_create_custom_capacity(self):
        """
        Tests that the create method will create a new ContainerDb at the
        provided path with the provided capacity
        """
        custom_capacity = 1000
        storage = containerdb.ContainerDb.create(
            self.temp_db_file.name,
            capacity=custom_capacity
        )
        db = containerdb.ContainerDb(storage)

        conn = db.open()
        self.assertEqual(conn.root.container.capacity, custom_capacity)

    def test_load(self):
        """
        Tests that the load method will open an existing ContainerDb object
        and raise a FileNotFoundError if the files does not exist
        """
        custom_capacity = 1000
        storage = containerdb.ContainerDb.create(
            self.temp_db_file.name,
            capacity=custom_capacity
        )
        db = containerdb.ContainerDb.load(storage)

        conn = db.open()
        self.assertEqual(conn.root.container.capacity, custom_capacity)

    def test_new_default_capacity(self):
        """
        Tests that the new method will create a new ContainerDb at the
        provided path with the default capacity and then return ContainerDb
        object
        """
        expected_capacity = 115000
        db = containerdb.ContainerDb.new(self.temp_db_file.name)

        conn = db.open()
        self.assertEqual(conn.root.container.capacity, expected_capacity)

    def test_new_custom_capacity(self):
        """
        Tests that the new method will create a new ContainerDb at the
        provided path with the provided capacity and then return ContainerDb
        object
        """
        custom_capacity = 1000
        db = containerdb.ContainerDb.new(
            self.temp_db_file.name,
            capacity=custom_capacity
        )

        conn = db.open()
        self.assertEqual(conn.root.container.capacity, custom_capacity)


class ContainerDbContextManagerTests(TestCase):
    """
    Tests that the ``ContainerDb`` class is able to create a temporary
    connection object when used as a context manager
    """

    def setUp(self):
        # set up a temporary directory and file
        self.temp_directory = TemporaryDirectory()
        self.temp_db_file = NamedTemporaryFile(dir=self.temp_directory.name)

    def tearDown(self):
        # safely close the filestorage file
        self.temp_db_file.close()
        self.temp_directory.cleanup()

    def test_with_statement(self):
        """
        Tests that a ContainerDb opens up a temporary connection when used
        as a context manager and closes that connection at the end of the block
        """
        db = containerdb.ContainerDb.new(self.temp_db_file.name)

        keys = ['key0', 'key1', 'key2', 'key3']
        values = ['val0', 'val1', 'val2', 'val3']
        items = {k: v for k, v in zip(keys, values)}

        with db as connection:
            with connection.transaction_manager as tm:
                for key, value in items.items():
                    connection.root.container.write(key, value)
                tm.commit()

        with db as connection:
            for key, value in items.items():
                self.assertTrue(connection.root.container.has(key))
                self.assertEqual(connection.root.container.read(key), value)


if __name__ == '__main__':
    main()

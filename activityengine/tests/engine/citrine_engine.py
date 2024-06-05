from unittest import TestCase, main
from tempfile import TemporaryDirectory, NamedTemporaryFile

from citrine import CitrineDB
from jsonld import JsonLdPackage

from activityengine.engine import citrine_engine as ce


class CitrineEngineConstructor(TestCase):
    """
    Tests the constructor for a ``CitrineEngine`` object.

    Checks that the correct filesystem database is represented to and that the
    default packages are correctly added/organized
    """

    def setUp(self):
        """
        Creates a temporary database for each test
        """
        self.temp_directory = TemporaryDirectory()
        self.temp_db_file = NamedTemporaryFile(dir=self.temp_directory.name)
        temp_db = CitrineDB.new(self.temp_db_file.name).close()

    def tearDown(self):
        """
        Deletes the temporary database
        """
        self.temp_db_file.close()
        self.temp_directory.cleanup()

    def test_connect_to_existing_db_no_packages(self):
        """
        Tests that a new ``CitrineEngine`` object can be created using the
        ``__init__`` constructor using no packages
        """


    def test_connect_to_existing_db_one_package(self):
        """
        Tests that a new ``CitrineEngine`` object can be created using the
        ``__init__`` constructor using one package
        """

    def test_connect_to_existing_db_multiple_packages(self):
        """
        Tests that a new ``CitrineEngine`` object can be created using the
        ``__init__` constructor using multiple packages
        """

    def test_load_existing_db_no_packages(self):
        """
        Tests that a ``CitrineEngine.load`` will load an object from an
        existing filesystem db, providing no packages
        """

    def test_load_existing_db_one_package(self):
        """
        Tests that a ``CitrineEngine.load`` will load an object from an
        existing filesystem db, providing one package
        """

    def test_load_existing_db_multiple_packages(self):
        """
        Tests that a ``CitrineEngine.load`` will load an object from an
        existing filesystem db, providing multiple packages
        """

    def test_create_filesystem_db(self):
        """
        Tests that the ``CitrineEngine.create`` method can be used to create
        a new filesystem db and return a ``Filesystem`` object
        """

    def test_new_no_packages(self):
        """
        Tests that the ``CitrineEngine.new`` method can be used to create
        a new filesystem db and return a ``CitrineEngine`` object
        with no packages loaded
        """

    def test_new_one_package(self):
        """
        Tests that the ``CitrineEngine.new`` method can be used to create
        a new filesystem db and return a ``CitrineEngine`` object
        with a single package loaded
        """

    def test_new_multiple_packages(self):
        """
        Tests that the ``CitrineEngine.new`` method can be used to create
        a new filesystem db and return a ``CitrineEngine`` object
        with multiple packages loaded
        """


class CitrineEngineConnectionConstructor(TestCase):
    """
    Tests the constructor for a ``CitrineEngineConnection`` object and that one
    can be acquired from a ``CitrineEngine``.

    Checks that a filesystem database can be connected to manually, that a
    database object can produce a connection, that a manually created
    connection takes a set of packages and integrates them into the json engine,
    that a database object-created connection is provided with the db object's
    packages, and that additional packages can be provided to a database object
    created connection that receive priority over the previous packages
    """

    def test_connect_to_db_no_packages(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        by providing a database object and no packages
        """

    def test_connect_to_db_one_package(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        by providing a database object and a single package
        """

    def test_connect_to_db_multiple_packages(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        by providing a database object and multiple packages
        """

    def test_connection_from_db_open_no_packages(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        from a ``CitrineEngine``'s ``open`` method when the engine has no
        packages and no additional packages are provided
        """

    def test_connection_from_db_open_one_engine_package_no_additional(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        from a ``CitrineEngine``'s ``open`` method when the engine has one
        package and no additional packages are provided
        """

    def test_connection_from_db_open_multiple_engine_packages_no_additional(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        from a ``CitrineEngine``'s ``open`` method when the engine has multiple
        packages and no additional packages are provided
        """

    def test_connection_from_db_no_engine_packages_one_additional(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        from a ``CitrineEngine``'s ``open`` method when the engine has no
        packages and one additional package is provided
        """

    def test_connection_from_db_no_engine_packages_multiple_additional(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        from a ``CitrineEngine``'s ``open`` method when the engine has no
        packages and multiple additional packages are provided
        """

    def test_connection_from_db_one_engine_package_one_additional(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        from a ``CitrineEngine``'s ``open`` method when the engine has one
        package and one additional package is provided
        """

    def test_connection_from_db_one_engine_package_multiple_additional(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        from a ``CitrineEngine``'s ``open`` method when the engine has one
        package and multiple additional packages are provided
        """

    def test_connection_from_db_multiple_engine_packages_one_additional(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        from a ``CitrineEngine``'s ``open`` method when the engine has multiple
        packages and one additional package is provided
        """

    def test_connection_from_db_multiple_engine_packages_multiple_additional(self):
        """
        Tests that a new ``CitrineEngineConnection`` object can be created
        from a ``CitrineEngine``'s ``open`` method when the engine has multiple
        packages and multiple additional packages are provided
        """


class CitrineEngineConnectionJsonLdEngine(TestCase):
    """
    Tests that the jsonld engine receives the packages, can take json text
    data, and can perform the basic actions of a ``JsonLdEngine`` object.
    """

    def test_produces_create_method_for_each_class_in_package(self):
        """
        Tests that a ``CitrineEngineConnection`` object creates a
        ``create_x`` method for each object in the packages
        """

    def test_parses_json_text_into_objects(self):
        """
        Tests that a ``CitrineEngineConnection`` object can process json text
        into objects from the packages
        """

    def test_parses_json_text_into_new_persistent_objects(self):
        """
        Tests that a ``CitrineEngineConnection`` object can process json text
        into objects from the packages and save those objects to the database
        """

    def test_raises_exception_on_nonpermitted_database_overwrite(self):
        """
        Tests that a ``CitrineEngineConnection`` object will raise an exception
        when attempting to parse and process json text data if the id is
        already in use and ``overwrite=False``
        """

    def test_parses_json_text_into_updated_perisistent_objects(self):
        """
        Tests that a ``CitrineEngineConnection`` object can process json text
        into objects from the packages and overwrite an existing object in the
        database if ``overwrite=True``
        """


class CitrineEngineConnectionDatabase(TestCase):
    """
    Tests that the database can be accessed using the same constructor params
    as a ``CitrineDB`` object, and that the standard ``create``, ``read``,
    ``update``, and ``delete`` methods can be used.

    Objects created by the engine should persist automatically, load by id
    without losing any data, and update in the database when autocommit is
    enabled.
    """

    def test_persistent_creation(self):
        """
        Tests that a ``CitrineEngineConnection`` object can create a new
        object in the database using one of the ``create_x`` methods
        """

    def test_exception_on_overwrite_with_create(self):
        """
        Tests that unless ``overwrite=True`` is provided, a ``create`` action
        will raise an exception if the id is already used in the database
        """

    def test_update_on_noncrystalized_object(self):
        """
        Tests that if the ``update`` method is used and the object to update
        with is not currently crystallized, the engine will attempt to
        crystallize the object
        """

    def test_update_on_crystallized_object(self):
        """
        Tests that if the ``update`` method is used and the object to update
        with is already crystallized, the engine will not alter the existing
        crystal
        """

    def test_read_loads_with_specified_type(self):
        """
        Tests that the ``read`` method can be used to load an object when it is
        explicitly given a class to use
        """

    def test_read_selects_correct_type(self):
        """
        Tests that the ``read`` method can be used to detect the type of object
        that should be loaded and correctly load objects from the database
        """

    def test_read_autocommit(self):
        """
        Tests that ``read`` can load objects that will automatically commit
        any changes to tracked properties to the database
        """

    def test_read_autocommit_off(self):
        """
        Tests that ``read`` can load objects that will not automatically commit
        any changes to tracked properties to the database
        """


if __name__ == '__main__':
    main()

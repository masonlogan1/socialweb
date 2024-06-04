from unittest import TestCase, main


class CitrineEngineConstructor(TestCase):
    """
    Tests the constructor for a ``CitrineEngine`` object.

    Checks that the correct filesystem database is represented to and that the
    default packages are correctly added/organized
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


class CitrineEngineConnectionJsonLdEngine(TestCase):
    """
    Tests that the jsonld engine receives the packages, can take json text
    data, and can perform the basic actions of a ``JsonLdEngine`` object.
    """


class CitrineEngineConnectionDatabase(TestCase):
    """
    Tests that the database can be accessed using the same constructor params
    as a ``CitrineDB`` object, and that the standard ``create``, ``read``,
    ``update``, and ``delete`` methods can be used.
    """


class CitrineEngineConnectionObjectManagement(TestCase):
    """
    Tests that objects created by the CitrineEngineConnection work as expected.

    Objects created by the engine should persist automatically, load by id
    without losing any data, and update in the database when autocommit is
    enabled.
    """


if __name__ == '__main__':
    main()

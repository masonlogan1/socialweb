"""
Provides objects and functions for packaging classes into a format the JSON-LD
engine can load
"""

class JsonLdPackage:
    """
    A discrete package of classes, properties, and transformation functions
    that can be given to the JSON-LD engine and used to process new and existing
    JSON-LD data

    All packages MUST have a unique namespace
    """

    @property
    def namespace(self):
        # this will always be set during construction
        return self.__namespace

    @namespace.setter
    def namespace(self, ns):
        # can only be set once, during construction
        if getattr(self, 'namespace', None):
            raise AttributeError(f'JsonLdPackage namespace is immutable')
        self.__namespace = ns

    def __init__(self, namespace: str, *args, **kwargs):
        self.namespace = namespace

    def __iter__(self):
        # need to decide how we should iterate over the data
        raise NotImplementedError("JsonLdPackage objects cannot be iterated")

    def __getitem__(self, key):
        # need to decide what the return format should look like and how slicing
        # would work here
        raise NotImplementedError("Cannot get item from JsonLdPackage objects")

    def __str__(self):
        # this should probably return the name of the package
        raise NotImplementedError("Can't convert JsonLdPackage into a string")

    def __hash__(self):
        # future work on the object persistence engine is dependent on the
        # ability to hash a package
        raise NotImplementedError("Can't hash JsonLdPackage objects")

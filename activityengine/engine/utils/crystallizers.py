"""
Classes and functions for simplifying and abstracting the Crystallization
process in the engine
"""

from citrine import Crystal

DEFAULT_DEPTH = 1


def create_method(cls):
    """
    Returns a function that can create a new instance from the provided class,
    crystallize it, persists that crystallized form into the database, and
    return the object.

    Also provides an optional keyword argument 'depth' that specifies the depth
    of connected objects that should also be persisted

    :param cls: the class to use
    :return: a function that can create a new instance
    """

    def create(self, id, depth=DEFAULT_DEPTH, *args, **kwargs):
        """
        Creates a new instance of the class, crystallizes it, persists that
        crystallized form into the database, and returns the object
        :param id: the id of the object
        :param depth: persistence depth for connected objects
        :return: a new object
        """
        new_obj = cls(id, *args, **kwargs)
        crystallized_obj = Crystal.crystallize(new_obj)
        self.create(id, crystallized_obj)

        return new_obj

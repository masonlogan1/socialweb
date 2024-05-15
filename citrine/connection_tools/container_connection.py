from ZODB.Connection import Connection

class ContainerConnection(Connection):
    """
    Expansion of ``ZODB.Connection`` that obscures the under-the-hood functions
    in favor of ``create``, ``read``, ``update``, and ``delete`` methods.
    """
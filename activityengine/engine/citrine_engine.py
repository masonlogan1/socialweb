"""
Implementations of the ``jsonld.JsonLdEngine`` that can work on top of both
a local Citrine database or as a client for a CitrineServer database
"""

from jsonld import JsonLdEngine
from citrine import CitrineDBConnection, CitrineClientConnection


class CitrineEngine(JsonLdEngine, CitrineDBConnection):
    """
    Implementation of the JsonLdEngine that functions as the connection for a
    local CitrineDB
    """


class CitrineClientEngine(JsonLdEngine, CitrineClientConnection):
    """
    Implementation of the JsonLdEngine that functions as the client for a
    remote CitrineServer
    """
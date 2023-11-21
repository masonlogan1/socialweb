"""
AUTHOR:     Mason Logan <PythonActivityStreams@masonlogan.com>
CREATED:    November 16, 2023
UPDATED:    November 16, 2023
Implements core objects for working with ActivityStreams. Objects are intended
to be used as an alternative to working directly with JSON-LD data.
"""
# Yes, the docstrings for each class are directly taken from the ActivityStreams
# Vocabulary document. This whole module is intentionally barely one level of
# abstraction from the spec
from vocabulary import Object

class Application(Object):
    """
    Describes a software application.
    """


class Group(Object):
    """
    Represents a formal or informal collective of Actors.
    """


class Organization(Object):
    """
    Represents an organization.
    """


class Person(Object):
    """
    Represents an individual person.
    """


class Service(Object):
    """
    Represents a service of any kind.
    """
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


class Relationship(Object):
    """
    Describes a relationship between two individuals. The subject and object
    properties are used to identify the connected individuals.

    See 5.2 Representing Relationships Between Entities for additional
    information.
    """
    def __init__(self, id, subject=None, object=None, relationship=None,
                 **kwargs):
        super().__init__(id, **kwargs)
        self.subject = subject
        self.object = object
        self.relationship = relationship


class Article(Object):
    """
    Represents any kind of multi-paragraph written work.
    """


class Document(Object):
    """
    Represents a document of any kind.
    """


class Audio(Document):
    """
    Represents an audio document of any kind.
    """


class Image(Document):
    """
    An image document of any kind
    """


class Video(Document):
    """
    Represents a video document of any kind.
    """


class Note(Object):
    """
    Represents a short written work typically less than a single paragraph in
    length.
    """


class Page(Document):
    """
    Represents a Web Page.
    """


class Event(Object):
    """
    Represents any kind of event.
    """


class Place(Object):
    """
    Represents a logical or physical location. See 5.3 Representing Places
    for additional information.
    """
    def __init__(self, id, accuracy=None, altitude=None, latitude=None,
                 longitude=None, radius=None, units=None, **kwargs):
        super().__init__(id, **kwargs)
        self.accuracy = accuracy
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.units = units


class Profile(Object):
    """
    A Profile is a content object that describes another Object, typically
    used to describe Actor Type objects. The describes property is used to
    reference the object being described by the profile.
    """
    def __init__(self, id, describes=None, **kwargs):
        super().__init__(id, **kwargs)
        self.describes = describes


class Tombstone(Object):
    """
    A Tombstone represents a content object that has been deleted. It can be
    used in Collections to signify that there used to be an object at this
    position, but it has been deleted.
    """
    def __init__(self, id, former_type, deleted, **kwargs):
        super().__init__(id, **kwargs)
        self.former_type = former_type
        self.deleted = deleted

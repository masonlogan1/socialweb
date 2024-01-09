"""
All Object Types inherit the properties of the base Object type. Link Types
inherit the properties of the base Link type. Some specific Object Types are
subtypes or specializations of more generalized Object Types (for instance,
the Like Type is a more specific form of the Activity type).
"""
__ref__ = "https://www.w3.org/TR/activitystreams-vocabulary/#object-types"

from activitypy.activitystreams.core import Object, Link, LinkManager
from activitypy.activitystreams.models import RelationshipModel, ArticleModel, \
    DocumentModel, AudioModel, ImageModel, VideoModel, NoteModel, PageModel, \
    EventModel, PlaceModel, ProfileModel, TombstoneModel, MentionModel
from activitypy.activitystreams.models.properties import Subject, \
    Object as ObjectProp, Relationship as RelationshipProp


class Relationship(Object, RelationshipModel):
    """
    Describes a relationship between two individuals. The subject and object
    properties are used to identify the connected individuals.
    """
    type = "Relationship"

    @ObjectProp.object.setter
    @LinkManager().setter
    def object(self, val):
        ObjectProp.object.fset(self, val)

    @Subject.subject.setter
    @LinkManager().setter
    def subject(self, val):
        Subject.subject.fset(self, val)

    @RelationshipProp.relationship.setter
    @LinkManager().setter
    def relationship(self, val):
        Relationship.relationship.fset(self, val)


class Article(Object, ArticleModel):
    """
    Represents any kind of multi-paragraph written work.
    """
    type = "Article"


class Document(Object, DocumentModel):
    """
    Represents a document of any kind.
    """
    type = "Document"


class Audio(Object, AudioModel):
    """
    Represents an audio document of any kind.
    """
    type = "Audio"


class Image(Document, ImageModel):
    """
    An image document of any kind
    """
    type = "Image"


class Video(Document, VideoModel):
    """
    Represents a video document of any kind.
    """
    type = "Video"


class Note(Object, NoteModel):
    """
    Represents a short written work typically less than a single paragraph in
    length.
    """
    type = "Note"


class Page(Document, PageModel):
    """
    Represents a Web Page.
    """
    type = "Page"


class Event(Object, EventModel):
    """
    Represents any kind of event.
    """
    type = "Event"


class Place(Object, PlaceModel):
    """
    Represents a logical or physical location. See 5.3 Representing Places
    for additional information.
    """
    type = "Place"


class Profile(Object, ProfileModel):
    """
    A Profile is a content object that describes another Object, typically
    used to describe Actor Type objects. The describes property is used to
    reference the object being described by the profile.
    """
    type = "Profile"


class Tombstone(Object, TombstoneModel):
    """
    A Tombstone represents a content object that has been deleted. It can be
    used in Collections to signify that there used to be an object at this
    position, but it has been deleted.
    """
    type = "Tombstone"


class Mention(Link, MentionModel):
    """
    A specialized Link that represents a @mention.
    """
    type = "Mention"

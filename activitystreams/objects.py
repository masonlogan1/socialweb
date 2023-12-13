"""
All Object Types inherit the properties of the base Object type. Link Types
inherit the properties of the base Link type. Some specific Object Types are
subtypes or specializations of more generalized Object Types (for instance,
the Like Type is a more specific form of the Activity type).
"""
__ref__ = "https://www.w3.org/TR/activitystreams-vocabulary/#object-types"

from activitystreams.core import Object, Link
from activitystreams.models import RelationshipModel, ArticleModel, \
    DocumentModel, AudioModel, ImageModel, VideoModel, NoteModel, PageModel, \
    EventModel, PlaceModel, ProfileModel, TombstoneModel, MentionModel


class Relationship(Object, RelationshipModel):
    """
    Describes a relationship between two individuals. The subject and object
    properties are used to identify the connected individuals.
    """
    type = "Relationship"
    context = "https://www.w3.org/ns/activitystreams#Relationship"


class Article(Object, ArticleModel):
    """
    Represents any kind of multi-paragraph written work.
    """
    type = "Article"
    context = "https://www.w3.org/ns/activitystreams#Article"


class Document(Object, DocumentModel):
    """
    Represents a document of any kind.
    """
    type = "Document"
    context = "https://www.w3.org/ns/activitystreams#Document"


class Audio(Object, AudioModel):
    """
    Represents an audio document of any kind.
    """
    type = "Audio"
    context = "https://www.w3.org/ns/activitystreams#Audio"


class Image(Document, ImageModel):
    """
    An image document of any kind
    """
    type = "Image"
    context = "https://www.w3.org/ns/activitystreams#Image"


class Video(Document, VideoModel):
    """
    Represents a video document of any kind.
    """
    type = "Video"
    context = "https://www.w3.org/ns/activitystreams#Video"


class Note(Object, NoteModel):
    """
    Represents a short written work typically less than a single paragraph in
    length.
    """
    type = "Note"
    context = "https://www.w3.org/ns/activitystreams#Note"


class Page(Document, PageModel):
    """
    Represents a Web Page.
    """
    type = "Page"
    context = "https://www.w3.org/ns/activitystreams#Page"


class Event(Object, EventModel):
    """
    Represents any kind of event.
    """
    type = "Event"
    context = "https://www.w3.org/ns/activitystreams#Event"


class Place(Object, PlaceModel):
    """
    Represents a logical or physical location. See 5.3 Representing Places
    for additional information.
    """
    type = "Place"
    context = "https://www.w3.org/ns/activitystreams#Place"


class Profile(Object, ProfileModel):
    """
    A Profile is a content object that describes another Object, typically
    used to describe Actor Type objects. The describes property is used to
    reference the object being described by the profile.
    """
    type = "Profile"
    context = "https://www.w3.org/ns/activitystreams#Profile"


class Tombstone(Object, TombstoneModel):
    """
    A Tombstone represents a content object that has been deleted. It can be
    used in Collections to signify that there used to be an object at this
    position, but it has been deleted.
    """
    type = "Tombstone"
    context = "https://www.w3.org/ns/activitystreams#Tombstone"


class Mention(Link, MentionModel):
    """
    A specialized Link that represents a @mention.
    """
    type = "Mention"
    context = "https://www.w3.org/ns/activitystreams#Mention"

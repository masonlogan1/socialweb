"""
All Object Types inherit the properties of the base Object type. Link Types
inherit the properties of the base Link type. Some specific Object Types are
subtypes or specializations of more generalized Object Types (for instance,
the Like Type is a more specific form of the Activity type).
"""
__ref__ = "https://www.w3.org/TR/activitystreams-vocabulary/#object-types"

from activitypy.activitystreams.core import Object, Link, LinkManager
from activitypy.activitystreams.handlers import NumberHandler
from activitypy.activitystreams.models import RelationshipModel, ArticleModel, \
    DocumentModel, AudioModel, ImageModel, VideoModel, NoteModel, PageModel, \
    EventModel, PlaceModel, ProfileModel, TombstoneModel, MentionModel
from activitypy.activitystreams.models.properties import Subject, \
    Object as ObjectProp, Relationship as RelationshipProp, Accuracy, Altitude,\
    Latitude, Longitude, Radius, Units

from activitypy.jsonld import JSON_DATA_CONTEXT


class Relationship(Object, RelationshipModel):
    """
    Describes a relationship between two individuals. The subject and object
    properties are used to identify the connected individuals.
    """
    type = "Relationship"

    # //// //// //// //// //// //// object //// //// //// //// //// ////
    @ObjectProp.object.getter
    @LinkManager().getter
    def object(self):
        """
        Describes an object of any kind. The Object type serves as the base type
        for most of the other kinds of objects defined in the Activity
        Vocabulary, including other Core types such as Activity,
        IntransitiveActivity, Collection and OrderedCollection.
        :return:
        """
        return ObjectProp.object.fget(self)

    @object.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def object(self):
        return ObjectProp.object.fget(self)

    @object.setter
    @LinkManager().setter
    def object(self, val):
        ObjectProp.object.fset(self, val)

    # //// //// //// //// //// //// subject //// //// //// //// //// ////
    @Subject.subject.getter
    @LinkManager().getter
    def subject(self):
        """
        On a Relationship object, the subject property identifies one of the
        connected individuals. For instance, for a Relationship object
        describing "John is related to Sally", subject would refer to John.
        :return: Link or Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Subject.subject.fget(self)

    @subject.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def subject(self):
        return Subject.subject.fget(self)

    @subject.setter
    @LinkManager().setter
    def subject(self, val):
        Subject.subject.fset(self, val)

    # //// //// //// //// //// //// relationship //// //// //// //// //// ////
    @RelationshipProp.relationship.getter
    @LinkManager().getter
    def relationship(self):
        """
        On a Relationship object, the relationship property identifies the kind
        of relationship that exists between subject and object.
        :return: Object
        :raises ValueError: if non-Object assignment is attempted
        """
        return RelationshipProp.relationship.fget(self)

    @relationship.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def relationship(self):
        return RelationshipProp.relationship.fget(self)

    @relationship.setter
    @LinkManager().setter
    def relationship(self, val):
        RelationshipProp.relationship.fset(self, val)


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

    @Accuracy.accuracy.getter
    def accuracy(self):
        """
        Indicates the accuracy of position coordinates on a Place objects.
        Expressed in properties of percentage. e.g. "94.0" means "94.0%
        accurate".
        :return: float
        :raises ValueError: if a non-number less than 0 or greater than 100 is assigned
        """
        return Accuracy.accuracy.fget(self)

    @accuracy.getter_context(JSON_DATA_CONTEXT)
    def accuracy(self):
        return Accuracy.accuracy.fget(self)

    @accuracy.setter
    @NumberHandler().str_to_number
    def accuracy(self, val):
        Accuracy.accuracy.fset(self, val)

    @Altitude.altitude.getter
    def altitude(self):
        """
        Indicates the altitude of a place. The measurement units is indicated
        using the units property. If units is not specified, the default is
        assumed to be "m" indicating meters.
        :return: float
        :raises ValueError: if a non-float value is assigned
        """
        return Altitude.altitude.fget(self)

    @altitude.getter_context(JSON_DATA_CONTEXT)
    def altitude(self):
        return Altitude.altitude.fget(self)

    @altitude.setter
    @NumberHandler().str_to_number
    def altitude(self, val):
        Altitude.altitude.fset(self, val)

    @Latitude.latitude.getter
    def latitude(self):
        """
        The latitude of a place
        :return: float
        :raises ValueError: if a non-float value is assigned
        """
        return Latitude.latitude.fget(self)

    @latitude.getter_context(JSON_DATA_CONTEXT)
    def latitude(self):
        return Latitude.latitude.fget(self)

    @latitude.setter
    @NumberHandler().str_to_number
    def latitude(self, val):
        Latitude.latitude.fset(self, val)

    @Longitude.longitude.getter
    def longitude(self):
        """
        The longitude of a place
        :return: float
        :raises ValueError: if a non-float value is assigned
        """
        return Longitude.longitude.fget(self)

    @longitude.getter_context(JSON_DATA_CONTEXT)
    def longitude(self):
        return Longitude.longitude.fget(self)

    @longitude.setter
    @NumberHandler().str_to_number
    def longitude(self, val):
        Longitude.longitude.fset(self, val)

    @Radius.radius.getter
    def radius(self):
        """
        The radius from the given latitude and longitude for a Place. The \
        units is expressed by the units property. If units is not specified, \
        the default is assumed to be "m" indicating "meters".
        :return: float
        :raises ValueError: if non-float or value less than 0 is assigned
        """
        return Radius.radius.fget(self)

    @radius.getter_context(JSON_DATA_CONTEXT)
    def radius(self):
        return Radius.radius.fget(self)

    @radius.setter
    @NumberHandler().str_to_number
    def radius(self, val):
        Radius.radius.fset(self, val)

    @Units.units.getter
    @LinkManager().getter
    def units(self):
        """
        Specifies the measurement units for the radius and altitude properties \
        on a Place object. If not specified, the default is assumed to be "m" \
        for "meters".
        :return: string
        :raises ValueError: if assigned value is a list, tuple, dict, or set
        """
        return Units.units.fget(self)

    @units.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def units(self):
        return Units.units.fget(self)

    @units.setter
    @LinkManager().setter
    def units(self, val):
        Units.units.fset(self, val)


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

"""
Implementation of Properties from ActivityStreams specification as native
Python objects.
"""
from datetime import datetime, timedelta
from urllib.parse import urlparse


class Id:
    """
    Provides the globally unique identifier for an Object or Link.
    """


class Type:
    """
    Identifies the Object or Link type. Multiple values may be specified.
    """


class Actor:
    """
    Describes one or more entities that either performed or are expected to
    perform the activity. Any single activity can have multiple actors. The
    actor MAY be specified using an indirect Link.
    """


class Attachment:
    """
    Identifies a resource attached or related to an object that potentially
    requires special handling. The intent is to provide a model that is at
    least semantically similar to attachments in email.
    """


class AttributedTo:
    """
    Identifies one or more entities to which this object is attributed. The
    attributed entities might not be Actors. For instance, an object might be
    attributed to the completion of another activity.
    """


class Audience:
    """
    Identifies one or more entities that represent the total population of
    entities for which the object can be considered to be relevant.
    """


class Bcc:
    """
    Identifies one or more Objects that are part of the private secondary
    audience of this Object.
    """


class Bto:
    """
    Identifies an Object that is part of the private primary audience of this
    Object.
    """


class Cc:
    """
    Identifies an Object that is part of the public secondary audience of this
    Object.
    """


class Context:
    """
    Identifies the context within which the object exists or an activity was
    performed.

    The notion of "context" used is intentionally vague. The intended function
    is to serve as a means of grouping objects and activities that share a
    common originating context or purpose. An example could be all activities
    relating to a common project or event.
    """


class Current:
    """
    In a paged Collection, indicates the page that contains the most recently
    updated member items.
    """


class First:
    """
    In a paged Collection, indicates the furthest preceding page of items in
    the collection.
    """


class Generator:
    """
    Identifies the entity (e.g. an application) that generated the object.
    """


class Icon:
    """
    Indicates an entity that describes an icon for this object. The image
    should have an aspect ratio of one (horizontal) to one (vertical) and
    should be suitable for presentation at a small size.
    """


class Image:
    """
    Indicates an entity that describes an image for this object. Unlike the
    icon property, there are no aspect ratio or display size limitations
    assumed.
    """


class InReplyTo:
    """
    Indicates one or more entities for which this object is considered a
    response.
    """


class Instrument:
    """
    Identifies one or more objects used (or to be used) in the completion of an
    Activity.
    """


class Last:
    """
    In a paged Collection, indicates the furthest proceeding page of the
    collection.
    """


class Location:
    """
    Indicates one or more physical or logical locations associated with the
    object.
    """


class Items:
    """
    Identifies the items contained in a collection. The items might be ordered
    or unordered.
    """


class OneOf:
    """
    Identifies an exclusive option for a Question. Use of oneOf implies that
    the Question can have only a single answer. To indicate that a Question can
    have multiple answers, use anyOf.
    """


class AnyOf:
    """
    Identifies an inclusive option for a Question. Use of anyOf implies that
    the Question can have multiple answers. To indicate that a Question can
    have only one answer, use oneOf.
    """


class Closed:
    """
    Indicates that a question has been closed, and answers are no longer
    accepted.
    """


class Origin:
    """
    Describes an indirect object of the activity from which the activity is
    directed. The precise meaning of the origin is the object of the English
    preposition "from". For instance, in the activity "John moved an item to
    List B from List A", the origin of the activity is "List A".
    """


class Next:
    """
    In a paged Collection, indicates the next page of items.
    """


class Object:
    """
    When used within an Activity, describes the direct object of the activity.
    For instance, in the activity "John added a movie to his wishlist", the
    object of the activity is the movie added.

    When used within a Relationship describes the entity to which the subject
    is related.
    """


class Prev:
    """
    In a paged Collection, identifies the previous page of items.
    """


class Preview:
    """
    Identifies an entity that provides a preview of this object.
    """


class Result:
    """
    Describes the result of the activity. For instance, if a particular action
    results in the creation of a new resource, the result property can be used
    to describe that new resource.
    """


class Replies:
    """
    Identifies a Collection containing objects considered to be responses to
    this object.
    """


class Tag:
    """
    One or more "tags" that have been associated with an objects. A tag can be
    any kind of Object. The key difference between attachment and tag is that
    the former implies association by inclusion, while the latter implies
    associated by reference.
    """


class Target:
    """
    Describes the indirect object, or target, of the activity. The precise
    meaning of the target is largely dependent on the type of action being
    described but will often be the object of the English preposition "to". For
    instance, in the activity "John added a movie to his wishlist", the target
    of the activity is John's wishlist. An activity can have more than one
    target.
    """


class To:
    """
    Identifies an entity considered to be part of the public primary audience
    of an Object
    """


class Url:
    """
    Identifies one or more links to representations of the object
    """


class Accuracy:
    """
    Indicates the accuracy of position coordinates on a Place objects.
    Expressed in properties of percentage. e.g. "94.0" means "94.0% accurate".
    """


class Altitude:
    """
    Indicates the altitude of a place. The measurement units is indicated
    using the units property. If units is not specified, the default is
    assumed to be "m" indicating meters.
    """


class Content:
    """
    The content or textual representation of the Object encoded as a JSON
    string. By default, the value of content is HTML. The mediaType property
    can be used in the object to indicate a different content type.

    The content MAY be expressed using multiple language-tagged values.
    """


class Name:
    """
    A simple, human-readable, plain-text name for the object. HTML markup
    MUST NOT be included. The name MAY be expressed using multiple
    language-tagged values.
    """


class Duration:
    """
    When the object describes a time-bound resource, such as an audio or video,
    a meeting, etc, the duration property indicates the object's approximate
    duration. The value MUST be expressed as an xsd:duration as defined by
    [xmlschema11-2], section 3.3.6 (e.g. a period of 5 seconds is represented
    as "PT5S").
    """


class Height:
    """
    On a Link, specifies a hint as to the rendering height in device-independent
    pixels of the linked resource.
    """


class Href:
    """
    The target resource pointed to by a Link.
    """


class HrefLang:
    """
    Hints as to the language used by the target resource. Value MUST be a
    [BCP47] Language-Tag.
    """


class PartOf:
    """
    Identifies the Collection to which a CollectionPage objects items belong.
    """


class Latitude:
    """
    The latitude of a place
    """


class Longitude:
    """
    The longitude of a place
    """


class MediaType:
    """
    When used on a Link, identifies the MIME media type of the referenced
    resource.

    When used on an Object, identifies the MIME media type of the value of the
    content property. If not specified, the content property is assumed to
    contain text/html content.
    """


class EndTime:
    """
    The date and time describing the actual or expected ending time of the
    object. When used with an Activity object, for instance, the endTime
    property specifies the moment the activity concluded or is expected to
    conclude.
    """


class Published:
    """
    The date and time at which the object was published
    """


class StartTime:
    """
    The date and time describing the actual or expected starting time of the
    object. When used with an Activity object, for instance, the startTime
    property specifies the moment the activity began or is scheduled to begin.
    """


class Radius:
    """
    The radius from the given latitude and longitude for a Place. The units is
    expressed by the units property. If units is not specified, the default is
    assumed to be "m" indicating "meters".
    """


class Rel:
    """
    A link relation associated with a Link. The value MUST conform to both the
    [HTML5] and [RFC5988] "link relation" definitions.

    In the [HTML5], any string not containing the "space" U+0020,
    "tab" (U+0009), "LF" (U+000A), "FF" (U+000C), "CR" (U+000D) or "," (U+002C)
    characters can be used as a valid link relation.
    """


class StartIndex:
    """
    A non-negative integer value identifying the relative position within the
    logical view of a strictly ordered collection.
    """


class Summary:
    """
    A natural language summarization of the object encoded as HTML. Multiple
    language tagged summaries MAY be provided.
    """


class TotalItems:
    """
    A non-negative integer specifying the total number of objects contained by
    the logical view of the collection. This number might not reflect the
    actual number of items serialized within the Collection object instance.
    """


class Units:
    """
    Specifies the measurement units for the radius and altitude properties on a
    Place object. If not specified, the default is assumed to be "m" for
    "meters".
    """


class Updated:
    """
    The date and time at which the object was updated
    """


class Width:
    """
    On a Link, specifies a hint as to the rendering width in device-independent
    pixels of the linked resource.
    """


class Subject:
    """
    On a Relationship object, the subject property identifies one of the
    connected individuals. For instance, for a Relationship object describing
    "John is related to Sally", subject would refer to John.
    """


class Relationship:
    """
    On a Relationship object, the relationship property identifies the kind of
    relationship that exists between subject and object.
    """


class Describes:
    """
    On a Profile object, the describes property identifies the object described
    by the Profile.
    """


class FormerType:
    """
    On a Tombstone object, the formerType property identifies the type of the
    object that was deleted.
    """


class Deleted:
    """
    On a Tombstone object, the deleted property is a timestamp for when the
    object was deleted.
    """

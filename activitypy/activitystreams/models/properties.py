"""
Provides data structures for ActivityStreams vocabulary objects. These objects
are not a full implementation, just an outline that ensures attributes are
handled correctly.
"""
# Yes, the docstrings for each class are directly taken from the ActivityStreams
# Vocabulary document. This whole module is intentionally barely one level of
# abstraction from the spec
import logging
from datetime import datetime, timedelta
from activitypy.jsonld import JsonProperty
from activitypy.activitystreams.models.utils import is_activity_datetime, \
    parse_activitystream_datetime, url_validator, is_nonnegative, \
    PropValidator, LinkExpander

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SECURE_URLS_ONLY = False


# "Why is this one big file? Shouldn't you break this into multiple modules?"
# I would love to, but because Properties, Activities, Actors, and Objects all
# relate to one another and everything has a clearly defined domain and range,
# any attempt to split these into separate files results in a clusterfuck of
# circular imports. Abandon hope ye who enter! This is a godless nightmare

# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# PROPERTIES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#properties
#
#   These classes describe the properties defined as part of the ActivityStreams
#   vocabulary. They ARE NOT intended to function as standalone classes and
#   exist primarily to ensure that all classes using these properties are using
#   them correctly
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class Id(JsonProperty):
    """
    Provides the globally unique identifier for an Object or Link.
    """
    __id = None

    @property
    def id(self):
        return self.__id

    @id.setter
    @PropValidator(types=(str,), functional=True, additional=(url_validator,),
                   secure=SECURE_URLS_ONLY, skip_none=True).check
    def id(self, val):
        self.__id = val


class Type(JsonProperty):
    """
    Identifies the Object or Link type. Multiple values may be specified.
    """
    __type = None

    @property
    def type(self):
        return self.__type

    @type.setter
    @PropValidator(types=(str,)).check
    def type(self, val):
        self.__type = val


class Attachment(JsonProperty):
    """
    Identifies a resource attached or related to an object that potentially
    requires special handling. The intent is to provide a model that is at
    least semantically similar to attachments in email.
    """
    __attachment = None

    @property
    def attachment(self):
        return self.__attachment

    @attachment.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def attachment(self, val):
        self.__attachment = val


class AttributedTo(JsonProperty):
    """
    Identifies one or more entities to which this object is attributed. The
    attributed entities might not be Actors. For instance, an object might be
    attributed to the completion of another activity.
    """

    __attributedTo = None

    @property
    #@LinkExpander()
    def attributedTo(self):
        return self.__attributedTo

    @attributedTo.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def attributedTo(self, val):
        self.__attributedTo = val


class Actor(AttributedTo):
    """
    Describes one or more entities that either performed or are expected to
    perform the activity. Any single activity can have multiple actors. The
    actor MAY be specified using an indirect Link.
    """

    @property
    def actor(self):
        return self.attributedTo

    @actor.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def actor(self, val):
        self.attributedTo = val


class Audience(JsonProperty):
    """
    Identifies one or more entities that represent the total population of
    entities for which the object can be considered to be relevant.
    """

    __audience = None

    @property
    def audience(self):
        return self.__audience

    @audience.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def audience(self, val):
        self.__audience = val


class Bcc(JsonProperty):
    """
    Identifies one or more Objects that are part of the private secondary
    audience of this Object.
    """

    __bcc = None

    @property
    def bcc(self):
        return self.__bcc

    @bcc.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def bcc(self, val):
        self.__bcc = val


class Bto(JsonProperty):
    """
    Identifies an Object that is part of the private primary audience of this
    Object.
    """

    __bto = None

    @property
    def bto(self):
        return self.__bto

    @bto.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def bto(self, val):
        self.__bto = val


class Cc(JsonProperty):
    """
    Identifies an Object that is part of the public secondary audience of this
    Object.
    """

    __cc = None

    @property
    def cc(self):
        return self.__cc

    @cc.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def cc(self, val):
        self.__cc = val


class Context(JsonProperty):
    """
    Identifies the context within which the object exists or an activity was
    performed.

    The notion of "context" used is intentionally vague. The intended function
    is to serve as a means of grouping objects and activities that share a
    common originating context or purpose. An example could be all activities
    relating to a common project or event.
    """

    __context = None

    @property
    def context(self):
        return self.__context

    @context.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def context(self, val):
        self.__context = val


class Current(JsonProperty):
    """
    In a paged Collection, indicates the page that contains the most recently
    updated member items.
    """

    __current = None

    @property
    def current(self):
        return self.__current

    @current.setter
    @PropValidator(types=('CollectionPageModel', 'LinkModel'),
                   functional=True).check
    def current(self, val):
        self.__current = val


class First(JsonProperty):
    """
    In a paged Collection, indicates the furthest preceding page of items in
    the collection.
    """

    __first = None

    @property
    def first(self):
        return self.__first

    @first.setter
    @PropValidator(types=('CollectionPageModel', 'LinkModel'),
                   functional=True).check
    def first(self, val):
        self.__first = val


class Generator(JsonProperty):
    """
    Identifies the entity (e.g. an application) that generated the object.
    """

    __generator = None

    @property
    def generator(self):
        return self.__generator

    @generator.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def generator(self, val):
        self.__generator = val


class Icon(JsonProperty):
    """
    Indicates an entity that describes an icon for this object. The image
    should have an aspect ratio of one (horizontal) to one (vertical) and
    should be suitable for presentation at a small size.
    """

    __icon = None

    @property
    def icon(self):
        return self.__icon

    @icon.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def icon(self, val):
        self.__icon = val


class Image(JsonProperty):
    """
    Indicates an entity that describes an image for this object. Unlike the
    icon property, there are no aspect ratio or display size limitations
    assumed.
    """

    __image = None

    @property
    def image(self):
        return self.__image

    @image.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def image(self, val):
        self.__image = val


class InReplyTo(JsonProperty):
    """
    Indicates one or more entities for which this object is considered a
    response.
    """

    __inReplyTo = None

    @property
    def inReplyTo(self):
        return self.__inReplyTo

    @inReplyTo.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def inReplyTo(self, val):
        self.__inReplyTo = val


class Instrument(JsonProperty):
    """
    Identifies one or more objects used (or to be used) in the completion of an
    Activity.
    """

    __instrument = None

    @property
    def instrument(self):
        return self.__instrument

    @instrument.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def instrument(self, val):
        self.__instrument = val


class Last(JsonProperty):
    """
    In a paged Collection, indicates the furthest proceeding page of the
    collection.
    """

    __last = None

    @property
    def last(self):
        return self.__last

    @last.setter
    @PropValidator(types=('CollectionPageModel', 'LinkModel'),
                   functional=True).check
    def last(self, val):
        self.__last = val


class Location(JsonProperty):
    """
    Indicates one or more physical or logical locations associated with the
    object.
    """

    __location = None

    @property
    def location(self):
        return self.__location

    @location.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def location(self, val):
        self.__location = val


class Items(JsonProperty):
    """
    Identifies the items contained in a collection. The items might be ordered
    or unordered.
    """

    __items = None

    @property
    def items(self):
        return self.__items

    @items.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def items(self, val):
        self.__items = val


class OrderedItems(Items):
    """
    Identifies the items contained in a collection. The items might be ordered
    or unordered.
    """

    # this is essentially just a wrapper for "items"
    @property
    def orderedItems(self):
        return self.items

    @orderedItems.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def orderedItems(self, val):
        self.items = val


class UnorderedItems(JsonProperty):
    """
    Identifies the items contained in a collection. The items might be ordered
    or unordered.
    """

    __unorderedItems = None

    @property
    def unorderedItems(self):
        return self.__unorderedItems

    @unorderedItems.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def unorderedItems(self, val):
        self.__unorderedItems = val


class OneOf(JsonProperty):
    """
    Identifies an exclusive option for a Question. Use of oneOf implies that
    the Question can have only a single answer. To indicate that a Question can
    have multiple answers, use anyOf.
    """

    __oneOf = None

    @property
    def oneOf(self):
        return self.__oneOf

    @oneOf.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def oneOf(self, val):
        self.__oneOf = val


class AnyOf(JsonProperty):
    """
    Identifies an inclusive option for a Question. Use of anyOf implies that
    the Question can have multiple answers. To indicate that a Question can
    have only one answer, use oneOf.
    """

    __anyOf = None

    @property
    def anyOf(self):
        return self.__anyOf

    @anyOf.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def anyOf(self, val):
        self.__anyOf = val


class Closed(JsonProperty):
    """
    Indicates that a question has been closed, and answers are no longer
    accepted.
    """

    __closed = None

    @property
    def closed(self):
        return self.__closed

    @closed.setter
    @PropValidator(types=('ObjectModel', 'LinkModel', datetime, bool)).check
    def closed(self, val):
        self.__closed = val


class Origin(JsonProperty):
    """
    Describes an indirect object of the activity from which the activity is
    directed. The precise meaning of the origin is the object of the English
    preposition "from". For instance, in the activity "John moved an item to
    List B from List A", the origin of the activity is "List A".
    """

    __origin = None

    @property
    def origin(self):
        return self.__origin

    @origin.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def origin(self, val):
        self.__origin = val


class Next(JsonProperty):
    """
    In a paged Collection, indicates the next page of items.
    """

    __next = None

    @property
    def next(self):
        return self.__next

    @next.setter
    @PropValidator(types=('CollectionPageModel', 'LinkModel'),
                   functional=True).check
    def next(self, val):
        self.__next = val


class Object(JsonProperty):
    """
    When used within an Activity, describes the direct object of the activity.
    For instance, in the activity "John added a movie to his wishlist", the
    object of the activity is the movie added.

    When used within a Relationship describes the entity to which the subject
    is related.
    """

    __object = None

    @property
    def object(self):
        return self.__object

    @object.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def object(self, val):
        self.__object = val


class Prev(JsonProperty):
    """
    In a paged Collection, identifies the previous page of items.
    """

    __prev = None

    @property
    def prev(self):
        return self.__prev

    @prev.setter
    @PropValidator(types=('CollectionPageModel', 'LinkModel'),
                   functional=True).check
    def prev(self, val):
        self.__prev = val


class Preview(JsonProperty):
    """
    Identifies an entity that provides a preview of this object.
    """

    __preview = None

    @property
    def preview(self):
        return self.__preview

    @preview.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def preview(self, val):
        self.__preview = val


class Result(JsonProperty):
    """
    Describes the result of the activity. For instance, if a particular action
    results in the creation of a new resource, the result property can be used
    to describe that new resource.
    """

    __result = None

    @property
    def result(self):
        return self.__result

    @result.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def result(self, val):
        self.__result = val


class Replies(JsonProperty):
    """
    Identifies a Collection containing objects considered to be responses to
    this object.
    """

    __replies = None

    @property
    def replies(self):
        return self.__replies

    @replies.setter
    @PropValidator(types=('CollectionModel',), functional=True).check
    def replies(self, val):
        self.__replies = val


class Tag(JsonProperty):
    """
    One or more "tags" that have been associated with an objects. A tag can be
    any kind of Object. The key difference between attachment and tag is that
    the former implies association by inclusion, while the latter implies
    associated by reference.
    """

    __tag = None

    @property
    def tag(self):
        return self.__tag

    @tag.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def tag(self, val):
        self.__tag = val


class Target(JsonProperty):
    """
    Describes the indirect object, or target, of the activity. The precise
    meaning of the target is largely dependent on the type of action being
    described but will often be the object of the English preposition "to". For
    instance, in the activity "John added a movie to his wishlist", the target
    of the activity is John's wishlist. An activity can have more than one
    target.
    """

    __target = None

    @property
    def target(self):
        return self.__target

    @target.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def target(self, val):
        self.__target = val


class To(JsonProperty):
    """
    Identifies an entity considered to be part of the public primary audience
    of an Object
    """

    __to = None

    @property
    def to(self):
        return self.__to

    @to.setter
    @PropValidator(types=('ObjectModel', 'LinkModel')).check
    def to(self, val):
        self.__to = val


class Url(JsonProperty):
    """
    Identifies one or more links to representations of the object
    """

    __url = None

    @property
    def url(self):
        return self.__url

    @url.setter
    @PropValidator(types=('LinkModel', str)).check
    def url(self, val):
        self.__url = val


class Accuracy(JsonProperty):
    """
    Indicates the accuracy of position coordinates on a Place objects.
    Expressed in properties of percentage. e.g. "94.0" means "94.0% accurate".
    """

    __accuracy = None

    @property
    def accuracy(self):
        return self.__accuracy

    @accuracy.setter
    @PropValidator(types=(float, int), functional=True).check
    def accuracy(self, val):
        self.__accuracy = val


class Altitude(JsonProperty):
    """
    Indicates the altitude of a place. The measurement units is indicated
    using the units property. If units is not specified, the default is
    assumed to be "m" indicating meters.
    """

    __altitude = None

    @property
    def altitude(self):
        return self.__altitude

    @altitude.setter
    @PropValidator(types=(float, int), functional=True).check
    def altitude(self, val):
        self.__altitude = val


class Content(JsonProperty):
    """
    The content or textual representation of the Object encoded as a JSON
    string. By default, the value of content is HTML. The mediaType property
    can be used in the object to indicate a different content type.

    The content MAY be expressed using multiple language-tagged values.
    """

    __content = None

    @property
    def content(self):
        return self.__content

    @content.setter
    @PropValidator(types=(str,)).check
    def content(self, val):
        self.__content = val


class Name(JsonProperty):
    """
    A simple, human-readable, plain-text name for the object. HTML markup
    MUST NOT be included. The name MAY be expressed using multiple
    language-tagged values.
    """

    __name = None

    @property
    def name(self):
        return self.__name

    @name.setter
    @PropValidator(types=(str, dict)).check
    def name(self, val):
        self.__name = val


class Duration(JsonProperty):
    """
    When the object describes a time-bound resource, such as an audio or video,
    a meeting, etc., the duration property indicates the object's approximate
    duration. The value MUST be expressed as an xsd:duration as defined by
    [xmlschema11-2], section 3.3.6 (e.g. a period of 5 seconds is represented
    as "PT5S").
    """

    __duration = None

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    @PropValidator(types=(timedelta, str), functional=True).check
    def duration(self, val):
        self.__duration = val


class Height(JsonProperty):
    """
    On a Link, specifies a hint as to the rendering height in device-independent
    pixels of the linked resource.
    """

    __height = None

    @property
    def height(self):
        return self.__height

    @height.setter
    @PropValidator(types=(int,), functional=True,
                   additional=(is_nonnegative,)).check
    def height(self, val):
        self.__height = val


class Href(JsonProperty):
    """
    The target resource pointed to by a Link.
    """

    __href = None

    @property
    def href(self):
        return self.__href

    @href.setter
    @PropValidator(types=(str,), functional=True).check
    def href(self, val):
        self.__href = val


class HrefLang(JsonProperty):
    """
    Hints as to the language used by the target resource. Value MUST be a
    [BCP47] Language-Tag.
    """

    __hrefLang = None

    @property
    def hreflang(self):
        return self.__hrefLang

    @hreflang.setter
    @PropValidator(types=(str,), functional=True).check
    def hreflang(self, val):
        self.__hrefLang = val


class PartOf(JsonProperty):
    """
    Identifies the Collection to which a CollectionPage objects items belong.
    """

    __partOf = None

    @property
    def partOf(self):
        return self.__partOf

    @partOf.setter
    @PropValidator(types=('CollectionModel', 'LinkModel'), functional=True).check
    def partOf(self, val):
        self.__partOf = val


class Latitude(JsonProperty):
    """
    The latitude of a place
    """

    __latitude = None

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    @PropValidator(types=(float, int), functional=True).check
    def latitude(self, val):
        self.__latitude = val


class Longitude(JsonProperty):
    """
    The longitude of a place
    """

    __longitude = None

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    @PropValidator(types=(float, int), functional=True).check
    def longitude(self, val):
        self.__longitude = val


class MediaType(JsonProperty):
    """
    When used on a Link, identifies the MIME media type of the referenced
    resource.

    When used on an Object, identifies the MIME media type of the value of the
    content property. If not specified, the content property is assumed to
    contain text/html content.
    """

    __mediaType = 'text/html'

    @property
    def mediaType(self):
        return self.__mediaType

    @mediaType.setter
    @PropValidator(types=(str,), functional=True).check
    def mediaType(self, val):
        self.__mediaType = val


class EndTime(JsonProperty):
    """
    The date and time describing the actual or expected ending time of the
    object. When used with an Activity object, for instance, the endTime
    property specifies the moment the activity concluded or is expected to
    conclude.
    """

    __endTime = None

    @property
    def endTime(self):
        return self.__endTime

    @endTime.setter
    @PropValidator(types=(datetime, str), functional=True,
                   additional=(is_activity_datetime,)).check
    def endTime(self, val):
        self.__endTime = parse_activitystream_datetime(val)


class Published(JsonProperty):
    """
    The date and time at which the object was published
    """

    __published = None

    @property
    def published(self):
        return self.__published

    @published.setter
    @PropValidator(types=(datetime, str), functional=True,
                   additional=(is_activity_datetime,)).check
    def published(self, val):
        self.__published = parse_activitystream_datetime(val)


class StartTime(JsonProperty):
    """
    The date and time describing the actual or expected starting time of the
    object. When used with an Activity object, for instance, the startTime
    property specifies the moment the activity began or is scheduled to begin.
    """

    __startTime = None

    @property
    def startTime(self):
        return self.__startTime

    @startTime.setter
    @PropValidator(types=(datetime, str), functional=True,
                   additional=(is_activity_datetime,)).check
    def startTime(self, val):
        self.__startTime = parse_activitystream_datetime(val)


class Radius(JsonProperty):
    """
    The radius from the given latitude and longitude for a Place. The units are
    expressed by the units property. If units is not specified, the default is
    assumed to be "m" indicating "meters".
    """

    __radius = None

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    @PropValidator(types=(float, int), functional=True,
                   additional=(is_nonnegative,)).check
    def radius(self, val):
        self.__radius = val


class Rel(JsonProperty):
    """
    A link relation associated with a Link. The value MUST conform to both the
    [HTML5] and [RFC5988] "link relation" definitions.

    In the [HTML5], any string not containing the "space" U+0020,
    "tab" (U+0009), "LF" (U+000A), "FF" (U+000C), "CR" (U+000D) or "," (U+002C)
    characters can be used as a valid link relation.
    """

    __rel = None

    @property
    def rel(self):
        return self.__rel

    @rel.setter
    @PropValidator(types=(str,)).check
    def rel(self, val):
        self.__rel = val


class StartIndex(JsonProperty):
    """
    A non-negative integer value identifying the relative position within the
    logical view of a strictly ordered collection.
    """

    __startIndex = None

    @property
    def startIndex(self):
        return self.__startIndex

    @startIndex.setter
    @PropValidator(types=(int,), functional=True,
                   additional=(is_nonnegative,)).check
    def startIndex(self, val):
        self.__startIndex = val


class Summary(JsonProperty):
    """
    A natural language summarization of the object encoded as HTML. Multiple
    language tagged summaries MAY be provided.
    """

    __summary = None

    @property
    def summary(self):
        return self.__summary

    @summary.setter
    @PropValidator(types=(str,)).check
    def summary(self, val):
        self.__summary = val


class TotalItems(JsonProperty):
    """
    A non-negative integer specifying the total number of objects contained by
    the logical view of the collection. This number might not reflect the
    actual number of items serialized within the Collection object instance.
    """

    __totalItems = None

    @property
    def totalItems(self):
        return self.__totalItems

    @totalItems.setter
    @PropValidator(types=(int,), functional=True,
                   additional=(is_nonnegative,)).check
    def totalItems(self, val):
        self.__totalItems = val


class Units(JsonProperty):
    """
    Specifies the measurement units for the radius and altitude properties on a
    Place object. If not specified, the default is assumed to be "m" for
    "meters".
    """

    __units = None

    @property
    def units(self):
        return self.__units

    @units.setter
    @PropValidator(types=(str,), functional=True).check
    def units(self, val):
        self.__units = val


class Updated(JsonProperty):
    """
    The date and time at which the object was updated
    """

    __updated = None

    @property
    def updated(self):
        return self.__updated

    @updated.setter
    @PropValidator(types=(datetime, str), functional=True,
                   additional=(is_activity_datetime,)).check
    def updated(self, val):
        self.__updated = parse_activitystream_datetime(val)


class Width(JsonProperty):
    """
    On a Link, specifies a hint as to the rendering width in device-independent
    pixels of the linked resource.
    """

    __width = None

    @property
    def width(self):
        return self.__width

    @width.setter
    @PropValidator(types=(int,), functional=True,
                   additional=(is_nonnegative,)).check
    def width(self, val):
        self.__width = val


class Subject(JsonProperty):
    """
    On a Relationship object, the subject property identifies one of the
    connected individuals. For instance, for a Relationship object describing
    "John is related to Sally", subject would refer to John.
    """

    __subject = None

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    @PropValidator(types=('ObjectModel', 'LinkModel'), functional=True).check
    def subject(self, val):
        self.__subject = val


class Relationship(JsonProperty):
    """
    On a Relationship object, the relationship property identifies the kind of
    relationship that exists between subject and object.
    """

    __relationship = None

    @property
    def relationship(self):
        return self.__relationship

    @relationship.setter
    @PropValidator(types=('ObjectModel',)).check
    def relationship(self, val):
        self.__relationship = val


class Describes(JsonProperty):
    """
    On a Profile object, the describes property identifies the object described
    by the Profile.
    """

    __describes = None

    @property
    def describes(self):
        return self.__describes

    @describes.setter
    @PropValidator(types=('ObjectModel',), functional=True).check
    def describes(self, val):
        self.__describes = val


class FormerType(JsonProperty):
    """
    On a Tombstone object, the formerType property identifies the type of the
    object that was deleted.
    """

    __formerType = None

    @property
    def formerType(self):
        return self.__formerType

    @formerType.setter
    @PropValidator(types=('ObjectModel',)).check
    def formerType(self, val):
        self.__formerType = val


class Deleted(JsonProperty):
    """
    On a Tombstone object, the deleted property is a timestamp for when the
    object was deleted.
    """

    __deleted = None

    @property
    def deleted(self):
        return self.__deleted

    @deleted.setter
    @PropValidator(types=(datetime,), functional=True,
                   additional=(is_activity_datetime,)).check
    def deleted(self, val):
        self.__deleted = val

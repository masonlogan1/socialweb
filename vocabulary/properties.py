"""
Implementation of Properties from ActivityStreams specification as native
Python objects.
"""
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# IMPORTANT NOTE: None of these are intended to be used directly! They exist
# purely as a way of allowing us to compose classes that use a collection of
# shared properties
class Id:
    """
    Provides the globally unique identifier for an Object or Link.
    """
    @property
    def id(self):
        return getattr(self, '_id', '')

    @id.setter
    def id(self, value):
        logger.debug(f'setting "id" of {self} to {value}')
        self._id = value


class Type:
    """
    Identifies the Object or Link type. Multiple values may be specified.
    """
    @property
    def type(self):
        return getattr(self, '_type', '')

    @type.setter
    def type(self, type):
        self._type = type


class Actor:
    """
    Describes one or more entities that either performed or are expected to
    perform the activity. Any single activity can have multiple actors. The
    actor MAY be specified using an indirect Link.
    """
    @property
    def actor(self):
        return getattr(self, '_actor', '')

    @actor.setter
    def actor(self, actor):
        self._actor = actor


class Attachment:
    """
    Identifies a resource attached or related to an object that potentially
    requires special handling. The intent is to provide a model that is at
    least semantically similar to attachments in email.
    """
    @property
    def attachment(self):
        return getattr(self, '_attachment', '')

    @attachment.setter
    def attachment(self, attachment):
        self._attachment = attachment


class AttributedTo:
    """
    Identifies one or more entities to which this object is attributed. The
    attributed entities might not be Actors. For instance, an object might be
    attributed to the completion of another activity.
    """
    @property
    def attributedTo(self):
        return getattr(self, '_attributedTo', '')

    @attributedTo.setter
    def attributedTo(self, attributedTo):
        self._attributedTo = attributedTo


class Audience:
    """
    Identifies one or more entities that represent the total population of
    entities for which the object can be considered to be relevant.
    """
    @property
    def audience(self):
        return getattr(self, '_audience', '')

    @audience.setter
    def audience(self, audience):
        self._audience = audience


class Bcc:
    """
    Identifies one or more Objects that are part of the private secondary
    audience of this Object.
    """
    @property
    def bcc(self):
        return getattr(self, '_bcc', '')

    @bcc.setter
    def bcc(self, bcc):
        self._bcc = bcc


class Bto:
    """
    Identifies an Object that is part of the private primary audience of this
    Object.
    """
    @property
    def bto(self):
        return getattr(self, '_bto', '')

    @bto.setter
    def bto(self, bto):
        self._bto = bto


class Cc:
    """
    Identifies an Object that is part of the public secondary audience of this
    Object.
    """
    @property
    def cc(self):
        return getattr(self, '_cc', '')

    @cc.setter
    def cc(self, cc):
        self._cc = cc


class Context:
    """
    Identifies the context within which the object exists or an activity was
    performed.

    The notion of "context" used is intentionally vague. The intended function
    is to serve as a means of grouping objects and activities that share a
    common originating context or purpose. An example could be all activities
    relating to a common project or event.
    """
    @property
    def context(self):
        return getattr(self, '_context', '')

    @context.setter
    def context(self, context):
        self._context = context


class Current:
    """
    In a paged Collection, indicates the page that contains the most recently
    updated member items.
    """
    @property
    def current(self):
        return getattr(self, '_current', '')

    @current.setter
    def current(self, current):
        self._current = current


class First:
    """
    In a paged Collection, indicates the furthest preceding page of items in
    the collection.
    """
    @property
    def first(self):
        return getattr(self, '_first', '')

    @first.setter
    def first(self, first):
        self._first = first


class Generator:
    """
    Identifies the entity (e.g. an application) that generated the object.
    """
    @property
    def generator(self):
        return getattr(self, '_generator', '')

    @generator.setter
    def generator(self, generator):
        self._generator = generator


class Icon:
    """
    Indicates an entity that describes an icon for this object. The image
    should have an aspect ratio of one (horizontal) to one (vertical) and
    should be suitable for presentation at a small size.
    """
    @property
    def icon(self):
        return getattr(self, '_icon', '')

    @icon.setter
    def icon(self, icon):
        self._icon = icon


class Image:
    """
    Indicates an entity that describes an image for this object. Unlike the
    icon property, there are no aspect ratio or display size limitations
    assumed.
    """
    @property
    def image(self):
        return getattr(self, '_image', '')

    @image.setter
    def image(self, image):
        self._image = image


class InReplyTo:
    """
    Indicates one or more entities for which this object is considered a
    response.
    """
    @property
    def inReplyTo(self):
        return getattr(self, '_inReplyTo', '')

    @inReplyTo.setter
    def inReplyTo(self, inReplyTo):
        self._inReplyTo = inReplyTo


class Instrument:
    """
    Identifies one or more objects used (or to be used) in the completion of an
    Activity.
    """
    @property
    def instrument(self):
        return getattr(self, '_instrument', '')

    @instrument.setter
    def instrument(self, instrument):
        self._instrument = instrument


class Last:
    """
    In a paged Collection, indicates the furthest proceeding page of the
    collection.
    """
    @property
    def last(self):
        return getattr(self, '_last', '')

    @last.setter
    def last(self, last):
        self._last = last


class Location:
    """
    Indicates one or more physical or logical locations associated with the
    object.
    """
    @property
    def location(self):
        return getattr(self, '_location', '')

    @location.setter
    def location(self, location):
        self._location = location


class Items:
    """
    Identifies the items contained in a collection. The items might be ordered
    or unordered.
    """
    @property
    def items(self):
        return getattr(self, '_items', '')

    @items.setter
    def items(self, items):
        self._items = items


class OneOf:
    """
    Identifies an exclusive option for a Question. Use of oneOf implies that
    the Question can have only a single answer. To indicate that a Question can
    have multiple answers, use anyOf.
    """
    @property
    def oneOf(self):
        return getattr(self, '_oneOf', '')

    @oneOf.setter
    def oneOf(self, oneOf):
        self._oneOf = oneOf


class AnyOf:
    """
    Identifies an inclusive option for a Question. Use of anyOf implies that
    the Question can have multiple answers. To indicate that a Question can
    have only one answer, use oneOf.
    """
    @property
    def anyOf(self):
        return getattr(self, '_anyOf', '')

    @anyOf.setter
    def anyOf(self, anyOf):
        self._anyOf = anyOf


class Closed:
    """
    Indicates that a question has been closed, and answers are no longer
    accepted.
    """
    @property
    def closed(self):
        return getattr(self, '_closed', '')

    @closed.setter
    def closed(self, closed):
        self._closed = closed


class Origin:
    """
    Describes an indirect object of the activity from which the activity is
    directed. The precise meaning of the origin is the object of the English
    preposition "from". For instance, in the activity "John moved an item to
    List B from List A", the origin of the activity is "List A".
    """
    @property
    def origin(self):
        return getattr(self, '_origin', '')

    @origin.setter
    def origin(self, origin):
        self._origin = origin


class Next:
    """
    In a paged Collection, indicates the next page of items.
    """
    @property
    def next(self):
        return getattr(self, '_next', '')

    @next.setter
    def next(self, next):
        self._next = next


class Object:
    """
    When used within an Activity, describes the direct object of the activity.
    For instance, in the activity "John added a movie to his wishlist", the
    object of the activity is the movie added.

    When used within a Relationship describes the entity to which the subject
    is related.
    """
    @property
    def object(self):
        return getattr(self, '_object', '')

    @object.setter
    def object(self, object):
        self._object = object


class Prev:
    """
    In a paged Collection, identifies the previous page of items.
    """
    @property
    def prev(self):
        return getattr(self, '_prev', '')

    @prev.setter
    def prev(self, prev):
        self._prev = prev


class Preview:
    """
    Identifies an entity that provides a preview of this object.
    """
    @property
    def preview(self):
        return getattr(self, '_preview', '')

    @preview.setter
    def preview(self, preview):
        self._preview = preview


class Result:
    """
    Describes the result of the activity. For instance, if a particular action
    results in the creation of a new resource, the result property can be used
    to describe that new resource.
    """
    @property
    def result(self):
        return getattr(self, '_result', '')

    @result.setter
    def result(self, result):
        self._result = result


class Replies:
    """
    Identifies a Collection containing objects considered to be responses to
    this object.
    """
    @property
    def replies(self):
        return getattr(self, '_replies', '')

    @replies.setter
    def replies(self, replies):
        self._replies = replies


class Tag:
    """
    One or more "tags" that have been associated with an objects. A tag can be
    any kind of Object. The key difference between attachment and tag is that
    the former implies association by inclusion, while the latter implies
    associated by reference.
    """
    @property
    def tag(self):
        return getattr(self, '_tag', '')

    @tag.setter
    def tag(self, tag):
        self._tag = tag


class Target:
    """
    Describes the indirect object, or target, of the activity. The precise
    meaning of the target is largely dependent on the type of action being
    described but will often be the object of the English preposition "to". For
    instance, in the activity "John added a movie to his wishlist", the target
    of the activity is John's wishlist. An activity can have more than one
    target.
    """
    @property
    def target(self):
        return getattr(self, '_target', '')

    @target.setter
    def target(self, target):
        self._target = target


class To:
    """
    Identifies an entity considered to be part of the public primary audience
    of an Object
    """
    @property
    def to(self):
        return getattr(self, '_to', '')

    @to.setter
    def to(self, to):
        self._to = to


class Url:
    """
    Identifies one or more links to representations of the object
    """
    @property
    def url(self):
        return getattr(self, '_url', '')

    @url.setter
    def url(self, url):
        self._url = url


class Accuracy:
    """
    Indicates the accuracy of position coordinates on a Place objects.
    Expressed in properties of percentage. e.g. "94.0" means "94.0% accurate".
    """
    @property
    def accuracy(self):
        return getattr(self, '_accuracy', '')

    @accuracy.setter
    def accuracy(self, accuracy):
        self._accuracy = accuracy


class Altitude:
    """
    Indicates the altitude of a place. The measurement units is indicated
    using the units property. If units is not specified, the default is
    assumed to be "m" indicating meters.
    """
    @property
    def altitude(self):
        return getattr(self, '_altitude', '')

    @altitude.setter
    def altitude(self, altitude):
        self._altitude = altitude


class Content:
    """
    The content or textual representation of the Object encoded as a JSON
    string. By default, the value of content is HTML. The mediaType property
    can be used in the object to indicate a different content type.

    The content MAY be expressed using multiple language-tagged values.
    """
    @property
    def content(self):
        return getattr(self, '_content', '')

    @content.setter
    def content(self, content):
        self._content = content


class Name:
    """
    A simple, human-readable, plain-text name for the object. HTML markup
    MUST NOT be included. The name MAY be expressed using multiple
    language-tagged values.
    """
    @property
    def name(self):
        return getattr(self, '_name', '')

    @name.setter
    def name(self, name):
        self._name = name


class Duration:
    """
    When the object describes a time-bound resource, such as an audio or video,
    a meeting, etc, the duration property indicates the object's approximate
    duration. The value MUST be expressed as an xsd:duration as defined by
    [xmlschema11-2], section 3.3.6 (e.g. a period of 5 seconds is represented
    as "PT5S").
    """
    @property
    def duration(self):
        return getattr(self, '_duration', '')

    @duration.setter
    def duration(self, duration):
        self._duration = duration


class Height:
    """
    On a Link, specifies a hint as to the rendering height in device-independent
    pixels of the linked resource.
    """
    @property
    def height(self):
        return getattr(self, '_height', '')

    @height.setter
    def height(self, height):
        self._height = height


class Href:
    """
    The target resource pointed to by a Link.
    """
    @property
    def href(self):
        return getattr(self, '_href', '')

    @href.setter
    def href(self, href):
        self._href = href


class HrefLang:
    """
    Hints as to the language used by the target resource. Value MUST be a
    [BCP47] Language-Tag.
    """
    @property
    def hreflang(self):
        return getattr(self, '_hreflang', '')

    @hreflang.setter
    def hreflang(self, hreflang):
        self._hreflang = hreflang


class PartOf:
    """
    Identifies the Collection to which a CollectionPage objects items belong.
    """
    @property
    def partOf(self):
        return getattr(self, '_partOf', '')

    @partOf.setter
    def partOf(self, partOf):
        self._partOf = partOf


class Latitude:
    """
    The latitude of a place
    """
    @property
    def latitude(self):
        return getattr(self, '_latitude', '')

    @latitude.setter
    def latitude(self, latitude):
        self._latitude = latitude


class Longitude:
    """
    The longitude of a place
    """
    @property
    def longitude(self):
        return getattr(self, '_longitude', '')

    @longitude.setter
    def longitude(self, longitude):
        self._longitude = longitude


class MediaType:
    """
    When used on a Link, identifies the MIME media type of the referenced
    resource.

    When used on an Object, identifies the MIME media type of the value of the
    content property. If not specified, the content property is assumed to
    contain text/html content.
    """
    @property
    def mediaType(self):
        return getattr(self, '_mediaType', '')

    @mediaType.setter
    def mediaType(self, mediaType):
        self._mediaType = mediaType


class EndTime:
    """
    The date and time describing the actual or expected ending time of the
    object. When used with an Activity object, for instance, the endTime
    property specifies the moment the activity concluded or is expected to
    conclude.
    """
    @property
    def endTime(self):
        return getattr(self, '_endTime', '')

    @endTime.setter
    def endTime(self, endTime):
        self._endTime = endTime


class Published:
    """
    The date and time at which the object was published
    """
    @property
    def published(self):
        return getattr(self, '_published', '')

    @published.setter
    def published(self, published):
        self._published = published


class StartTime:
    """
    The date and time describing the actual or expected starting time of the
    object. When used with an Activity object, for instance, the startTime
    property specifies the moment the activity began or is scheduled to begin.
    """
    @property
    def startTime(self):
        return getattr(self, '_startTime', '')

    @startTime.setter
    def startTime(self, startTime):
        self._startTime = startTime


class Radius:
    """
    The radius from the given latitude and longitude for a Place. The units is
    expressed by the units property. If units is not specified, the default is
    assumed to be "m" indicating "meters".
    """
    @property
    def radius(self):
        return getattr(self, '_radius', '')

    @radius.setter
    def radius(self, radius):
        self._radius = radius


class Rel:
    """
    A link relation associated with a Link. The value MUST conform to both the
    [HTML5] and [RFC5988] "link relation" definitions.

    In the [HTML5], any string not containing the "space" U+0020,
    "tab" (U+0009), "LF" (U+000A), "FF" (U+000C), "CR" (U+000D) or "," (U+002C)
    characters can be used as a valid link relation.
    """
    @property
    def rel(self):
        return getattr(self, '_rel', '')

    @rel.setter
    def rel(self, rel):
        self._rel = rel


class StartIndex:
    """
    A non-negative integer value identifying the relative position within the
    logical view of a strictly ordered collection.
    """
    @property
    def startIndex(self):
        return getattr(self, '_startIndex', '')

    @startIndex.setter
    def startIndex(self, startIndex):
        self._startIndex = startIndex


class Summary:
    """
    A natural language summarization of the object encoded as HTML. Multiple
    language tagged summaries MAY be provided.
    """
    @property
    def summary(self):
        return getattr(self, '_summary', '')

    @summary.setter
    def summary(self, summary):
        self._summary = summary


class TotalItems:
    """
    A non-negative integer specifying the total number of objects contained by
    the logical view of the collection. This number might not reflect the
    actual number of items serialized within the Collection object instance.
    """
    @property
    def totalItems(self):
        return getattr(self, '_totalItems', '')

    @totalItems.setter
    def totalItems(self, totalItems):
        self._totalItems = totalItems


class Units:
    """
    Specifies the measurement units for the radius and altitude properties on a
    Place object. If not specified, the default is assumed to be "m" for
    "meters".
    """
    @property
    def units(self):
        return getattr(self, '_units', '')

    @units.setter
    def units(self, units):
        self._units = units


class Updated:
    """
    The date and time at which the object was updated
    """
    @property
    def updated(self):
        return getattr(self, '_updated', '')

    @updated.setter
    def updated(self, updated):
        self._updated = updated


class Width:
    """
    On a Link, specifies a hint as to the rendering width in device-independent
    pixels of the linked resource.
    """
    @property
    def width(self):
        return getattr(self, '_width', '')

    @width.setter
    def width(self, width):
        self._width = width


class Subject:
    """
    On a Relationship object, the subject property identifies one of the
    connected individuals. For instance, for a Relationship object describing
    "John is related to Sally", subject would refer to John.
    """
    @property
    def subject(self):
        return getattr(self, '_subject', '')

    @subject.setter
    def subject(self, subject):
        self._subject = subject


class Relationship:
    """
    On a Relationship object, the relationship property identifies the kind of
    relationship that exists between subject and object.
    """
    @property
    def relationship(self):
        return getattr(self, '_relationship', '')

    @relationship.setter
    def relationship(self, relationship):
        self._relationship = relationship


class Describes:
    """
    On a Profile object, the describes property identifies the object described
    by the Profile.
    """
    @property
    def describes(self):
        return getattr(self, '_describes', '')

    @describes.setter
    def describes(self, describes):
        self._describes = describes


class FormerType:
    """
    On a Tombstone object, the formerType property identifies the type of the
    object that was deleted.
    """
    @property
    def formerType(self):
        return getattr(self, '_formerType', '')

    @formerType.setter
    def formerType(self, formerType):
        self._formerType = formerType


class Deleted:
    """
    On a Tombstone object, the deleted property is a timestamp for when the
    object was deleted.
    """
    @property
    def deleted(self):
        return getattr(self, '_deleted', '')

    @deleted.setter
    def deleted(self, deleted):
        self._deleted = deleted

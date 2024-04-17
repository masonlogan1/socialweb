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
from jsonld import JsonProperty, contextualproperty, \
    JSON_DATA_CONTEXT
from jsonld.tools import validate_url
from jsonld.tools import is_activity_datetime, \
    parse_activitystream_datetime, datetime_str, timedelta_str
from jsonld.tools import is_nonnegative
from jsonld.tools import SetterValidator

from activitystreams.models import Object, Link, Collection, \
    CollectionPage, ACTIVITYSTREAMS_NS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SECURE_URLS_ONLY = False


class ActivityStreamsProperty(JsonProperty):
    @classmethod
    def __get_namespace__(cls):
        # provides namespacing logic for ALL derived children
        return f'{ACTIVITYSTREAMS_NS}#dfn-{cls.__get_property_name__()}'


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

class Id(ActivityStreamsProperty):
    """
    Provides the globally unique identifier for an Object or Link.
    """
    @contextualproperty
    def id(self):
        return getattr(self, '___id___', None)

    @id.setter
    @SetterValidator(types=(str,), functional=True, additional=(validate_url,),
                     secure=SECURE_URLS_ONLY, skip_none=True).check
    def id(self, val):
        setattr(self, '___id___', val)


class Type(ActivityStreamsProperty):
    """
    Identifies the Object or Link type. Multiple values may be specified.
    """
    @contextualproperty
    def type(self):
        return getattr(self, '__type___', None)

    @type.setter
    @SetterValidator(types=(str,)).check
    def type(self, val):
        setattr(self, '__type___', val)


class Attachment(ActivityStreamsProperty):
    """
    Identifies a resource attached or related to an object that potentially
    requires special handling. The intent is to provide a model that is at
    least semantically similar to attachments in email.
    """

    @contextualproperty
    @Link.expand
    def attachment(self):
        return getattr(self, '___attachment___', None)

    @attachment.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def attachment(self):
        return getattr(self, '___attachment___', None)

    @attachment.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def attachment(self, val):
        self.___attachment___ = val


class AttributedTo(ActivityStreamsProperty):
    """
    Identifies one or more entities to which this object is attributed. The
    attributed entities might not be Actors. For instance, an object might be
    attributed to the completion of another activity.
    """

    @contextualproperty
    @Link.expand
    def attributedTo(self):
        return getattr(self, '___attributedTo___', None)

    @attributedTo.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def attributedTo(self):
        return getattr(self, '___attributedTo___', None)

    @attributedTo.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def attributedTo(self, val):
        self.___attributedTo___ = val


class Actor(ActivityStreamsProperty):
    """
    Describes one or more entities that either performed or are expected to
    perform the activity. Any single activity can have multiple actors. The
    actor MAY be specified using an indirect Link.
    """

    # TODO: FIND A WAY TO DISABLE ATTRIBUTEDTO WHEN ACTOR IS PRESENT
    @contextualproperty
    @Link.expand
    def actor(self):
        return getattr(self, '___actor___', None)

    @actor.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def actor(self):
        return getattr(self, '___actor___', None)

    @actor.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def actor(self, val):
        self.___actor___ = val


class Audience(ActivityStreamsProperty):
    """
    Identifies one or more entities that represent the total population of
    entities for which the object can be considered to be relevant.
    """

    @contextualproperty
    @Link.expand
    def audience(self):
        return getattr(self, '___audience___', None)

    @audience.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def audience(self):
        return getattr(self, '___audience___', None)

    @audience.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def audience(self, val):
        self.___audience___ = val


class Bcc(ActivityStreamsProperty):
    """
    Identifies one or more Objects that are part of the private secondary
    audience of this Object.
    """

    @contextualproperty
    @Link.expand
    def bcc(self):
        return getattr(self, '___bcc___', None)

    @bcc.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def bcc(self):
        return getattr(self, '___bcc___', None)

    @bcc.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def bcc(self, val):
        self.___bcc___ = val


class Bto(ActivityStreamsProperty):
    """
    Identifies an Object that is part of the private primary audience of this
    Object.
    """

    @contextualproperty
    @Link.expand
    def bto(self):
        return getattr(self, '___bto___', None)

    @bto.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def bto(self):
        return getattr(self, '___bto___', None)

    @bto.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def bto(self, val):
        self.___bto___ = val


class Cc(ActivityStreamsProperty):
    """
    Identifies an Object that is part of the public secondary audience of this
    Object.
    """

    @contextualproperty
    @Link.expand
    def cc(self):
        return getattr(self, '___cc___', None)

    @cc.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def cc(self):
        return getattr(self, '___cc___', None)

    @cc.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def cc(self, val):
        self.___cc___ = val


class Context(ActivityStreamsProperty):
    """
    Identifies the context within which the object exists or an activity was
    performed.

    The notion of "context" used is intentionally vague. The intended function
    is to serve as a means of grouping objects and activities that share a
    common originating context or purpose. An example could be all activities
    relating to a common project or event.
    """

    @contextualproperty
    @Link.expand
    def context(self):
        return getattr(self, '___context___', None)

    @context.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def context(self):
        return getattr(self, '___context___', None)

    @context.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def context(self, val):
        self.___context___ = val


class Current(ActivityStreamsProperty):
    """
    In a paged Collection, indicates the page that contains the most recently
    updated member items.
    """

    @contextualproperty
    @Link.expand
    def current(self):
        return getattr(self, '___current___', None)

    @current.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def current(self):
        return getattr(self, '___current___', None)

    @current.setter
    @Link.from_str
    @SetterValidator(types=(CollectionPage, Link), functional=True).check
    def current(self, val):
        self.___current___ = val


class First(ActivityStreamsProperty):
    """
    In a paged Collection, indicates the furthest preceding page of items in
    the collection.
    """

    @contextualproperty
    @Link.expand
    def first(self):
        return getattr(self, '___first___', None)

    @first.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def first(self):
        return getattr(self, '___first___', None)

    @first.setter
    @Link.from_str
    @SetterValidator(types=(CollectionPage, Link), functional=True).check
    def first(self, val):
        self.___first___ = val


class Generator(ActivityStreamsProperty):
    """
    Identifies the entity (e.g. an application) that generated the object.
    """

    @contextualproperty
    @Link.expand
    def generator(self):
        return getattr(self, '___generator___', None)

    @generator.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def generator(self):
        return getattr(self, '___generator___', None)

    @generator.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def generator(self, val):
        self.___generator___ = val


class Icon(ActivityStreamsProperty):
    """
    Indicates an entity that describes an icon for this object. The image
    should have an aspect ratio of one (horizontal) to one (vertical) and
    should be suitable for presentation at a small size.
    """

    @contextualproperty
    @Link.expand
    def icon(self):
        return getattr(self, '___icon___', None)

    @icon.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def icon(self):
        return getattr(self, '___icon___', None)

    @icon.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def icon(self, val):
        self.___icon___ = val


class Image(ActivityStreamsProperty):
    """
    Indicates an entity that describes an image for this object. Unlike the
    icon property, there are no aspect ratio or display size limitations
    assumed.
    """

    @contextualproperty
    @Link.expand
    def image(self):
        return getattr(self, '___image___', None)

    @image.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def image(self):
        return getattr(self, '___image___', None)

    @image.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def image(self, val):
        self.___image___ = val


class InReplyTo(ActivityStreamsProperty):
    """
    Indicates one or more entities for which this object is considered a
    response.
    """

    @contextualproperty
    @Link.expand
    def inReplyTo(self):
        return getattr(self, '___inReplyTo___', None)

    @inReplyTo.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def inReplyTo(self):
        return getattr(self, '___inReplyTo___', None)

    @inReplyTo.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def inReplyTo(self, val):
        self.___inReplyTo___ = val


class Instrument(ActivityStreamsProperty):
    """
    Identifies one or more objects used (or to be used) in the completion of an
    Activity.
    """

    @contextualproperty
    @Link.expand
    def instrument(self):
        return getattr(self, '___instrument___', None)

    @instrument.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def instrument(self):
        return getattr(self, '___instrument___', None)

    @instrument.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def instrument(self, val):
        self.___instrument___ = val


class Last(ActivityStreamsProperty):
    """
    In a paged Collection, indicates the furthest proceeding page of the
    collection.
    """

    @contextualproperty
    @Link.expand
    def last(self):
        return getattr(self, '___last___', None)

    @last.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def last(self):
        return getattr(self, '___last___', None)

    @last.setter
    @Link.from_str
    @SetterValidator(types=(CollectionPage, Link), functional=True).check
    def last(self, val):
        self.___last___ = val


class Location(ActivityStreamsProperty):
    """
    Indicates one or more physical or logical locations associated with the
    object.
    """

    @contextualproperty
    @Link.expand
    def location(self):
        return getattr(self, '___location___', None)

    @location.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def location(self):
        return getattr(self, '___location___', None)

    @location.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def location(self, val):
        self.___location___ = val


class Items(ActivityStreamsProperty):
    """
    Identifies the items contained in a collection. The items might be ordered
    or unordered.
    """

    @contextualproperty
    @Link.expand
    def items(self):
        return getattr(self, '___items___', None)

    @items.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def items(self):
        return getattr(self, '___items___', None)

    @items.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def items(self, val):
        self.___items___ = val


class OrderedItems(ActivityStreamsProperty):
    """
    Identifies the items contained in a collection. The items might be ordered
    or unordered.
    """

    @contextualproperty
    @Link.expand
    def orderedItems(self):
        return getattr(self, '___orderedItems___', None)

    @orderedItems.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def orderedItems(self):
        return getattr(self, '___orderedItems___', None)

    @orderedItems.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def orderedItems(self, val):
        self.___orderedItems___ = val


class UnorderedItems(ActivityStreamsProperty):
    """
    Identifies the items contained in a collection. The items might be ordered
    or unordered.
    """

    @contextualproperty
    @Link.expand
    def unorderedItems(self):
        return getattr(self, '___unorderedItems___', None)

    @unorderedItems.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def unorderedItems(self):
        return getattr(self, '___unorderedItems___', None)

    @unorderedItems.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def unorderedItems(self, val):
        self.___unorderedItems___ = val


class OneOf(ActivityStreamsProperty):
    """
    Identifies an exclusive option for a Question. Use of oneOf implies that
    the Question can have only a single answer. To indicate that a Question can
    have multiple answers, use anyOf.
    """

    @contextualproperty
    @Link.expand
    def oneOf(self):
        return getattr(self, '___oneOf___', None)

    @oneOf.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def oneOf(self):
        return getattr(self, '___oneOf___', None)

    @oneOf.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def oneOf(self, val):
        self.___oneOf___ = val


class AnyOf(ActivityStreamsProperty):
    """
    Identifies an inclusive option for a Question. Use of anyOf implies that
    the Question can have multiple answers. To indicate that a Question can
    have only one answer, use oneOf.
    """

    @contextualproperty
    @Link.expand
    def anyOf(self):
        return getattr(self, '___anyOf___', None)

    @anyOf.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def anyOf(self):
        return getattr(self, '___anyOf___', None)

    @anyOf.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def anyOf(self, val):
        self.___anyOf___ = val


class Closed(ActivityStreamsProperty):
    """
    Indicates that a question has been closed, and answers are no longer
    accepted.
    """

    @contextualproperty
    @Link.expand
    def closed(self):
        return getattr(self, '___closed___', None)

    @closed.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def closed(self):
        val = getattr(self, '___closed___', None)
        if isinstance(val, datetime):
            return datetime_str(val)
        return val

    @closed.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link, datetime, bool)).check
    def closed(self, val):
        self.___closed___ = val


class Origin(ActivityStreamsProperty):
    """
    Describes an indirect object of the activity from which the activity is
    directed. The precise meaning of the origin is the object of the English
    preposition "from". For instance, in the activity "John moved an item to
    List B from List A", the origin of the activity is "List A".
    """

    @contextualproperty
    @Link.expand
    def origin(self):
        return getattr(self, '___origin___', None)

    @origin.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def origin(self):
        return getattr(self, '___origin___', None)

    @origin.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def origin(self, val):
        self.___origin___ = val


class Next(ActivityStreamsProperty):
    """
    In a paged Collection, indicates the next page of items.
    """

    @contextualproperty
    @Link.expand
    def next(self):
        return getattr(self, '___next___', None)

    @next.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def next(self):
        return getattr(self, '___next___', None)

    @next.setter
    @Link.from_str
    @SetterValidator(types=(CollectionPage, Link), functional=True).check
    def next(self, val):
        self.___next___ = val


class Object(ActivityStreamsProperty):
    """
    When used within an Activity, describes the direct object of the activity.
    For instance, in the activity "John added a movie to his wishlist", the
    object of the activity is the movie added.

    When used within a Relationship describes the entity to which the subject
    is related.
    """

    @contextualproperty
    @Link.expand
    def object(self):
        return getattr(self, '___object___', None)

    @object.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def object(self):
        return getattr(self, '___object___', None)

    @object.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def object(self, val):
        self.___object___ = val


class Prev(ActivityStreamsProperty):
    """
    In a paged Collection, identifies the previous page of items.
    """

    @contextualproperty
    @Link.expand
    def prev(self):
        return getattr(self, '___prev___', None)

    @prev.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def prev(self):
        return getattr(self, '___prev___', None)

    @prev.setter
    @Link.from_str
    @SetterValidator(types=(CollectionPage, Link), functional=True).check
    def prev(self, val):
        self.___prev___ = val


class Preview(ActivityStreamsProperty):
    """
    Identifies an entity that provides a preview of this object.
    """

    @contextualproperty
    @Link.expand
    def preview(self):
        return getattr(self, '___preview___', None)

    @preview.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def preview(self):
        return getattr(self, '___preview___', None)

    @preview.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def preview(self, val):
        self.___preview___ = val


class Result(ActivityStreamsProperty):
    """
    Describes the result of the activity. For instance, if a particular action
    results in the creation of a new resource, the result property can be used
    to describe that new resource.
    """

    @contextualproperty
    @Link.expand
    def result(self):
        return getattr(self, '___result___', None)

    @result.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def result(self):
        return getattr(self, '___result___', None)

    @result.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def result(self, val):
        self.___result___ = val


class Replies(ActivityStreamsProperty):
    """
    Identifies a Collection containing objects considered to be responses to
    this object.
    """

    @contextualproperty
    @Link.expand
    def replies(self):
        return getattr(self, '___replies___', None)

    @replies.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def replies(self):
        return getattr(self, '___replies___', None)

    @replies.setter
    @Link.from_str
    @SetterValidator(types=(Collection,), functional=True).check
    def replies(self, val):
        self.___replies___ = val


class Tag(ActivityStreamsProperty):
    """
    One or more "tags" that have been associated with an objects. A tag can be
    any kind of Object. The key difference between attachment and tag is that
    the former implies association by inclusion, while the latter implies
    associated by reference.
    """

    @contextualproperty
    @Link.expand
    def tag(self):
        return getattr(self, '___tag___', None)

    @tag.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def tag(self):
        return getattr(self, '___tag___', None)

    @tag.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link, dict)).check
    def tag(self, val):
        self.___tag___ = val


class Target(ActivityStreamsProperty):
    """
    Describes the indirect object, or target, of the activity. The precise
    meaning of the target is largely dependent on the type of action being
    described but will often be the object of the English preposition "to". For
    instance, in the activity "John added a movie to his wishlist", the target
    of the activity is John's wishlist. An activity can have more than one
    target.
    """

    @contextualproperty
    @Link.expand
    def target(self):
        return getattr(self, '___target___', None)

    @target.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def target(self):
        return getattr(self, '___target___', None)

    @target.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def target(self, val):
        self.___target___ = val


class To(ActivityStreamsProperty):
    """
    Identifies an entity considered to be part of the public primary audience
    of an Object
    """

    @contextualproperty
    @Link.expand
    def to(self):
        return getattr(self, '___to___', None)

    @to.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def to(self):
        return getattr(self, '___to___', None)

    @to.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link)).check
    def to(self, val):
        self.___to___ = val


class Url(ActivityStreamsProperty):
    """
    Identifies one or more links to representations of the object
    """

    @contextualproperty
    @Link.expand
    def url(self):
        return getattr(self, '___url___', None)

    @url.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def url(self):
        return getattr(self, '___url___', None)

    @url.setter
    @Link.from_str
    @SetterValidator(types=(Link, str)).check
    def url(self, val):
        self.___url___ = val


class Accuracy(ActivityStreamsProperty):
    """
    Indicates the accuracy of position coordinates on a Place objects.
    Expressed in properties of percentage. e.g. "94.0" means "94.0% accurate".
    """

    @contextualproperty
    def accuracy(self):
        return getattr(self, '___accuracy___', None)

    @accuracy.setter
    @SetterValidator(types=(float, int), functional=True).check
    def accuracy(self, val):
        self.___accuracy___ = val


class Altitude(ActivityStreamsProperty):
    """
    Indicates the altitude of a place. The measurement units is indicated
    using the units property. If units is not specified, the default is
    assumed to be "m" indicating meters.
    """

    @contextualproperty
    def altitude(self):
        return getattr(self, '___altitude___', None)

    @altitude.setter
    @SetterValidator(types=(float, int), functional=True).check
    def altitude(self, val):
        self.___altitude___ = val


class Content(ActivityStreamsProperty):
    """
    The content or textual representation of the Object encoded as a JSON
    string. By default, the value of content is HTML. The mediaType property
    can be used in the object to indicate a different content type.

    The content MAY be expressed using multiple language-tagged values.
    """

    @contextualproperty
    def content(self):
        return getattr(self, '___content___', None)

    @content.setter
    @SetterValidator(types=(str,)).check
    def content(self, val):
        self.___content___ = val


class Name(ActivityStreamsProperty):
    """
    A simple, human-readable, plain-text name for the object. HTML markup
    MUST NOT be included. The name MAY be expressed using multiple
    language-tagged values.
    """

    @contextualproperty
    def name(self):
        return getattr(self, '___name___', None)

    @name.setter
    @SetterValidator(types=(str, dict)).check
    def name(self, val):
        self.___name___ = val


class Duration(ActivityStreamsProperty):
    """
    When the object describes a time-bound resource, such as an audio or video,
    a meeting, etc., the duration property indicates the object's approximate
    duration. The value MUST be expressed as an xsd:duration as defined by
    [xmlschema11-2], section 3.3.6 (e.g. a period of 5 seconds is represented
    as "PT5S").
    """

    @contextualproperty
    def duration(self):
        return getattr(self, '___duration___', None)

    @duration.getter_context(JSON_DATA_CONTEXT)
    def duration(self):
        val = getattr(self, '___duration___', None)
        if isinstance(val, timedelta):
            return timedelta_str(val)
        return val

    @duration.setter
    @SetterValidator(types=(timedelta, str), functional=True).check
    def duration(self, val):
        self.___duration___ = val


class Height(ActivityStreamsProperty):
    """
    On a Link, specifies a hint as to the rendering height in device-independent
    pixels of the linked resource.
    """

    __height = None

    @contextualproperty
    def height(self):
        return self.__height

    @height.setter
    @SetterValidator(types=(int,), functional=True,
                     additional=(is_nonnegative,)).check
    def height(self, val):
        self.__height = val


class Href(ActivityStreamsProperty):
    """
    The target resource pointed to by a Link.
    """

    @contextualproperty
    def href(self):
        return getattr(self, '___href___', None)

    @href.setter
    @SetterValidator(types=(str,), functional=True).check
    def href(self, val):
        self.___href___ = val


class HrefLang(ActivityStreamsProperty):
    """
    Hints as to the language used by the target resource. Value MUST be a
    [BCP47] Language-Tag.
    """

    @contextualproperty
    def hreflang(self):
        return getattr(self, '___hreflang___', None)

    @hreflang.setter
    @SetterValidator(types=(str,), functional=True).check
    def hreflang(self, val):
        self.__hrefLang = val


class PartOf(ActivityStreamsProperty):
    """
    Identifies the Collection to which a CollectionPage objects items belong.
    """

    @contextualproperty
    @Link.expand
    def partOf(self):
        return getattr(self, '___partOf___', None)

    @partOf.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def partOf(self):
        return getattr(self, '___partOf___', None)

    @partOf.setter
    @Link.from_str
    @SetterValidator(types=(Collection, Link), functional=True).check
    def partOf(self, val):
        self.___partOf___ = val


class Latitude(ActivityStreamsProperty):
    """
    The latitude of a place
    """

    @contextualproperty
    def latitude(self):
        return getattr(self, '___latitude___', None)

    @latitude.setter
    @SetterValidator(types=(float, int), functional=True).check
    def latitude(self, val):
        self.___latitude___ = val


class Longitude(ActivityStreamsProperty):
    """
    The longitude of a place
    """

    @contextualproperty
    def longitude(self):
        return getattr(self, '___longitude___', None)

    @longitude.setter
    @SetterValidator(types=(float, int), functional=True).check
    def longitude(self, val):
        self.___longitude___ = val


class MediaType(ActivityStreamsProperty):
    """
    When used on a Link, identifies the MIME media type of the referenced
    resource.

    When used on an Object, identifies the MIME media type of the value of the
    content property. If not specified, the content property is assumed to
    contain text/html content.
    """

    @contextualproperty
    def mediaType(self):
        return getattr(self, '___mediaType___', None)

    @mediaType.setter
    @SetterValidator(types=(str,), functional=True).check
    def mediaType(self, val):
        self.___mediaType___ = val


class EndTime(ActivityStreamsProperty):
    """
    The date and time describing the actual or expected ending time of the
    object. When used with an Activity object, for instance, the endTime
    property specifies the moment the activity concluded or is expected to
    conclude.
    """

    @contextualproperty
    def endTime(self):
        return getattr(self, '___endTime___', None)

    @endTime.getter_context(JSON_DATA_CONTEXT)
    def endTime(self):
        val = getattr(self, '___endTime___', None)
        if isinstance(val, datetime):
            return datetime_str(val)
        return val

    @endTime.setter
    @SetterValidator(types=(datetime, str), functional=True,
                     additional=(is_activity_datetime,)).check
    def endTime(self, val):
        self.___endTime___ = parse_activitystream_datetime(val)


class Published(ActivityStreamsProperty):
    """
    The date and time at which the object was published
    """

    @contextualproperty
    def published(self):
        return getattr(self, '___published___', None)

    @published.getter_context(JSON_DATA_CONTEXT)
    def published(self):
        val = getattr(self, '___published___', None)
        if isinstance(val, datetime):
            return datetime_str(val)
        return val

    @published.setter
    @SetterValidator(types=(datetime, str), functional=True,
                     additional=(is_activity_datetime,)).check
    def published(self, val):
        self.___published___ = parse_activitystream_datetime(val)


class StartTime(ActivityStreamsProperty):
    """
    The date and time describing the actual or expected starting time of the
    object. When used with an Activity object, for instance, the startTime
    property specifies the moment the activity began or is scheduled to begin.
    """

    @contextualproperty
    def startTime(self):
        return getattr(self, '___startTime___', None)

    @startTime.getter_context(JSON_DATA_CONTEXT)
    def startTime(self):
        val = getattr(self, '___startTime___', None)
        if isinstance(val, datetime):
            return datetime_str(val)
        return val

    @startTime.setter
    @SetterValidator(types=(datetime, str), functional=True,
                     additional=(is_activity_datetime,)).check
    def startTime(self, val):
        self.___startTime___ = parse_activitystream_datetime(val)


class Radius(ActivityStreamsProperty):
    """
    The radius from the given latitude and longitude for a Place. The units are
    expressed by the units property. If units is not specified, the default is
    assumed to be "m" indicating "meters".
    """

    @contextualproperty
    def radius(self):
        return getattr(self, '___radius___', None)

    @radius.setter
    @SetterValidator(types=(float, int), functional=True,
                     additional=(is_nonnegative,)).check
    def radius(self, val):
        self.___radius___ = val


class Rel(ActivityStreamsProperty):
    """
    A link relation associated with a Link. The value MUST conform to both the
    [HTML5] and [RFC5988] "link relation" definitions.

    In the [HTML5], any string not containing the "space" U+0020,
    "tab" (U+0009), "LF" (U+000A), "FF" (U+000C), "CR" (U+000D) or "," (U+002C)
    characters can be used as a valid link relation.
    """

    @contextualproperty
    def rel(self):
        return getattr(self, '___rel___', None)

    @rel.setter
    @SetterValidator(types=(str,)).check
    def rel(self, val):
        self.___rel___ = val


class StartIndex(ActivityStreamsProperty):
    """
    A non-negative integer value identifying the relative position within the
    logical view of a strictly ordered collection.
    """

    @contextualproperty
    def startIndex(self):
        return getattr(self, '___startIndex___', None)

    @startIndex.setter
    @SetterValidator(types=(int,), functional=True,
                     additional=(is_nonnegative,)).check
    def startIndex(self, val):
        self.___startIndex___ = val


class Summary(ActivityStreamsProperty):
    """
    A natural language summarization of the object encoded as HTML. Multiple
    language tagged summaries MAY be provided.
    """

    @contextualproperty
    def summary(self):
        return getattr(self, '___summary___', None)

    @summary.setter
    @SetterValidator(types=(str,)).check
    def summary(self, val):
        self.___summary___ = val


class TotalItems(ActivityStreamsProperty):
    """
    A non-negative integer specifying the total number of objects contained by
    the logical view of the collection. This number might not reflect the
    actual number of items serialized within the Collection object instance.
    """

    @contextualproperty
    def totalItems(self):
        return getattr(self, '___totalItems___', None)

    @totalItems.setter
    @SetterValidator(types=(int,), functional=True,
                     additional=(is_nonnegative,)).check
    def totalItems(self, val):
        self.___totalItems___ = val


class Units(ActivityStreamsProperty):
    """
    Specifies the measurement units for the radius and altitude properties on a
    Place object. If not specified, the default is assumed to be "m" for
    "meters".
    """

    @contextualproperty
    def units(self):
        return getattr(self, '___units___', None)

    @units.setter
    @SetterValidator(types=(str,), functional=True).check
    def units(self, val):
        self.___units___ = val


class Updated(ActivityStreamsProperty):
    """
    The date and time at which the object was updated
    """

    @contextualproperty
    def updated(self):
        return getattr(self, '___updated___', None)

    @updated.getter_context(JSON_DATA_CONTEXT)
    def updated(self):
        val = getattr(self, '___updated___', None)
        if isinstance(val, datetime):
            return datetime_str(val)
        return val

    @updated.setter
    @SetterValidator(types=(datetime, str), functional=True,
                     additional=(is_activity_datetime,)).check
    def updated(self, val):
        self.___updated___ = parse_activitystream_datetime(val)


class Width(ActivityStreamsProperty):
    """
    On a Link, specifies a hint as to the rendering width in device-independent
    pixels of the linked resource.
    """

    @contextualproperty
    def width(self):
        return getattr(self, '___width___', None)

    @width.setter
    @SetterValidator(types=(int,), functional=True,
                     additional=(is_nonnegative,)).check
    def width(self, val):
        self.___width___ = val


class Subject(ActivityStreamsProperty):
    """
    On a Relationship object, the subject property identifies one of the
    connected individuals. For instance, for a Relationship object describing
    "John is related to Sally", subject would refer to John.
    """

    @contextualproperty
    @Link.expand
    def subject(self):
        return getattr(self, '___subject___', None)

    @subject.getter_context(JSON_DATA_CONTEXT)
    @Link.href_only
    def subject(self):
        return getattr(self, '___subject___', None)

    @subject.setter
    @Link.from_str
    @SetterValidator(types=(Object, Link), functional=True).check
    def subject(self, val):
        self.___subject___ = val


class Relationship(ActivityStreamsProperty):
    """
    On a Relationship object, the relationship property identifies the kind of
    relationship that exists between subject and object.
    """

    @contextualproperty
    def relationship(self):
        return getattr(self, '___relationship___', None)

    @relationship.setter
    @SetterValidator(types=(Object, str)).check
    def relationship(self, val):
        self.___relationship___ = val


class Describes(ActivityStreamsProperty):
    """
    On a Profile object, the describes property identifies the object described
    by the Profile.
    """

    @contextualproperty
    def describes(self):
        return getattr(self, '___describes___', None)

    @describes.setter
    @SetterValidator(types=(Object,), functional=True).check
    def describes(self, val):
        self.___describes___ = val


class FormerType(ActivityStreamsProperty):
    """
    On a Tombstone object, the formerType property identifies the type of the
    object that was deleted.
    """

    @contextualproperty
    def formerType(self):
        return getattr(self, '___formerType___', None)

    @formerType.setter
    @SetterValidator(types=(Object,)).check
    def formerType(self, val):
        self.___formerType___ = val


class Deleted(ActivityStreamsProperty):
    """
    On a Tombstone object, the deleted property is a timestamp for when the
    object was deleted.
    """

    @contextualproperty
    def deleted(self):
        return getattr(self, '___deleted___', None)

    @deleted.getter_context(JSON_DATA_CONTEXT)
    def deleted(self):
        val = getattr(self, '___deleted___', None)
        if isinstance(val, datetime):
            return datetime_str(val)
        return val

    @deleted.setter
    @SetterValidator(types=(datetime,), functional=True,
                     additional=(is_activity_datetime,)).check
    def deleted(self, val):
        self.___deleted___ = val

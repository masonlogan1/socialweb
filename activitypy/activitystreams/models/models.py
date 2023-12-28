"""
Provides data structures for ActivityStreams vocabulary objects. These objects
are not a full implementation, just an outline that ensures attributes are
handled correctly.
"""
# Yes, the docstrings for each class are directly taken from the ActivityStreams
# Vocabulary document. This whole module is intentionally barely one level of
# abstraction from the spec

from collections.abc import Iterable, Sized
from datetime import datetime, timedelta
from activitypy.jsonld import ApplicationActivityJson
from activitypy.activitystreams.models.utils import is_activity_datetime, \
    parse_activitystream_datetime

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# "Why is this one big file? Shouldn't you break this into multiple modules?"
# I would love to, but because Properties, Activities, Actors, and Objects all
# relate to one another and everything has a clearly defined domain and range,
# any attempt to split these into separate files results in a clusterfuck of
# circular imports. Abandon hope ye who enter! This is a godless nightmare


# VALIDATOR TOOLS
# Currently the validator tools allow for storing things as literal strings.
# In the future, this functionality will be REMOVED in favor of a system
# that uses Links/Objects that are transformed back into the string literal
# when generating the outgoing json
def object_or_link(val):
    return isinstance(val, (ObjectModel, LinkModel, str))

def object_list_or_link(val):
    return isinstance(val, (ObjectModel, LinkModel, list, str))

def collectionpage_or_link(val):
    return isinstance(val, (CollectionPageModel, LinkModel, str))

def collection_or_link(val):
    return isinstance(val, (CollectionModel, LinkModel, str))

def is_collection(val):
    return isinstance(val, (CollectionModel, str))


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

class IdProperty:
    """
    Provides the globally unique identifier for an Object or Link.
    """
    __id = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, val):
        if val is not None and not isinstance(val, str):
            raise ValueError(f'Property "id" must be of type "str"; ' +
                             f'got {val} ({type(val)})')
        logger.debug(f'setting "id" of {self} to {val}')
        self.__id = val


class TypeProperty:
    """
    Identifies the Object or Link type. Multiple values may be specified.
    """
    __type = None

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, val):
        if val is not None and not isinstance(val, str):
            raise ValueError(f'Property "type" must be of type "str"; ' +
                             f'got {val} ({type(val)})')
        self.__type = val


class ActorProperty:
    """
    Describes one or more entities that either performed or are expected to
    perform the activity. Any single activity can have multiple actors. The
    actor MAY be specified using an indirect Link.
    """
    __actor = None

    @property
    def actor(self):
        return self.__actor

    @actor.setter
    def actor(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "actor" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__actor = val


class AttachmentProperty:
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
    def attachment(self, val):
        if val is not None and not object_list_or_link(val):
            raise ValueError(
                f'Property "attachment" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__attachment = val


class AttributedToProperty:
    """
    Identifies one or more entities to which this object is attributed. The
    attributed entities might not be Actors. For instance, an object might be
    attributed to the completion of another activity.
    """

    __attributedTo = None

    @property
    def attributedTo(self):
        return self.__attributedTo

    @attributedTo.setter
    def attributedTo(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "attributedTo" must be of type "Object" or ' +
                f'"Link"; got {val} ({type(val)})')
        self.__attributedTo = val


class AudienceProperty:
    """
    Identifies one or more entities that represent the total population of
    entities for which the object can be considered to be relevant.
    """

    __audience = None

    @property
    def audience(self):
        return self.__audience

    @audience.setter
    def audience(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "audience" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__audience = val


class BccProperty:
    """
    Identifies one or more Objects that are part of the private secondary
    audience of this Object.
    """

    __bcc = None

    @property
    def bcc(self):
        return self.__bcc

    @bcc.setter
    def bcc(self, val):
        if val is not None and not object_list_or_link(val):
            raise ValueError(
                f'Property "bcc" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__bcc = val


class BtoProperty:
    """
    Identifies an Object that is part of the private primary audience of this
    Object.
    """

    __bto = None

    @property
    def bto(self):
        return self.__bto

    @bto.setter
    def bto(self, val):
        if val is not None and not object_list_or_link(val):
            raise ValueError(
                f'Property "bto" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__bto = val


class CcProperty:
    """
    Identifies an Object that is part of the public secondary audience of this
    Object.
    """

    __cc = None

    @property
    def cc(self):
        return self.__cc

    @cc.setter
    def cc(self, val):
        if val is not None and not object_list_or_link(val):
            raise ValueError(
                f'Property "cc" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__cc = self.__cc


class ContextProperty:
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
    def context(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "context" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__context = val


class CurrentProperty:
    """
    In a paged Collection, indicates the page that contains the most recently
    updated member items.
    """

    __current = None

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, val):
        if val is not None and not collectionpage_or_link(val):
            raise ValueError(
                f'Property "current" must be of type "CollectionPage" or ' +
                f'"Link"; got {val} ({type(val)})')
        self.__current = val


class FirstProperty:
    """
    In a paged Collection, indicates the furthest preceding page of items in
    the collection.
    """

    __first = None

    @property
    def first(self):
        return self.__first

    @first.setter
    def first(self, val):
        if val is not None and not collectionpage_or_link(val):
            raise ValueError(
                f'Property "first" must be of type "CollectionPage" or ' +
                f'"Link"; got {val} ({type(val)})')
        self.__first = val


class GeneratorProperty:
    """
    Identifies the entity (e.g. an application) that generated the object.
    """

    __generator = None

    @property
    def generator(self):
        return self.__generator

    @generator.setter
    def generator(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "generator" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__generator = val


class IconProperty:
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
    def icon(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "icon" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__icon = val


class ImageProperty:
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
    def image(self, val):
        if val is not None and not isinstance(val, (ImageModel, LinkModel)):
            raise ValueError(
                f'Property "image" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__image = val


class InReplyToProperty:
    """
    Indicates one or more entities for which this object is considered a
    response.
    """

    __inReplyTo = None

    @property
    def inReplyTo(self):
        return self.__inReplyTo

    @inReplyTo.setter
    def inReplyTo(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "inReplyTo" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__inReplyTo = val


class InstrumentProperty:
    """
    Identifies one or more objects used (or to be used) in the completion of an
    Activity.
    """

    __instrument = None

    @property
    def instrument(self):
        return self.__instrument

    @instrument.setter
    def instrument(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "instrument" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__instrument = val


class LastProperty:
    """
    In a paged Collection, indicates the furthest proceeding page of the
    collection.
    """

    __last = None

    @property
    def last(self):
        return self.__last

    @last.setter
    def last(self, val):
        if val is not None and not collectionpage_or_link(val):
            raise ValueError(
                f'Property "last" must be of type "CollectionPage" or ' +
                f'"Link"; got {val} ({type(val)})')
        self.__last = val


class LocationProperty:
    """
    Indicates one or more physical or logical locations associated with the
    object.
    """

    __location = None

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "location" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__location = val


class ItemsProperty:
    """
    Identifies the items contained in a collection. The items might be ordered
    or unordered.
    """

    __items = None

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, val):
        if val is not None and not isinstance(val, (
                ObjectModel, LinkModel, Iterable)):
            raise ValueError(
                f'Property "items" must be of type "Object", "Link", or ' +
                f'Iterable; got {val} ({type(val)})')
        self.__items = val


class OrderedItemsProperty(ItemsProperty):
    """
    Identifies the items contained in a collection. The items might be ordered
    or unordered.
    """

    # this is essentially just a wrapper for "items"
    @property
    def orderedItems(self):
        return self.items

    @orderedItems.setter
    def orderedItems(self, val):
        if val is not None and not isinstance(val, (
                ObjectModel, LinkModel, Iterable)):
            raise ValueError(
                f'Property "orderedItems" must be of type "Object", ' +
                f'"Link", or Iterable; got {val} ({type(val)})')
        self.items = val


class UnorderedItemsProperty:
    """
    Identifies the items contained in a collection. The items might be ordered
    or unordered.
    """

    __unorderedItems = None

    @property
    def unorderedItems(self):
        return self.__unorderedItems

    @unorderedItems.setter
    def unorderedItems(self, val):
        if val is not None and not isinstance(val, (
                ObjectModel, LinkModel, Iterable)):
            raise ValueError(
                f'Property "unorderedItems" must be of type "Object", ' +
                f'"Link", or Iterable; got {val} ({type(val)})')
        self.__unorderedItems = val


class OneOfProperty:
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
    def oneOf(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "oneOf" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__oneOf = val


class AnyOfProperty:
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
    def anyOf(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "anyOf" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__anyOf = val


class ClosedProperty:
    """
    Indicates that a question has been closed, and answers are no longer
    accepted.
    """

    __closed = None

    @property
    def closed(self):
        return self.__closed

    @closed.setter
    def closed(self, val):
        if val is not None and not isinstance(val,
                                              (ObjectModel, LinkModel, bool,
                                               datetime)):
            raise ValueError(
                f'Property "closed" must be of type "Object", "Link", ' +
                f'"datetime.datetime", or "bool"; got {val} ({type(val)})')
        self.__closed = val


class OriginProperty:
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
    def origin(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "origin" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__origin = val


class NextProperty:
    """
    In a paged Collection, indicates the next page of items.
    """

    __next = None

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, val):
        if val is not None and not collectionpage_or_link(val):
            raise ValueError(
                f'Property "next" must be of type "CollectionPage" or ' +
                f'"Link"; got {val} ({type(val)})')
        self.__next = val


class ObjectProperty:
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
    def object(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "object" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__object = val


class PrevProperty:
    """
    In a paged Collection, identifies the previous page of items.
    """

    __prev = None

    @property
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self, val):
        if val is not None and not collectionpage_or_link(val):
            raise ValueError(
                f'Property "prev" must be of type "CollectionPage" or ' +
                f'"Link"; got {val} ({type(val)})')
        self.__prev = val


class PreviewProperty:
    """
    Identifies an entity that provides a preview of this object.
    """

    __preview = None

    @property
    def preview(self):
        return self.__preview

    @preview.setter
    def preview(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "preview" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__preview = val


class ResultProperty:
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
    def result(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "result" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__result = val


class RepliesProperty:
    """
    Identifies a Collection containing objects considered to be responses to
    this object.
    """

    __replies = None

    @property
    def replies(self):
        return self.__replies

    @replies.setter
    def replies(self, val):
        if val is not None and not is_collection(val):
            raise ValueError(
                f'Property "replies" must be of type "Collection"; ' +
                f'got {val} ({type(val)})')
        self.__replies = val


class TagProperty:
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
    def tag(self, val):
        if val is not None and not object_list_or_link(val):
            raise ValueError(
                f'Property "tag" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__tag = val


class TargetProperty:
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
    def target(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "target" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__target = val


class ToProperty:
    """
    Identifies an entity considered to be part of the public primary audience
    of an Object
    """

    __to = None

    @property
    def to(self):
        return self.__to

    @to.setter
    def to(self, val):
        if val is not None and not object_list_or_link(val):
            raise ValueError(
                f'Property "to" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__to = val


class UrlProperty:
    """
    Identifies one or more links to representations of the object
    """

    __url = None

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, val):
        if val is not None and not isinstance(val, (LinkModel, str)):
            raise ValueError(
                f'Property "url" must be of type "Link" or "str"; ' +
                f'got {val} ({type(val)})')
        self.__url = val


class AccuracyProperty:
    """
    Indicates the accuracy of position coordinates on a Place objects.
    Expressed in properties of percentage. e.g. "94.0" means "94.0% accurate".
    """

    __accuracy = None

    @property
    def accuracy(self):
        return self.__accuracy

    @accuracy.setter
    def accuracy(self, val):
        if val is not None and not isinstance(val, float):
            raise ValueError(
                f'Property "accuracy" must be of type "float"; ' +
                f'got {val} ({type(val)})')
        self.__accuracy = val


class AltitudeProperty:
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
    def altitude(self, val):
        if val is not None and not isinstance(val, float):
            raise ValueError(
                f'Property "altitude" must be of type "float"; ' +
                f'got {val} ({type(val)})')
        self.__altitude = val


class ContentProperty:
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
    def content(self, val):
        if val is not None and not isinstance(val, str):
            raise ValueError(
                f'Property "content" must be of type "str"; ' +
                f'got {val} ({type(val)})')
        self.__content = val


class NameProperty:
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
    def name(self, val):
        if val is not None and not isinstance(val, str):
            raise ValueError(
                f'Property "name" must be of type "str"; ' +
                f'got {val} ({type(val)})')
        self.__name = val


class DurationProperty:
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
    def duration(self, val):
        if val is not None and not isinstance(val, (str, timedelta)):
            raise ValueError(
                f'Property "duration" must be of type "str" or "timedelta"; ' +
                f'got {val} ({type(val)})')
        self.__duration = val


class HeightProperty:
    """
    On a Link, specifies a hint as to the rendering height in device-independent
    pixels of the linked resource.
    """

    __height = None

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, val):
        if val is not None:
            if not isinstance(val, int):
                raise ValueError(
                    f'Property "content" must be of type "int"; ' +
                    f'got {val} ({type(val)})')
            if val < 0:
                raise ValueError(f'Property "height" must be greater than 0; ' +
                                 f'got {val}')
        self.__height = val


class HrefProperty:
    """
    The target resource pointed to by a Link.
    """

    __href = None

    @property
    def href(self):
        return self.__href

    @href.setter
    def href(self, val):
        if val is not None and not isinstance(val, str):
            raise ValueError(
                f'Property "href" must be of type "str"; ' +
                f'got {val} ({type(val)})')
        self.__href = val


class HrefLangProperty:
    """
    Hints as to the language used by the target resource. Value MUST be a
    [BCP47] Language-Tag.
    """

    __hrefLang = None

    @property
    def hreflang(self):
        return self.__hrefLang

    @hreflang.setter
    def hreflang(self, val):
        if val is not None and not isinstance(val, str):
            raise ValueError(
                f'Property "hrefLang" must be of type "str"; ' +
                f'got {val} ({type(val)})')
        self.__hrefLang = val


class PartOfProperty:
    """
    Identifies the Collection to which a CollectionPage objects items belong.
    """

    __partOf = None

    @property
    def partOf(self):
        return self.__partOf

    @partOf.setter
    def partOf(self, val):
        if val is not None and not collection_or_link(val):
            raise ValueError(
                f'Property "partOf" must be of type "Collection" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__partOf = val


class LatitudeProperty:
    """
    The latitude of a place
    """

    __latitude = None

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, val):
        if val is not None and not isinstance(val, float):
            raise ValueError(
                f'Property "latitude" must be of type "float"; ' +
                f'got {val} ({type(val)})')
        self.__latitude = val


class LongitudeProperty:
    """
    The longitude of a place
    """

    __longitude = None

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, val):
        if val is not None and not isinstance(val, float):
            raise ValueError(
                f'Property "longitude" must be of type "float"; ' +
                f'got {val} ({type(val)})')
        self.__longitude = val


class MediaTypeProperty:
    """
    When used on a Link, identifies the MIME media type of the referenced
    resource.

    When used on an Object, identifies the MIME media type of the value of the
    content property. If not specified, the content property is assumed to
    contain text/html content.
    """

    __mediaType = None

    @property
    def mediaType(self):
        return self.__mediaType

    @mediaType.setter
    def mediaType(self, val):
        if val is not None and not isinstance(val, str):
            raise ValueError(
                f'Property "mediaType" must be of type "str"; ' +
                f'got {val} ({type(val)})')
        self.__mediaType = val


class EndTimeProperty:
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
    def endTime(self, val):
        if val is not None and not is_activity_datetime(val):
            raise ValueError(
                f'Property "endTime" must be of type "datetime" or "str" in ' +
                f'"YYYY-mm-dd-THH:MM:SSZ" format; ' +
                f'got {val} ({type(val)})')
        self.__endTime = parse_activitystream_datetime(val)


class PublishedProperty:
    """
    The date and time at which the object was published
    """

    __published = None

    @property
    def published(self):
        return self.__published

    @published.setter
    def published(self, val):
        if val is not None and not is_activity_datetime(val):
            raise ValueError(
                f'Property "published" must be of type "datetime" or "str" ' +
                f'in "YYYY-mm-dd-THH:MM:SSZ" format; ' +
                f'got {val} ({type(val)})')
        self.__published = parse_activitystream_datetime(val)


class StartTimeProperty:
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
    def startTime(self, val):
        if val is not None and not is_activity_datetime(val):
            raise ValueError(
                f'Property "startTime" must be of type "datetime" or "str" ' +
                f'in "YYYY-mm-dd-THH:MM:SSZ" format; ' +
                f'got {val} ({type(val)})')
        self.__startTime = parse_activitystream_datetime(val)


class RadiusProperty:
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
    def radius(self, val):
        if val is not None:
            if not isinstance(val, float):
                raise ValueError(
                    f'Property "radius" must be of type "float"; ' +
                    f'got {val} ({type(val)})')
            if val < 0:
                raise ValueError(
                    f'Property "radius" must be greater than 0; ' +
                    f'got {val}'
                )
        self.__radius = val


class RelProperty:
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
    def rel(self, val):
        if val is not None and not isinstance(val, str):
            raise ValueError(
                f'Property "rel" must be of type "str"; ' +
                f'got {val} ({type(val)})')
        self.__rel = val


class StartIndexProperty:
    """
    A non-negative integer value identifying the relative position within the
    logical view of a strictly ordered collection.
    """

    __startIndex = None

    @property
    def startIndex(self):
        return self.__startIndex

    @startIndex.setter
    def startIndex(self, val):
        if val is not None:
            if not isinstance(val, int):
                raise ValueError(
                    f'Property "startIndex" must be of type "int"; ' +
                    f'got {val} ({type(val)})')
            if val < 0:
                raise ValueError(
                    f'Property "startIndex" must be greater than 0; ' +
                    f'got {val}'
                )
        self.__startIndex = val


class SummaryProperty:
    """
    A natural language summarization of the object encoded as HTML. Multiple
    language tagged summaries MAY be provided.
    """

    __summary = None

    @property
    def summary(self):
        return self.__summary

    @summary.setter
    def summary(self, val):
        if val is not None and not isinstance(val, str):
            raise ValueError(
                f'Property "summary" must be of type "str"; ' +
                f'got {val} ({type(val)})')
        self.__summary = val


class TotalItemsProperty:
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
    def totalItems(self, val):
        if val is not None:
            if not isinstance(val, int):
                raise ValueError(
                    f'Property "totalItems" must be of type "int"; ' +
                    f'got {val} ({type(val)})')
            if val < 0:
                raise ValueError(
                    f'Property "totalItems" must be greater than 0; ' +
                    f'got {val}'
                )
        self.__totalItems = val


class UnitsProperty:
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
    def units(self, val):
        if val is not None and not isinstance(val, str):
            raise ValueError(
                f'Property "units" must be of type "str"; ' +
                f'got {val} ({type(val)})')
        self.__units = val


class UpdatedProperty:
    """
    The date and time at which the object was updated
    """

    __updated = None

    @property
    def updated(self):
        return self.__updated

    @updated.setter
    def updated(self, val):
        if val is not None and not is_activity_datetime(val):
            raise ValueError(
                f'Property "updated" must be of type "datetime" or "str" ' +
                f'in "YYYY-mm-dd-THH:MM:SSZ" format; ' +
                f'got {val} ({type(val)})')
        self.__updated = parse_activitystream_datetime(val)


class WidthProperty:
    """
    On a Link, specifies a hint as to the rendering width in device-independent
    pixels of the linked resource.
    """

    __width = None

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, val):
        if val is not None:
            if not isinstance(val, int):
                raise ValueError(
                    f'Property "width" must be of type "int"; ' +
                    f'got {val} ({type(val)})')
            if val < 0:
                raise ValueError(
                    f'Property "width" must be greater than 0; ' +
                    f'got {val}'
                )
        self.__width = val


class SubjectProperty:
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
    def subject(self, val):
        if val is not None and not object_or_link(val):
            raise ValueError(
                f'Property "subject" must be of type "Object" or "Link"; ' +
                f'got {val} ({type(val)})')
        self.__subject = val


class RelationshipProperty:
    """
    On a Relationship object, the relationship property identifies the kind of
    relationship that exists between subject and object.
    """

    __relationship = None

    @property
    def relationship(self):
        return self.__relationship

    @relationship.setter
    def relationship(self, val):
        if val is not None and not isinstance(val, ObjectModel):
            raise ValueError(
                f'Property "relationship" must be of type "Object"' +
                f'got {val} ({type(val)})')
        self.__relationship = val


class DescribesProperty:
    """
    On a Profile object, the describes property identifies the object described
    by the Profile.
    """

    __describes = None

    @property
    def describes(self):
        return self.__describes

    @describes.setter
    def describes(self, val):
        if val is not None and not isinstance(val, ObjectModel):
            raise ValueError(
                f'Property "describes" must be of type "Object"' +
                f'got {val} ({type(val)})')
        self.__describes = val


class FormerTypeProperty:
    """
    On a Tombstone object, the formerType property identifies the type of the
    object that was deleted.
    """

    __formerType = None

    @property
    def formerType(self):
        return self.__formerType

    @formerType.setter
    def formerType(self, val):
        if val is not None and not isinstance(val, ObjectModel):
            raise ValueError(
                f'Property "formerType" must be of type "Object"' +
                f'got {val} ({type(val)})')
        self.__formerType = val


class DeletedProperty:
    """
    On a Tombstone object, the deleted property is a timestamp for when the
    object was deleted.
    """

    __deleted = None

    @property
    def deleted(self):
        return self.__deleted

    @deleted.setter
    def deleted(self, val):
        if val is not None and not isinstance(val, ObjectModel):
            raise ValueError(
                f'Property "deleted" must be of type "Object"' +
                f'got {val} ({type(val)})')
        self.__deleted = val


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# CORE TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#types
#
#   These classes serve as the basis for all other classes
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

# this insane cluster of inheritance might look bad, but it's actually a lot
# easier to manage the properties if we make them their own classes
class ObjectModel(ApplicationActivityJson, IdProperty, AttachmentProperty,
                  AttributedToProperty, AudienceProperty, ContentProperty,
                  ContextProperty, NameProperty, TypeProperty,
                  EndTimeProperty, GeneratorProperty, IconProperty,
                  ImageProperty,
                  InReplyToProperty, LocationProperty, PreviewProperty,
                  PublishedProperty, RepliesProperty, StartTimeProperty,
                  SummaryProperty, TagProperty, UpdatedProperty, UrlProperty,
                  ToProperty, BtoProperty, CcProperty, BccProperty,
                  MediaTypeProperty, DurationProperty):
    """
    Describes an object of any kind. The Object type serves as the base type
    for most of the other kinds of objects defined in the Activity
    Vocabulary, including other Core types such as Activity,
    IntransitiveActivity, Collection and OrderedCollection.
    """
    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None,
                 acontext='https://www.w3.org/ns/activitystreams'):
        ApplicationActivityJson.__init__(self, acontext=acontext)
        self.id = id
        self.type = type or self.type
        self.attachment = attachment
        self.attributedTo = attributedTo
        self.audience = audience
        self.content = content
        self.context = context
        self.name = name
        self.endTime = endTime
        self.generator = generator
        self.icon = icon
        self.image = image
        self.inReplyTo = inReplyTo
        self.location = location
        self.preview = preview
        self.published = published
        self.replies = replies
        self.startTime = startTime
        self.summary = summary
        self.tag = tag
        self.updated = updated
        self.url = url
        self.to = to
        self.bto = bto
        self.cc = cc
        self.bcc = bcc
        self.mediaType = mediaType
        self.duration = duration


class LinkModel(HrefProperty, RelProperty, MediaTypeProperty, NameProperty,
                HrefLangProperty, HeightProperty, WidthProperty,
                PreviewProperty, TypeProperty, ApplicationActivityJson):
    """
    A Link is an indirect, qualified reference to a resource identified by a
    URL. The fundamental model for links is established by [RFC5988]. Many
    of the properties defined by the Activity Vocabulary allow values that are
    either instances of Object or Link. When a Link is used, it establishes a
    qualified relation connecting the subject (the containing object) to the
    resource identified by the href. Properties of the Link are properties of
    the reference as opposed to properties of the resource
    """

    def __init__(self, href=None, rel=None, mediaType=None, name=None,
                 hreflang=None, height=None, width=None, preview=None,
                 context=None, type=None,
                 acontext='https://www.w3.org/ns/activitystreams'):
        # grants the ability to access all @property objects associated with the
        # model via __properties__ on instantiated objects and
        # __get_properties__ on classes
        ApplicationActivityJson.__init__(self, acontext=acontext)
        self.href = href
        self.rel = rel
        self.mediaType = mediaType
        self.name = name
        self.hreflang = hreflang
        self.height = height
        self.width = width
        self.preview = preview
        self.context = context
        self.type = type or self.__type


class ActivityModel(ObjectModel,
                    ActorProperty, ObjectProperty, TargetProperty,
                    ResultProperty, OriginProperty, InstrumentProperty):
    """
    An Activity is a subtype of Object that describes some form of action
    that may happen, is currently happening, or has already happened. The
    Activity type itself serves as an abstract base type for all types of
    activities. It is important to note that the Activity type itself does
    not carry any specific semantics about the kind of action being taken.
    :arg actor:
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, actor=None, object=None,
                 target=None, result=None, origin=None, instrument=None,
                 acontext='https://www.w3.org/ns/activitystreams'):
        # "this looks so bad" I KNOW, but it's the only way to make all the
        # params show up in tooltips! Yes it looks bad! But it makes it easier
        # to work with!!
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType,
                         duration=duration, acontext=acontext)
        self.actor = actor
        self.object = object
        self.target = target
        self.result = result
        self.origin = origin
        self.instrument = instrument


class IntransitiveActivityModel(ActivityModel):
    """
    Instances of IntransitiveActivity are a subtype of Activity representing
    intransitive actions (actions that do not require an object to make sense).
    The object property is therefore inappropriate for these activities.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, actor=None, object=None,
                 target=None, result=None, origin=None, instrument=None,
                 acontext='https://www.w3.org/ns/activitystreams'):
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType,
                         duration=duration, actor=actor, object=object,
                         target=target, result=result, origin=origin,
                         instrument=instrument, acontext=acontext)
        # intransitive activities do NOT inherit the 'object' attribute
        delattr(self, 'object')


class CollectionModel(ObjectModel,
                      TotalItemsProperty, CurrentProperty, FirstProperty,
                      LastProperty, ItemsProperty):
    """
    A Collection is a subtype of Object that represents ordered or unordered
    sets of Object or Link instances.

    Refer to the Activity Streams 2.0 Core specification for a complete
    description of the Collection type.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, totalItems=None, current=None,
                 first=None, last=None, items=None,
                 acontext='https://www.w3.org/ns/activitystreams'):
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType,
                         duration=duration, acontext=acontext)
        self.current = current
        self.first = first
        self.last = last
        # some inheritors may override this with more specific orderings,
        # they should be given precedence
        self.items = self.items if self.items else items

        # supplied value takes priority, followed by size of items if they are
        # sizeable, defaulting to 0 if not
        self.totalItems = totalItems if totalItems else (
            0 if not isinstance(self.items, Sized) else len(self.items)
        )


class OrderedCollectionModel(CollectionModel,
                             OrderedItemsProperty):
    """
    A subtype of Collection in which members of the logical collection are
    assumed to always be strictly ordered.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, totalItems=None, current=None,
                 first=None, last=None, orderedItems=None, items=None,
                 acontext='https://www.w3.org/ns/activitystreams'):
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType, items=items,
                         duration=duration, totalItems=totalItems,
                         current=current, first=first, last=last,
                         acontext=acontext)
        self.orderedItems = orderedItems


class CollectionPageModel(CollectionModel,
                          PartOfProperty, NextProperty, PrevProperty):
    """
    Used to represent distinct subsets of items from a Collection. Refer to the
    Activity Streams 2.0 Core for a complete description of the CollectionPage
    object.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, totalItems=None, current=None,
                 first=None, last=None, items=None, partOf=None, next=None,
                 prev=None, acontext='https://www.w3.org/ns/activitystreams',
                 **kwargs):
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType,
                         duration=duration, totalItems=totalItems,
                         current=current, first=first, last=last, items=items,
                         acontext=acontext)
        self.partOf = partOf
        self.next = next
        self.prev = prev


class OrderedCollectionPageModel(OrderedCollectionModel, CollectionPageModel,
                                 StartIndexProperty):
    """
    Used to represent ordered subsets of items from an OrderedCollection.
    Refer to the Activity Streams 2.0 Core for a complete description of the
    OrderedCollectionPage object.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, totalItems=None, current=None,
                 first=None, last=None, items=None, partOf=None, next=None,
                 prev=None, startIndex=None, orderedItems=None,
                 acontext='https://www.w3.org/ns/activitystreams'):
        # OrderedCollection has no special handling in its init that
        # CollectionPage doesn't already do
        OrderedCollectionModel.__init__(self, orderedItems=orderedItems)
        CollectionPageModel.__init__(self, id=id, type=type,
                                     attachment=attachment,
                                     attributedTo=attributedTo,
                                     audience=audience,
                                     content=content, context=context,
                                     name=name,
                                     endTime=endTime, generator=generator,
                                     icon=icon,
                                     image=image, inReplyTo=inReplyTo,
                                     location=location, preview=preview,
                                     published=published, replies=replies,
                                     startTime=startTime, summary=summary,
                                     tag=tag, updated=updated, url=url, to=to,
                                     bto=bto,
                                     cc=cc, bcc=bcc, mediaType=mediaType,
                                     duration=duration, totalItems=totalItems,
                                     current=current, first=first, last=last,
                                     partOf=partOf, next=next, prev=prev,
                                     acontext=acontext)
        self.startIndex = startIndex if startIndex else 0


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# ACTIVITY TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#activity-types
#
#   These classes serve as the activities that actors perform
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class AcceptModel(ActivityModel):
    """
    Indicates that the actor accepts the object. The target property can be
    used in certain circumstances to indicate the context into which the
    object has been accepted.
    """


class TentativeAcceptModel(AcceptModel):
    """
    A specialization of Accept indicating that the acceptance is tentative.
    """


class AddModel(ActivityModel):
    """
    Indicates that the actor has added the object to the target. If the
    target property is not explicitly specified, the target would need to be
    determined implicitly by context. The origin can be used to identify the
    context from which the object originated.
    """


class ArriveModel(IntransitiveActivityModel):
    """
    An IntransitiveActivity that indicates that the actor has arrived at the
    location. The origin can be used to identify the context from which the
    actor originated. The target typically has no defined meaning.
    """


class CreateModel(ActivityModel):
    """
    Indicates that the actor has created the object.
    """


class DeleteModel(ActivityModel):
    """
    Indicates that the actor has deleted the object. If specified, the origin
    indicates the context from which the object was deleted.
    """


class FollowModel(ActivityModel):
    """
    Indicates that the actor is "following" the object. Following is defined
    in the sense typically used within Social systems in which the actor is
    interested in any activity performed by or on the object. The target and
    origin typically have no defined meaning.
    """


class IgnoreModel(ActivityModel):
    """
    Indicates that the actor is ignoring the object. The target and origin
    typically have no defined meaning.
    """


class JoinModel(ActivityModel):
    """
    Indicates that the actor has joined the object. The target and origin
    typically have no defined meaning.
    """


class LeaveModel(ActivityModel):
    """
    Indicates that the actor has left the object. The target and origin
    typically have no meaning.
    """


class LikeModel(ActivityModel):
    """
    Indicates that the actor likes, recommends or endorses the object. The
    target and origin typically have no defined meaning.
    """


class OfferModel(ActivityModel):
    """
    Indicates that the actor is offering the object. If specified, the target
    indicates the entity to which the object is being offered.
    """


class InviteModel(OfferModel):
    """
    A specialization of Offer in which the actor is extending an invitation
    for the object to the target.
    """


class RejectModel(ActivityModel):
    """
    Indicates that the actor is rejecting the object. The target and origin
    typically have no defined meaning.
    """


class TentativeRejectModel(RejectModel):
    """
    A specialization of Reject in which the rejection is considered tentative.
    """


class RemoveModel(ActivityModel):
    """
    Indicates that the actor is removing the object. If specified,
    the origin indicates the context from which the object is being removed.
    """


class UndoModel(ActivityModel):
    """
    Indicates that the actor is undoing the object. In most cases, the object
    will be an Activity describing some previously performed action (for
    instance, a person may have previously "liked" an article but,
    for whatever reason, might choose to undo that like at some later point
    in time).

    The target and origin typically have no defined meaning.
    """


class UpdateModel(ActivityModel):
    """
    Indicates that the actor has updated the object. Note, however, that this
    vocabulary does not define a mechanism for describing the actual set of
    modifications made to object.

    The target and origin typically have no defined meaning.
    """


class ViewModel(ActivityModel):
    """
    Indicates that the actor has viewed the object.
    """


class ListenModel(ActivityModel):
    """
    Indicates that the actor has listened to the object.
    """


class ReadModel(ActivityModel):
    """
    Indicates that the actor has read the object.
    """


class MoveModel(ActivityModel):
    """
    Indicates that the actor has moved object from origin to target. If the
    origin or target are not specified, either can be determined by context.
    """


class TravelModel(IntransitiveActivityModel):
    """
    Indicates that the actor is traveling to target from origin. Travel is an
    IntransitiveObject whose actor specifies the direct object. If the target
    or origin are not specified, either can be determined by context.
    """


class AnnounceModel(ActivityModel):
    """
    Indicates that the actor is calling the target's attention the object.

    The origin typically has no defined meaning.
    """


class BlockModel(IgnoreModel):
    """
    Indicates that the actor is blocking the object. Blocking is a stronger
    form of Ignore. The typical use is to support social systems that allow
    one user to block activities or content of other users. The target and
    origin typically have no defined meaning.
    """


class FlagModel(ActivityModel):
    """
    Indicates that the actor is "flagging" the object. Flagging is defined in
    the sense common to many social platforms as reporting content as being
    inappropriate for any number of reasons.
    """


class DislikeModel(ActivityModel):
    """
    Indicates that the actor dislikes the object.
    """


class QuestionModel(IntransitiveActivityModel,
                    OneOfProperty, AnyOfProperty, ClosedProperty):
    """
    Represents a question being asked. Question objects are an extension of
    IntransitiveActivity. That is, the Question object is an Activity,
    but the direct object is the question itself, therefore it would not
    contain an object property.

    Either of the anyOf and oneOf properties MAY be used to express possible
    answers, but a Question object MUST NOT have both properties.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, actor=None, object=None,
                 target=None, result=None, origin=None, instrument=None,
                 oneOf=None, anyOf=None, closed=None,
                 acontext='https://www.w3.org/ns/activitystreams'):
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType,
                         duration=duration, actor=actor, object=object,
                         target=target, result=result, origin=origin,
                         instrument=instrument, acontext=acontext)
        self.oneOf = oneOf
        self.anyOf = anyOf
        self.closed = closed


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# ACTOR TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#actor-types
#
#   These classes serve as the actors who interact with the objects on a site
#   and perform activities
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class ApplicationModel(ObjectModel):
    """
    Describes a software application.
    """


class GroupModel(ObjectModel):
    """
    Represents a formal or informal collective of Actors.
    """


class OrganizationModel(ObjectModel):
    """
    Represents an organization.
    """


class PersonModel(ObjectModel):
    """
    Represents an individual person.
    """


class ServiceModel(ObjectModel):
    """
    Represents a service of any kind.
    """


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# OBJECT TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#object-types
#
#   These classes serve as the objects that are acted upon by actors
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class RelationshipModel(ObjectModel, SubjectProperty, ObjectProperty,
                        RelationshipProperty):
    """
    Describes a relationship between two individuals. The subject and object
    properties are used to identify the connected individuals.
    """
    def __init__(self, id, subject=None, object=None, relationship=None,
                 **kwargs):
        super().__init__(id, **kwargs)
        self.subject = subject
        self.object = object
        self.relationship = relationship


class ArticleModel(ObjectModel):
    """
    Represents any kind of multi-paragraph written work.
    """


class DocumentModel(ObjectModel):
    """
    Represents a document of any kind.
    """


class AudioModel(DocumentModel):
    """
    Represents an audio document of any kind.
    """


class ImageModel(DocumentModel):
    """
    An image document of any kind
    """


class VideoModel(DocumentModel):
    """
    Represents a video document of any kind.
    """


class NoteModel(ObjectModel):
    """
    Represents a short written work typically less than a single paragraph in
    length.
    """


class PageModel(DocumentModel):
    """
    Represents a Web Page.
    """


class EventModel(ObjectModel):
    """
    Represents any kind of event.
    """


class PlaceModel(ObjectModel, AccuracyProperty, AltitudeProperty,
                 LatitudeProperty, LongitudeProperty, RadiusProperty,
                 UnitsProperty):
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


class ProfileModel(ObjectModel, DescribesProperty):
    """
    A Profile is a content object that describes another Object, typically
    used to describe Actor Type objects. The describes property is used to
    reference the object being described by the profile.
    """
    def __init__(self, id, describes=None, **kwargs):
        super().__init__(id, **kwargs)
        self.describes = describes


class TombstoneModel(ObjectModel,
                     FormerTypeProperty, DeletedProperty):
    """
    A Tombstone represents a content object that has been deleted. It can be
    used in Collections to signify that there used to be an object at this
    position, but it has been deleted.
    """
    def __init__(self, id, former_type, deleted, **kwargs):
        super().__init__(id, **kwargs)
        self.former_type = former_type
        self.deleted = deleted


class MentionModel(LinkModel):
    """
    A specialized Link that represents a @mention.
    """
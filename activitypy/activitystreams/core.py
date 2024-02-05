"""
The Activity Vocabulary Core Types provide the basis for the rest of the
vocabulary.
"""
__ref__ = 'https://www.w3.org/TR/activitystreams-vocabulary/#types'

from activitypy.activitystreams.utils import PROPERTY_TRANSFORM_MAP, \
    validate_url, validate_acct_or_email

from activitypy.activitystreams.models import OrderedCollectionModel, \
    OrderedCollectionPageModel, CollectionModel, IntransitiveActivityModel, \
    ActivityModel, LinkModel, ObjectModel, CollectionPageModel
from activitypy.activitystreams.models.properties import Actor, \
    AttributedTo, InReplyTo, Object as ObjectProp, Audience, \
    Context, Generator, Icon, Instrument, \
    Location, Origin, Preview, Result, \
    Target, Attachment, Bcc, Cc, Bto, \
    Current, First, Image, Last, Items, \
    OrderedItems, Next, Prev, Tag, To, \
    Url, PartOf
from activitypy.jsonld import JSON_DATA_CONTEXT, ApplicationActivityJson
from activitypy.jsonld.utils import jsonld_get

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LinkManager:
    """Class serving as a decorator that can convert strings into Links"""

    def expand_link(self, data, *args, **kwargs):
        # if LinkModel isn't registered or this isn't a Link, pass the data
        # without expanding
        if not isinstance(data, Link):
            return data

        link = data.__dict__.get('_Href__href', '')
        # if we don't have an href, we can't expand; pass the data forward
        if not link:
            return data

        try:
            resp_data = jsonld_get(link)
        except Exception as e:
            # if we hit an error, pass the data through
            logger.info(f'Encountered an error expanding url {link}' +
                        f'\n{e}')
            return data

        try:
            new_obj = ApplicationActivityJson.from_json(resp_data)
        except Exception as e:
            # if we fail to form the new object, pass the data through
            logger.exception(f'Encountered an error forming object ' +
                             f'from {link}\n{e}')
            return data
        return new_obj

    def getter(self, get_func, *args, **kwargs):
        """
        Decorator for automatically expanding Link objects
        """

        def decorator(obj):
            return self.expand_link(get_func(obj))

        return decorator

    def href_only(self, get_func):
        """
        Decorator for getting only the href value back from a link
        :param get_func: getter function being decorated
        :return: the href of the link
        """
        def decorator(obj):
            val = get_func(obj)
            # if it's a single link, return the href
            if isinstance(val, Link):
                return val.href
            # if it's a list, return either the href or the item (if no href)
            if isinstance(val, list):
                return [item.href if isinstance(item, Link) else item
                        for item in val]
            # if we don't have a handler, just give back what we found
            return val
        return decorator

    def setter(self, set_prop, *args, **kwargs):
        """
        Decorator that allows the setter of a JsonProperty object to convert
        various data types into Link objects as a default
        """
        def create_link(v):
            # if it's a string representing an email, url, or account ref,
            # create a single link
            if (isinstance(v, str) and
                    (validate_url(v) or validate_acct_or_email(v))):
                return Link(href=v)
            if isinstance(v, dict) and v.get('href', None) and validate_url(v.get('href', '')):
                return Link(**v)
            # if it's an iterable other than a string or dict, create many links
            if isinstance(v, (list, tuple, set)):
                return [create_link(item) for item in v]
            return v

        def linkify(obj, val):
            val = create_link(val)
            set_prop(obj, val)
        return linkify


# IMPORTANT NOTE:
# For some reason pycharm seems to think things using the @contextproperty
# decorator rather than the standard @property aren't properties. This is a lie,
# do not trust the machine, he thrives on frustration.
# If it bothers you like it does me, you can disable "Inappropriate access to
# properties" in Pycharm's inspections

class Object(ObjectModel):
    """
    Describes an object of any kind. The Object type serves as the base type
    for most of the other kinds of objects defined in the Activity
    Vocabulary, including other Core types such as Activity,
    IntransitiveActivity, Collection and OrderedCollection.
    """
    type = "Object"
    default_transforms = PROPERTY_TRANSFORM_MAP

    # //// //// //// //// attachment start //// //// //// ////
    @Attachment.attachment.getter
    @LinkManager().getter
    def attachment(self):
        """
        Identifies a resource attached or related to an object that potentially
        requires special handling. The intent is to provide a model that is at
        least semantically similar to attachments in email.
        :return: Object
        :raises ValueError: If a non-Object or non-Link assignment is attempted
        """
        return Attachment.attachment.fget(self)

    @attachment.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def attachment(self):
        return Attachment.attachment.fget(self)

    @attachment.setter
    @LinkManager().setter
    def attachment(self, val):
        Attachment.attachment.fset(self, val)

    # //// //// //// //// attributedTo start //// //// //// ////
    @AttributedTo.attributedTo.getter
    @LinkManager().getter
    def attributedTo(self):
        """
        Identifies one or more entities to which this object is attributed. The
        attributed entities might not be Actors. For instance, an object might
        be attributed to the completion of another activity.
        :return: Object or Link
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return AttributedTo.attributedTo.fget(self)

    @attributedTo.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def attributedTo(self):
        return AttributedTo.attributedTo.fget(self)

    @attributedTo.setter
    @LinkManager().setter
    def attributedTo(self, val):
        AttributedTo.attributedTo.fset(self, val)

    # //// //// //// //// audience start //// //// //// ////
    @Audience.audience.getter
    @LinkManager().getter
    def audience(self):
        """
        Identifies one or more entities that represent the total population
        of entities for which the object can considered to be relevant.
        :return: Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Audience.audience.fget(self)

    @audience.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def audience(self):
        return Audience.audience.fget(self)

    @audience.setter
    @LinkManager().setter
    def audience(self, val):
        Audience.audience.fset(self, val)

    # //// //// //// //// to start //// //// //// ////
    @To.to.getter
    @LinkManager().getter
    def to(self):
        """
        Identifies an entity considered to be part of the public primary
        audience of an Object
        :return: Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return To.to.fget(self)

    @to.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def to(self):
        return To.to.fget(self)

    @to.setter
    @LinkManager().setter
    def to(self, val):
        To.to.fset(self, val)

    # //// //// //// //// bcc start //// //// //// ////
    @Bcc.bcc.getter
    @LinkManager().getter
    def bcc(self):
        """
        Identifies one or more Objects that are part of the private
        secondary audience of this Object.
        :return: Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Bcc.bcc.fget(self)

    @bcc.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def bcc(self):
        return Bcc.bcc.fget(self)

    @bcc.setter
    @LinkManager().setter
    def bcc(self, val):
        Bcc.bcc.fset(self, val)

    # //// //// //// //// bto start //// //// //// ////
    @Bto.bto.getter
    @LinkManager().getter
    def bto(self):
        """
        Identifies an Object that is part of the private primary audience of
        this Object.
        :return: Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Bto.bto.fget(self)

    @bto.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def bto(self):
        return Bto.bto.fget(self)

    @bto.setter
    @LinkManager().setter
    def bto(self, val):
        Bto.bto.fset(self, val)

    # //// //// //// //// cc start //// //// //// ////
    @Cc.cc.getter
    @LinkManager().getter
    def cc(self):
        """
        Identifies an Object that is part of the private primary audience of
        this Object.
        :return: Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Cc.cc.fget(self)

    @cc.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def cc(self):
        return Cc.cc.fget(self)

    @cc.setter
    @LinkManager().setter
    def cc(self, val):
        Cc.cc.fset(self, val)

    # //// //// //// //// context start //// //// //// ////
    @Context.context.getter
    @LinkManager().getter
    def context(self):
        """
        This property has ZERO RELATIONSHIP with the activitypy jsonld context
        management tools! It is part of the activitystreams specification!

        Identifies the context within which the object exists or an activity
        was performed.

        The notion of "context" used is intentionally vague. The intended
        function is to serve as a means of grouping objects and activities that
        share a common originating context or purpose. An example could be all
        activities relating to a common project or event.
        :return: Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Context.context.fget(self)

    @context.getter_context(JSON_DATA_CONTEXT)
    def context(self):
        return Context.context.fget(self)

    @context.setter
    @LinkManager().setter
    def context(self, val):
        Context.context.fset(self, val)

    # //// //// //// //// generator start //// //// //// ////
    @Generator.generator.getter
    @LinkManager().getter
    def generator(self):
        """
        Identifies the entity (e.g. an application) that generated the object.
        :return: Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Generator.generator.fget(self)

    @generator.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def generator(self):
        return Generator.generator.fget(self)

    @generator.setter
    @LinkManager().setter
    def generator(self, val):
        Generator.generator.fset(self, val)

    # //// //// //// //// icon start //// //// //// ////
    @Icon.icon.getter
    @LinkManager().getter
    def icon(self):
        """
        Indicates an entity that describes an icon for this object. The image
        should have an aspect ratio of one (horizontal) to one (vertical) and
        should be suitable for presentation at a small size.
        :return: Object
        :raises ValueError: if non-Link or non-Image assignment is attempted
        """
        return Icon.icon.fget(self)

    @icon.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def icon(self):
        return Icon.icon.fget(self)

    @icon.setter
    @LinkManager().setter
    def icon(self, val):
        Icon.icon.fset(self, val)

    # //// //// //// //// image start //// //// //// ////
    @Image.image.getter
    @LinkManager().getter
    def image(self):
        """
        Indicates an entity that describes an image for this object. Unlike the
        icon property, there are no aspect ratio or display size limitations
        assumed.
        :return: Object
        :raises ValueError: if non-Link or non-Image assignment is attempted
        """
        return Image.image.fget(self)

    @image.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def image(self):
        return Image.image.fget(self)

    @image.setter
    @LinkManager().setter
    def image(self, val):
        Image.image.fset(self, val)

    # //// //// //// //// inReplyTo start //// //// //// ////
    @InReplyTo.inReplyTo.getter
    @LinkManager().getter
    def inReplyTo(self):
        """
        Indicates one or more entities for which this object is considered a
        response.
        :return: Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return InReplyTo.inReplyTo.fget(self)

    @inReplyTo.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def inReplyTo(self):
        return InReplyTo.inReplyTo.fget(self)

    @inReplyTo.setter
    @LinkManager().setter
    def inReplyTo(self, val):
        InReplyTo.inReplyTo.fset(self, val)

    # //// //// //// //// location start //// //// //// ////
    @Location.location.getter
    @LinkManager().getter
    def location(self):
        """
        Indicates one or more physical or logical locations associated with the
        object.
        :return: Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Location.location.fget(self)

    @location.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def location(self):
        return Location.location.fget(self)

    @location.setter
    @LinkManager().setter
    def location(self, val):
        Location.location.fset(self, val)

    # //// //// //// //// preview start //// //// //// ////
    @Preview.preview.getter
    @LinkManager().getter
    def preview(self):
        """
        Identifies an entity that provides a preview of this object.
        :return: Object or Link
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Preview.preview.fget(self)

    @preview.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def preview(self):
        return Preview.preview.fget(self)

    @preview.setter
    @LinkManager().setter
    def preview(self, val):
        Preview.preview.fset(self, val)

    # //// //// //// //// tag start //// //// //// ////
    @Tag.tag.getter
    @LinkManager().getter
    def tag(self):
        """
        One or more "tags" that have been associated with an objects. A tag can
        be any kind of Object. The key difference between attachment and tag is
        that the former implies association by inclusion, while the latter
        implies associated by reference.
        :return: Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Tag.tag.fget(self)

    @tag.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def tag(self):
        return Tag.tag.fget(self)

    @tag.setter
    @LinkManager().setter
    def tag(self, val):
        Tag.tag.fset(self, val)

    # //// //// //// //// url start //// //// //// ////
    @Url.url.getter
    @LinkManager().getter
    def url(self):
        """
        Identifies one or more links to representations of the object
        :return: Link or str
        :raises ValueError: if non-Link or non-string assignment is attempted
        """
        return Url.url.fget(self)

    @url.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def url(self):
        return Url.url.fget(self)

    @url.setter
    @LinkManager().setter
    def url(self, val):
        Url.url.fset(self, val)


class Link(LinkModel):
    """
    A Link is an indirect, qualified reference to a resource identified by a
    URL. The fundamental model for links is established by [RFC5988]. Many
    of the properties defined by the Activity Vocabulary allow values that are
    either instances of Object or Link. When a Link is used, it establishes a
    qualified relation connecting the subject (the containing object) to the
    resource identified by the href. Properties of the Link are properties of
    the reference as opposed to properties of the resource
    """
    type = "Link"
    default_transforms = PROPERTY_TRANSFORM_MAP

    @Preview.preview.getter
    @LinkManager().getter
    def preview(self):
        """
        Identifies an entity that provides a preview of this object.
        :return: Object or Link
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Preview.preview.fget(self)

    @preview.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def preview(self):
        return Preview.preview.fget(self)

    @preview.setter
    @LinkManager().setter
    def preview(self, val):
        Preview.preview.fset(self, val)


class Activity(Object, ActivityModel):
    """
    An Activity is a subtype of Object that describes some form of action
    that may happen, is currently happening, or has already happened. The
    Activity type itself serves as an abstract base type for all types of
    activities. It is important to note that the Activity type itself does
    not carry any specific semantics about the kind of action being taken.
    """
    type = "Activity"

    # //// //// //// //// //// //// actor //// //// //// //// //// ////
    @Actor.actor.getter
    @LinkManager().getter
    def actor(self):
        """
        Describes one or more entities that either performed or are expected to
        perform the activity. Any single activity can have multiple actors. The
        actor MAY be specified using an indirect Link.
        :return: Object or Link
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Actor.actor.fget(self)

    @actor.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def actor(self):
        return Actor.actor.fget(self)

    @actor.setter
    @LinkManager().setter
    def actor(self, val):
        Actor.actor.fset(self, val)

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

    # //// //// //// //// //// //// instrument //// //// //// //// //// ////
    @Instrument.instrument.getter
    @LinkManager().getter
    def instrument(self):
        """
        Identifies one or more objects used (or to be used) in the completion
        of an Activity.
        :return: Link or Object
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Instrument.instrument.fget(self)

    @instrument.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def instrument(self):
        return Instrument.instrument.fget(self)

    @instrument.setter
    @LinkManager().setter
    def instrument(self, val):
        Instrument.instrument.fset(self, val)

    # //// //// //// //// //// //// origin //// //// //// //// //// ////
    @Origin.origin.getter
    @LinkManager().getter
    def origin(self):
        """
        Describes an indirect object of the activity from which the activity is
        directed. The precise meaning of the origin is the object of the
        English preposition "from". For instance, in the activity "John moved
        an item to List B from List A", the origin of the activity is "List A".
        :return: Object or Link
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Origin.origin.fget(self)

    @origin.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def origin(self):
        return Origin.origin.fget(self)

    @origin.setter
    @LinkManager().setter
    def origin(self, val):
        Origin.origin.fset(self, val)

    # //// //// //// //// //// //// result //// //// //// //// //// ////
    @Result.result.getter
    @LinkManager().getter
    def result(self):
        """
        Describes the result of the activity. For instance, if a particular
        action results in the creation of a new resource, the result property
        can be used to describe that new resource.
        :return: Object or Link
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Result.result.fget(self)

    @result.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def result(self):
        return Result.result.fget(self)

    @result.setter
    @LinkManager().setter
    def result(self, val):
        Result.result.fset(self, val)

    # //// //// //// //// //// //// target //// //// //// //// //// ////
    @Target.target.getter
    @LinkManager().getter
    def target(self):
        """
        Describes the indirect object, or target, of the activity. The precise
        meaning of the target is largely dependent on the type of action being
        described but will often be the object of the English preposition "to".
        For instance, in the activity "John added a movie to his wishlist", the
        target of the activity is John's wishlist. An activity can have more
        than one target.
        :return: Object or Link
        :raises ValueError: if non-Link or non-Object assignment is attempted
        """
        return Target.target.fget(self)

    @target.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def target(self):
        return Target.target.fget(self)

    @target.setter
    @LinkManager().setter
    def target(self, val):
        Target.target.fset(self, val)


class IntransitiveActivity(Activity, IntransitiveActivityModel):
    """
    Instances of IntransitiveActivity are a subtype of Activity representing
    intransitive actions (actions that do not require an object to make sense).
    The object property is therefore inappropriate for these activities.
    """
    type = "IntransitiveActivity"


class Collection(Object, CollectionModel):
    """
    A Collection is a subtype of Object that represents ordered or unordered
    sets of Object or Link instances.

    Refer to the Activity Streams 2.0 Core specification for a complete
    description of the Collection type.
    """
    type = "Collection"

    # //// //// //// //// //// //// current //// //// //// //// //// ////
    @Current.current.getter
    @LinkManager().getter
    def current(self):
        """
        In a paged Collection, indicates the page that contains the most
        recently updated member items.
        :return: CollectionPage or Link
        :raises ValueError: if non-Link or non-CollectionPage assignment is attempted
        """
        return Current.current.fget(self)

    @current.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def current(self):
        return Current.current.fget(self)

    @current.setter
    @LinkManager().setter
    def current(self, val):
        Current.current.fset(self, val)

    # //// //// //// //// //// //// items //// //// //// //// //// ////
    @Items.items.getter
    @LinkManager().getter
    def items(self):
        """
        Identifies the items contained in a collection. The items might be
        ordered or unordered.
        :return: Object, Link, or list[Object | Link]
        :raises ValueError: if non-Link, Object, or list assignment is attempted
        """
        return Items.items.fget(self)

    @Items.items.setter
    @LinkManager().setter
    def items(self, items):
        Items.items.fset(self, items)
        if items:
            self.totalItems = len(items)

    @items.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def items(self):
        return Items.items.fget(self)

    def __iter__(self):
        if not self.items:
            yield
        for item in self.items:
            yield item


class OrderedCollection(Collection, OrderedCollectionModel):
    """
    A subtype of Collection in which members of the logical collection are
    assumed to always be strictly ordered.
    """
    type = "OrderedCollection"

    # //// //// //// //// //// //// orderedItems //// //// //// //// //// ////
    @OrderedItems.orderedItems.getter
    @LinkManager().getter
    def orderedItems(self):
        """
        Identifies the items contained in a collection. The items are ordered
        :return: Object, Link, or list[Object | Link]
        :raises ValueError: if non-Link, Object, or list assignment is attempted
        """
        return OrderedItems.orderedItems.fget(self)

    @orderedItems.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def orderedItems(self):
        return OrderedItems.orderedItems.fget(self)

    @orderedItems.setter
    @LinkManager().setter
    def orderedItems(self, val):
        OrderedItems.orderedItems.fset(self, val)


class CollectionPage(Collection, CollectionPageModel):
    """
    Used to represent distinct subsets of items from a Collection. Refer to the
    Activity Streams 2.0 Core for a complete description of the CollectionPage
    object.
    """
    type = "CollectionPage"

    # //// //// //// //// //// //// first //// //// //// //// //// ////
    @First.first.getter
    @LinkManager().getter
    def first(self):
        return First.first.fget(self)

    @first.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def first(self):
        return First.first.fget(self)

    @first.setter
    @LinkManager().setter
    def first(self, val):
        First.first.fset(self, val)

    # //// //// //// //// //// //// last //// //// //// //// //// ////
    @Last.last.getter
    @LinkManager().getter
    def last(self):
        """
        In a paged Collection, indicates the furthest proceeding page of the
        collection.
        :return: CollectionPage or Link
        :raises ValueError: if non-CollectionPage or non-Link assignment is attempted
        """
        return Last.last.fget(self)

    @last.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def last(self):
        return Last.last.fget(self)

    @last.setter
    @LinkManager().setter
    def last(self, val):
        Last.last.fset(self, val)

    # //// //// //// //// //// //// next //// //// //// //// //// ////
    @Next.next.getter
    @LinkManager().getter
    def next(self):
        """
        In a paged Collection, indicates the next page of items.
        :return: CollectionPage or Link
        :raises ValueError: if non-CollectionPage or non-Link assignment is attempted
        """
        return Next.next.fget(self)

    @next.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def next(self):
        return Next.next.fget(self)

    @next.setter
    @LinkManager().setter
    def next(self, val):
        Next.next.fset(self, val)

    # //// //// //// //// //// //// partOf //// //// //// //// //// ////
    @PartOf.partOf.getter
    @LinkManager().getter
    def partOf(self):
        """
        Identifies the Collection to which a CollectionPage objects items
        belong.
        :return: Link or CollectionPage
        :raises ValueError: if non-Link or non-CollectionPage assignment attempted
        """
        return PartOf.partOf.fget(self)

    @partOf.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def partOf(self):
        return PartOf.partOf.fget(self)

    @partOf.setter
    @LinkManager().setter
    def partOf(self, val):
        PartOf.partOf.fset(self, val)

    # //// //// //// //// //// //// prev //// //// //// //// //// ////
    @Prev.prev.getter
    @LinkManager().getter
    def prev(self):
        """
        In a paged Collection, identifies the previous page of items.
        :return: Link or CollectionPage
        :raises ValueError: if non-Link or non-CollectionPage assignment attempted
        """
        return Prev.prev.fget(self)

    @prev.getter_context(JSON_DATA_CONTEXT)
    @LinkManager().href_only
    def prev(self):
        return Prev.prev.fget(self)

    @prev.setter
    @LinkManager().setter
    def prev(self, val):
        Prev.prev.fset(self, val)


class OrderedCollectionPage(OrderedCollection, CollectionPage,
                            OrderedCollectionPageModel):
    """
    Used to represent ordered subsets of items from an OrderedCollection.
    Refer to the Activity Streams 2.0 Core for a complete description of the
    OrderedCollectionPage object.
    """
    type = "OrderedCollectionPage"

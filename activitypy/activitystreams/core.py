"""
The Activity Vocabulary Core Types provide the basis for the rest of the
vocabulary.
"""
__ref__ = 'https://www.w3.org/TR/activitystreams-vocabulary/#types'

from activitypy.activitystreams.utils import PROPERTY_TRANSFORM_MAP, \
    validate_url

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


class Linkify:
    """Class serving as a decorator that can convert strings into Links"""
    def __init__(self, convert_dicts: bool = False):
        """
        :param convert_dicts: Convert all untyped dicts to links
        """
        self.convert_dicts = convert_dicts

    def __call__(self, set_prop, *args, **kwargs):
        def create_link(v):
            # if it's a string, create a single link
            if isinstance(v, str) and validate_url(v):
                return Link(href=v)
            if isinstance(v, dict) and v.get('href', None) and validate_url(v.get('href', '')):
                return Link(**v)
            if isinstance(v, dict) and self.convert_dicts and \
                    (not hasattr(v, 'type') or not getattr(v, 'type')):
                # if convert_dicts is True, convert every untyped dict value to
                # a link. If that fails try to convert it to an object instead
                try:
                    return Link(**v)
                except Exception as e:
                    return Object(**v)
            # if it's an iterable other than a string or dict, create many links
            if isinstance(v, (list, tuple, set)):
                return [create_link(item) for item in v]
            return v

        def linkify(obj, val):
            val = create_link(val)
            set_prop(obj, val)
        return linkify


class Object(ObjectModel):
    """
    Describes an object of any kind. The Object type serves as the base type
    for most of the other kinds of objects defined in the Activity
    Vocabulary, including other Core types such as Activity,
    IntransitiveActivity, Collection and OrderedCollection.
    """
    type = "Object"
    default_transforms = PROPERTY_TRANSFORM_MAP

    @Attachment.attachment.setter
    @Linkify()
    def attachment(self, val):
        Attachment.attachment.fset(self, val)

    @AttributedTo.attributedTo.setter
    @Linkify()
    def attributedTo(self, val):
        AttributedTo.attributedTo.fset(self, val)

    @Audience.audience.setter
    @Linkify()
    def audience(self, val):
        Audience.audience.fset(self, val)

    @To.to.setter
    @Linkify()
    def to(self, val):
        To.to.fset(self, val)

    @Bcc.bcc.setter
    @Linkify()
    def bcc(self, value):
        Bcc.bcc.fset(self, value)

    @Bto.bto.setter
    @Linkify()
    def bto(self, value):
        Bto.bto.fset(self, value)

    @Cc.cc.setter
    @Linkify()
    def cc(self, value):
        Cc.cc.fset(self, value)

    @Context.context.setter
    @Linkify()
    def context(self, val):
        Context.context.fset(self, val)

    @Generator.generator.setter
    @Linkify()
    def generator(self, val):
        Generator.generator.fset(self, val)

    @Icon.icon.setter
    @Linkify()
    def icon(self, val):
        Icon.icon.fset(self, val)

    @Image.image.setter
    @Linkify()
    def image(self, val):
        Image.image.fset(self, val)

    @InReplyTo.inReplyTo.setter
    @Linkify()
    def inReplyTo(self, val):
        InReplyTo.inReplyTo.fset(self, val)

    @Location.location.setter
    @Linkify()
    def location(self, val):
        Location.location.fset(self, val)

    @Preview.preview.setter
    @Linkify()
    def preview(self, val):
        Preview.preview.fset(self, val)

    @Tag.tag.setter
    @Linkify(convert_dicts=True)
    def tag(self, val):
        Tag.tag.fset(self, val)

    @Url.url.setter
    @Linkify()
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

    @Preview.preview.setter
    @Linkify()
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

    # wraps the actor property's setter; converts raw strings into Link objects
    # it still performs the standard type checking, it just normalizes incoming
    # strings for the purpose of handling incoming json
    @Actor.actor.setter
    @Linkify()
    def actor(self, val):
        Actor.actor.fset(self, val)

    @ObjectProp.object.setter
    @Linkify()
    def object(self, val):
        ObjectProp.object.fset(self, val)

    @Instrument.instrument.setter
    @Linkify()
    def instrument(self, val):
        Instrument.instrument.fset(self, val)

    @Origin.origin.setter
    @Linkify()
    def origin(self, val):
        Origin.origin.fset(self, val)

    @Result.result.setter
    @Linkify()
    def result(self, val):
        Result.result.fset(self, val)

    @Target.target.setter
    @Linkify()
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

    @Current.current.setter
    @Linkify()
    def current(self, val):
        Current.current.fset(self, val)

    @Items.items.setter
    @Linkify()
    def items(self, items):
        Items.items.fset(self, items)
        if items:
            self.totalItems = len(items)

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

    @OrderedItems.orderedItems.setter
    @Linkify()
    def orderedItems(self, val):
        OrderedItems.orderedItems.fset(self, val)


class CollectionPage(Collection, CollectionPageModel):
    """
    Used to represent distinct subsets of items from a Collection. Refer to the
    Activity Streams 2.0 Core for a complete description of the CollectionPage
    object.
    """
    type = "CollectionPage"

    @First.first.setter
    @Linkify()
    def first(self, val):
        First.first.fset(self, val)

    @Last.last.setter
    @Linkify()
    def last(self, val):
        Last.last.fset(self, val)

    @Next.next.setter
    @Linkify()
    def next(self, val):
        Next.next.fset(self, val)

    @PartOf.partOf.setter
    @Linkify()
    def partOf(self, val):
        PartOf.partOf.fset(self, val)

    @Prev.prev.setter
    @Linkify()
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

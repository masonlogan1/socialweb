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
from activitypy.activitystreams.models.models import ActorProperty, \
    AttributedToProperty, InReplyToProperty, ObjectProperty, AudienceProperty, \
    ContextProperty, GeneratorProperty, IconProperty, InstrumentProperty, \
    LocationProperty, OriginProperty, PreviewProperty, ResultProperty, \
    TargetProperty, AttachmentProperty, BccProperty, CcProperty, BtoProperty, \
    CurrentProperty, FirstProperty, ImageProperty, LastProperty, ItemsProperty, \
    OrderedItemsProperty, NextProperty, PrevProperty, TagProperty, ToProperty, \
    UrlProperty, PartOfProperty


class Linkify:
    """Class serving as a decorator that can convert strings into Links"""
    def __call__(self, set_prop, *args, **kwargs):
        def create_link(v):
            # if it's a string, create a single link
            if isinstance(v, str) and validate_url(v):
                return Link(href=v)
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

    @AttachmentProperty.attachment.setter
    @Linkify()
    def attachment(self, val):
        AttachmentProperty.attachment.fset(self, val)

    @AttributedToProperty.attributedTo.setter
    @Linkify()
    def attributedTo(self, val):
        AttributedToProperty.attributedTo.fset(self, val)

    @AudienceProperty.audience.setter
    @Linkify()
    def audience(self, val):
        AudienceProperty.audience.fset(self, val)

    @ToProperty.to.setter
    @Linkify()
    def to(self, val):
        ToProperty.to.fset(self, val)

    @BccProperty.bcc.setter
    @Linkify()
    def bcc(self, value):
        BccProperty.bcc.fset(self, value)

    @BtoProperty.bto.setter
    @Linkify()
    def bto(self, value):
        BtoProperty.bto.fset(self, value)

    @CcProperty.cc.setter
    @Linkify()
    def cc(self, value):
        CcProperty.cc.fset(self, value)

    @ContextProperty.context.setter
    @Linkify()
    def context(self, val):
        ContextProperty.context.fset(self, val)

    @GeneratorProperty.generator.setter
    @Linkify()
    def generator(self, val):
        GeneratorProperty.generator.fset(self, val)

    @IconProperty.icon.setter
    @Linkify()
    def icon(self, val):
        IconProperty.icon.fset(self, val)

    @ImageProperty.image.setter
    @Linkify()
    def image(self, val):
        ImageProperty.image.fset(self, val)

    @InReplyToProperty.inReplyTo.setter
    @Linkify()
    def inReplyTo(self, val):
        InReplyToProperty.inReplyTo.fset(self, val)

    @LocationProperty.location.setter
    @Linkify()
    def location(self, val):
        LocationProperty.location.fset(self, val)

    @PreviewProperty.preview.setter
    @Linkify()
    def preview(self, val):
        PreviewProperty.preview.fset(self, val)

    @TagProperty.tag.setter
    @Linkify()
    def tag(self, val):
        TagProperty.tag.fset(self, val)

    @UrlProperty.url.setter
    @Linkify()
    def url(self, val):
        UrlProperty.url.fset(self, val)


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

    @PreviewProperty.preview.setter
    @Linkify()
    def preview(self, val):
        PreviewProperty.preview.fset(self, val)


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
    @ActorProperty.actor.setter
    @Linkify()
    def actor(self, val):
        ActorProperty.actor.fset(self, val)

    @ObjectProperty.object.setter
    @Linkify()
    def object(self, val):
        ObjectProperty.object.fset(self, val)

    @InstrumentProperty.instrument.setter
    @Linkify()
    def instrument(self, val):
        InstrumentProperty.instrument.fset(self, val)

    @OriginProperty.origin.setter
    @Linkify()
    def origin(self, val):
        OriginProperty.origin.fset(self, val)

    @ResultProperty.result.setter
    @Linkify()
    def result(self, val):
        ResultProperty.result.fset(self, val)

    @TargetProperty.target.setter
    @Linkify()
    def target(self, val):
        TargetProperty.target.fset(self, val)


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

    @CurrentProperty.current.setter
    @Linkify()
    def current(self, val):
        CurrentProperty.current.fset(self, val)

    @ItemsProperty.items.setter
    @Linkify()
    def items(self, items):
        ItemsProperty.items.fset(self, items)
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

    @OrderedItemsProperty.orderedItems.setter
    @Linkify()
    def orderedItems(self, val):
        OrderedItemsProperty.orderedItems.fset(self, val)


class CollectionPage(Collection, CollectionPageModel):
    """
    Used to represent distinct subsets of items from a Collection. Refer to the
    Activity Streams 2.0 Core for a complete description of the CollectionPage
    object.
    """
    type = "CollectionPage"

    @FirstProperty.first.setter
    @Linkify()
    def first(self, val):
        FirstProperty.first.fset(self, val)

    @LastProperty.last.setter
    @Linkify()
    def last(self, val):
        LastProperty.last.fset(self, val)

    @NextProperty.next.setter
    @Linkify()
    def next(self, val):
        NextProperty.next.fset(self, val)

    @PartOfProperty.partOf.setter
    @Linkify()
    def partOf(self, val):
        PartOfProperty.partOf.fset(self, val)

    @PrevProperty.prev.setter
    @Linkify()
    def prev(self, val):
        PrevProperty.prev.fset(self, val)


class OrderedCollectionPage(OrderedCollection, CollectionPage,
                            OrderedCollectionPageModel):
    """
    Used to represent ordered subsets of items from an OrderedCollection.
    Refer to the Activity Streams 2.0 Core for a complete description of the
    OrderedCollectionPage object.
    """
    type = "OrderedCollectionPage"

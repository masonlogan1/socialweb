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
    TargetProperty


class Object(ObjectModel):
    """
    Describes an object of any kind. The Object type serves as the base type
    for most of the other kinds of objects defined in the Activity
    Vocabulary, including other Core types such as Activity,
    IntransitiveActivity, Collection and OrderedCollection.
    """
    type = "Object"
    default_transforms = PROPERTY_TRANSFORM_MAP

    @AttributedToProperty.attributedTo.setter
    def attributedTo(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        AttributedToProperty.attributedTo.fset(self, val)

    @InReplyToProperty.inReplyTo.setter
    def inReplyTo(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        InReplyToProperty.inReplyTo.fset(self, val)

    @AudienceProperty.audience.setter
    def audience(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        AudienceProperty.audience.fset(self, val)

    @ContextProperty.context.setter
    def context(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        ContextProperty.context.fset(self, val)

    @GeneratorProperty.generator.setter
    def generator(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        GeneratorProperty.generator.fset(self, val)

    @IconProperty.icon.setter
    def icon(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        IconProperty.icon.fset(self, val)

    @LocationProperty.location.setter
    def location(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        LocationProperty.location.fset(self, val)

    @PreviewProperty.preview.setter
    def preview(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        PreviewProperty.preview.fset(self, val)


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
    def preview(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
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
    def actor(self, val):
        if isinstance(val, str):
            val = Link(href=val)
        ActorProperty.actor.fset(self, val)

    @ObjectProperty.object.setter
    def object(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        ObjectProperty.object.fset(self, val)

    @InstrumentProperty.instrument.setter
    def instrument(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        InstrumentProperty.instrument.fset(self, val)

    @OriginProperty.origin.setter
    def origin(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        OriginProperty.origin.fset(self, val)

    @ResultProperty.result.setter
    def result(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
        ResultProperty.result.fset(self, val)

    @TargetProperty.target.setter
    def target(self, val):
        if isinstance(val, str) and validate_url(val):
            val = Link(href=val)
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


class CollectionPage(Collection, CollectionPageModel):
    """
    Used to represent distinct subsets of items from a Collection. Refer to the
    Activity Streams 2.0 Core for a complete description of the CollectionPage
    object.
    """
    type = "CollectionPage"


class OrderedCollectionPage(OrderedCollection, CollectionPage,
                            OrderedCollectionPageModel):
    """
    Used to represent ordered subsets of items from an OrderedCollection.
    Refer to the Activity Streams 2.0 Core for a complete description of the
    OrderedCollectionPage object.
    """
    type = "OrderedCollectionPage"

"""
The Activity Vocabulary Core Types provide the basis for the rest of the
vocabulary.
"""
__ref__ = 'https://www.w3.org/TR/activitystreams-vocabulary/#types'

from activitypy.activitystreams.utils import PROPERTY_TRANSFORM_MAP, \
    validate_url
from activitypy.activitystreams.models.utils import LinkExpander
from activitypy.jsonld.base import PropertyContext

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


class LinkManager:
    """Class serving as a decorator that can convert strings into Links"""

    global_contexts = {
        None: lambda data, *args, **kwargs: LinkExpander.expand(data)
    }

    def __init__(self, convert_dicts: bool = False):
        """
        :param convert_dicts: Convert all untyped dicts to links
        """
        self.convert_dicts = convert_dicts

    def getter(self, get_func=None, context_aware=True, context_functions=None,
               *args, **kwargs):
        """
        Decorator for automatically expanding Link objects
        """
        context_functions = context_functions or {}

        def getter_context_unaware(self, *args, **kwargs):
            """"""
            def decorator(obj, *args, **kwargs):
                """"""
                return get_func(obj)
            return decorator

        def getter_context_aware(self, *args, **kwargs):
            """"""
            def decorator(obj, *args, **kwargs):
                """"""
                # merges globally recognized functions with decorator-specific
                # functions, overriding global with instance-specific
                funcs = {**self.global_contexts, **context_functions}
                funcs.get(obj.__context__)(*args, **kwargs)
            return decorator

        return getter_context_aware if context_aware else getter_context_unaware

    def setter(self, set_prop, *args, **kwargs):
        """
        Decorator that allows the setter of a JsonProperty object to convert
        various data types into Link objects as a default
        """
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
    @LinkManager().setter
    def attachment(self, val):
        Attachment.attachment.fset(self, val)

    @PropertyContext.getter(fns={'process': lambda obj: 'test'})
    @AttributedTo.attributedTo.getter
    def attributedTo(self):
        return AttributedTo.attributedTo.fget(self)

    @AttributedTo.attributedTo.setter
    @LinkManager().setter
    def attributedTo(self, val):
        AttributedTo.attributedTo.fset(self, val)

    @Audience.audience.setter
    @LinkManager().setter
    def audience(self, val):
        Audience.audience.fset(self, val)

    @To.to.setter
    @LinkManager().setter
    def to(self, val):
        To.to.fset(self, val)

    @Bcc.bcc.setter
    @LinkManager().setter
    def bcc(self, value):
        Bcc.bcc.fset(self, value)

    @Bto.bto.setter
    @LinkManager().setter
    def bto(self, value):
        Bto.bto.fset(self, value)

    @Cc.cc.setter
    @LinkManager().setter
    def cc(self, value):
        Cc.cc.fset(self, value)

    @Context.context.setter
    @LinkManager().setter
    def context(self, val):
        Context.context.fset(self, val)

    @Generator.generator.setter
    @LinkManager().setter
    def generator(self, val):
        Generator.generator.fset(self, val)

    @Icon.icon.setter
    @LinkManager().setter
    def icon(self, val):
        Icon.icon.fset(self, val)

    @Image.image.setter
    @LinkManager().setter
    def image(self, val):
        Image.image.fset(self, val)

    @InReplyTo.inReplyTo.setter
    @LinkManager().setter
    def inReplyTo(self, val):
        InReplyTo.inReplyTo.fset(self, val)

    @Location.location.setter
    @LinkManager().setter
    def location(self, val):
        Location.location.fset(self, val)

    @Preview.preview.setter
    @LinkManager().setter
    def preview(self, val):
        Preview.preview.fset(self, val)

    @Tag.tag.setter
    @LinkManager(convert_dicts=True).setter
    def tag(self, val):
        Tag.tag.fset(self, val)

    @Url.url.setter
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

    @Preview.preview.setter
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

    @Actor.actor.getter
    def actor(self):
        Actor.actor.fget(self)

    @Actor.actor.setter
    @LinkManager().setter
    def actor(self, val):
        Actor.actor.fset(self, val)

    @ObjectProp.object.setter
    @LinkManager().setter
    def object(self, val):
        ObjectProp.object.fset(self, val)

    @Instrument.instrument.setter
    @LinkManager().setter
    def instrument(self, val):
        Instrument.instrument.fset(self, val)

    @Origin.origin.setter
    @LinkManager().setter
    def origin(self, val):
        Origin.origin.fset(self, val)

    @Result.result.setter
    @LinkManager().setter
    def result(self, val):
        Result.result.fset(self, val)

    @Target.target.setter
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

    @Current.current.setter
    @LinkManager().setter
    def current(self, val):
        Current.current.fset(self, val)

    @Items.items.setter
    @LinkManager().setter
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

    @First.first.setter
    @LinkManager().setter
    def first(self, val):
        First.first.fset(self, val)

    @Last.last.setter
    @LinkManager().setter
    def last(self, val):
        Last.last.fset(self, val)

    @Next.next.setter
    @LinkManager().setter
    def next(self, val):
        Next.next.fset(self, val)

    @PartOf.partOf.setter
    @LinkManager().setter
    def partOf(self, val):
        PartOf.partOf.fset(self, val)

    @Prev.prev.setter
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

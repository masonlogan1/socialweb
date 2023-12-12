"""
The Activity Vocabulary Core Types provide the basis for the rest of the
vocabulary.
"""
__ref__ = 'https://www.w3.org/TR/activitystreams-vocabulary/#types'

from activitystreams.models import OrderedCollectionModel, \
    OrderedCollectionPageModel, CollectionModel, IntransitiveActivityModel, \
    ActivityModel, LinkModel, ObjectModel, CollectionPageModel


class Object(ObjectModel):
    """
    Describes an object of any kind. The Object type serves as the base type
    for most of the other kinds of objects defined in the Activity
    Vocabulary, including other Core types such as Activity,
    IntransitiveActivity, Collection and OrderedCollection.
    """


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


class Activity(Object, ActivityModel):
    """
    An Activity is a subtype of Object that describes some form of action
    that may happen, is currently happening, or has already happened. The
    Activity type itself serves as an abstract base type for all types of
    activities. It is important to note that the Activity type itself does
    not carry any specific semantics about the kind of action being taken.
    """


class IntransitiveActivity(Activity, IntransitiveActivityModel):
    """
    Instances of IntransitiveActivity are a subtype of Activity representing
    intransitive actions (actions that do not require an object to make sense).
    The object property is therefore inappropriate for these activities.
    """


class Collection(Object, CollectionModel):
    """
    A Collection is a subtype of Object that represents ordered or unordered
    sets of Object or Link instances.

    Refer to the Activity Streams 2.0 Core specification for a complete
    description of the Collection type.
    """


class OrderedCollection(Collection, OrderedCollectionModel):
    """
    A subtype of Collection in which members of the logical collection are
    assumed to always be strictly ordered.
    """


class CollectionPage(Collection, CollectionPageModel):
    """
    Used to represent distinct subsets of items from a Collection. Refer to the
    Activity Streams 2.0 Core for a complete description of the CollectionPage
    object.
    """


class OrderedCollectionPage(OrderedCollection, CollectionPage,
                            OrderedCollectionPageModel):
    """
    Used to represent ordered subsets of items from an OrderedCollection.
    Refer to the Activity Streams 2.0 Core for a complete description of the
    OrderedCollectionPage object.
    """

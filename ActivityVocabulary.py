"""
AUTHOR:     Mason Logan <PythonActivityStreams@masonlogan.com>
CREATED:    July 16, 2023
UPDATED:    July 16, 2023
Implements objects for working with ActivityStreams. Objects are intended to
be used as an alternative to working directly with JSON-LD data.
"""
# Yes, the docstrings for each class are directly taken from the ActivityStreams
# Vocabulary document. This whole module is intentionally barely one level of
# abstraction from the spec
from validators import url

CONTEXT = "https://www.w3.org/ns/activitystreams"


class ActivityStreamsObject:
    """
    Base class for providing optional validation on all ActivityStreams fields.
    All fields mentioned in the ActivityVocabulary spec are inspected for
    type-correctness if strictness is enabled; will raise a ValueError for
    any incorrectly formatted fields
    """
    # NOTE: NOT CURRENTLY IMPLEMENTED! THIS IS PLANNING FOR FUTURE WORK!
    # THIS CLASS ISN'T USED BY ANYTHING AT ALL RIGHT NOW!
    # The eventual goal is to give all descendent classes a validator for
    # incoming field data; all fields have their types specified by the spec
    # so we know what basic checks to include
    __strict = False

    @classmethod
    def strict_init(cls):
        # sounds like an old british man. "bloody hell, bit strict innit?"
        cls.__strict = True

    @classmethod
    def nonstrict_init(cls):
        cls.__strict = False


## ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//
##
##  The Base Types
##      The six foundational classes that all other ActivityVocabulary
##      objects are built from
##
##  ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//


class Object:
    """
    Describes an object of any kind. The Object type serves as the base type
    for most of the other kinds of objects defined in the Activity
    Vocabulary, including other Core types such as Activity,
    IntransitiveActivity, Collection and OrderedCollection.
    """

    def __init__(self, id, attachment=None, attributed_to=None, audience=None,
                 content=None, context=None, name=None, end_time=None,
                 generator=None, icon=None, image=None, in_reply_to=None,
                 location=None, preview=None, published=None, replies=None,
                 start_time=None, summary=None, tag=None, updated=None,
                 url=None, to=None, bto=None, cc=None, bcc=None,
                 media_type=None, duration=None):
        self.context = CONTEXT
        self.id = id
        self.attachment = attachment
        self.attributed_to = attributed_to
        self.audience = audience
        self.content = content
        self.context = context
        self.name = name
        self.end_time = end_time
        self.generator = generator
        self.icon = icon
        self.image = image
        self.in_reply_to = in_reply_to
        self.location = location
        self.preview = preview
        self.published = published
        self.replies = replies
        self.start_time = start_time
        self.summary = summary
        self.tag = tag
        self.updated = updated
        self.url = url
        self.to = to
        self.bto = bto
        self.cc = cc
        self.bcc = bcc
        self.media_type = media_type
        self.duration = duration


class Link:
    """A Link is an indirect, qualified reference to a resource identified by a
    URL. The fundamental model for links is established by [RFC5988]. Many
    of the properties defined by the Activity Vocabulary allow values that are
    either instances of Object or Link. When a Link is used, it establishes a
    qualified relation connecting the subject (the containing object) to the
    resource identified by the href. Properties of the Link are properties of
    the reference as opposed to properties of the resource"""

    def __init__(self, href=None, rel=None, media_type=None, name=None,
                 hreflang=None, height=None, width=None, preview=None):
        self.href = href
        self.rel = rel
        self.media_type = media_type
        self.name = name
        self.hreflang = hreflang
        self.height = height
        self.width = width
        self.preview = preview


class Activity(Object):
    """
    An Activity is a subtype of Object that describes some form of action
    that may happen, is currently happening, or has already happened. The
    Activity type itself serves as an abstract base type for all types of
    activities. It is important to note that the Activity type itself does
    not carry any specific semantics about the kind of action being taken.
    :arg actor:
    """

    def __init__(self, id, actor=None, object=None, target=None,
                 result=None, origin=None, instrument=None, **kwargs):
        super().__init__(id, **kwargs)
        self.actor = actor
        self.object = object
        self.target = target
        self.result = result
        self.origin = origin
        self.instrument = instrument


class IntransitiveActivity(Activity):
    """
    Instances of IntransitiveActivity are a subtype of Activity representing
    intransitive actions (actions that do not require an object to make sense).
    The object property is therefore inappropriate for these activities.
    """

    def __init__(self, id, **kwargs):
        super().__init__(id, object=None, **kwargs)


class Collection(Object):
    """
    A Collection is a subtype of Object that represents ordered or unordered
    sets of Object or Link instances.

    Refer to the Activity Streams 2.0 Core specification for a complete
    description of the Collection type.
    """

    def __init__(self, id, total_items=None, current=None, first=None,
                 last=None, items=None, **kwargs):
        super().__init__(id, **kwargs)
        self.total_items = total_items
        self.current = current
        self.first = first
        self.last = last
        self.items = items


class OrderedCollection(Collection):
    """
    A subtype of Collection in which members of the logical collection are
    assumed to always be strictly ordered.
    """

    def __init__(self, id, **kwargs):
        super().__init__(id, **kwargs)


class CollectionPage(Collection):
    """
    Used to represent distinct subsets of items from a Collection. Refer to the
    Activity Streams 2.0 Core for a complete description of the CollectionPage
    object.
    """

    def __init__(self, id, part_of=None, next=None, prev=None, **kwargs):
        super().__init__(id, **kwargs)
        self.part_of = part_of
        self.next = next
        self.prev = prev


class OrderedCollectionPage(OrderedCollection, CollectionPage):
    """
    Used to represent ordered subsets of items from an OrderedCollection.
    Refer to the Activity Streams 2.0 Core for a complete description of the
    OrderedCollectionPage object.
    """

    def __init__(self, id, start_index, **kwargs):
        OrderedCollection.__init__(id, **kwargs)
        CollectionPage.__init__(id, **kwargs)
        self.start_index = start_index


# ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//
#
#   The Activity Types
#       These classes describe things an Actor might do with Objects
#
#  ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//
class Accept(Activity):
    """
    Indicates that the actor accepts the object. The target property can be
    used in certain circumstances to indicate the context into which the
    object has been accepted.
    """


class TentativeAccept(Accept):
    """
    A specialization of Accept indicating that the acceptance is tentative.
    """


class Add(Activity):
    """
    Indicates that the actor has added the object to the target. If the
    target property is not explicitly specified, the target would need to be
    determined implicitly by context. The origin can be used to identify the
    context from which the object originated.
    """


class Arrive(IntransitiveActivity):
    """
    An IntransitiveActivity that indicates that the actor has arrived at the
    location. The origin can be used to identify the context from which the
    actor originated. The target typically has no defined meaning.
    """


class Create(Activity):
    """
    Indicates that the actor has created the object.
    """


class Delete(Activity):
    """
    Indicates that the actor has deleted the object. If specified, the origin
    indicates the context from which the object was deleted.
    """


class Follow(Activity):
    """
    Indicates that the actor is "following" the object. Following is defined
    in the sense typically used within Social systems in which the actor is
    interested in any activity performed by or on the object. The target and
    origin typically have no defined meaning.
    """


class Ignore(Activity):
    """
    Indicates that the actor is ignoring the object. The target and origin
    typically have no defined meaning.
    """


class Join(Activity):
    """
    Indicates that the actor has joined the object. The target and origin
    typically have no defined meaning.
    """


class Leave(Activity):
    """
    Indicates that the actor has left the object. The target and origin
    typically have no meaning.
    """


class Like(Activity):
    """
    Indicates that the actor likes, recommends or endorses the object. The
    target and origin typically have no defined meaning.
    """


class Offer(Activity):
    """
    Indicates that the actor is offering the object. If specified, the target
    indicates the entity to which the object is being offered.
    """

class Invite(Offer):
    """
    A specialization of Offer in which the actor is extending an invitation
    for the object to the target.
    """


class Reject(Activity):
    """
    Indicates that the actor is rejecting the object. The target and origin
    typically have no defined meaning.
    """


class TentativeReject(Reject):
    """
    A specialization of Reject in which the rejection is considered tentative.
    """


class Remove(Activity):
    """
    Indicates that the actor is removing the object. If specified,
    the origin indicates the context from which the object is being removed.
    """


class Undo(Activity):
    """
    Indicates that the actor is undoing the object. In most cases, the object
    will be an Activity describing some previously performed action (for
    instance, a person may have previously "liked" an article but,
    for whatever reason, might choose to undo that like at some later point
    in time).

    The target and origin typically have no defined meaning.
    """


class Update(Activity):
    """
    Indicates that the actor has updated the object. Note, however, that this
    vocabulary does not define a mechanism for describing the actual set of
    modifications made to object.

    The target and origin typically have no defined meaning.
    """


class View(Activity):
    """
    Indicates that the actor has viewed the object.
    """


class Listen(Activity):
    """
    Indicates that the actor has listened to the object.
    """


class Read(Activity):
    """
    Indicates that the actor has read the object.
    """


class Move(Activity):
    """
    Indicates that the actor has moved object from origin to target. If the
    origin or target are not specified, either can be determined by context.
    """


class Travel(IntransitiveActivity):
    """
    Indicates that the actor is traveling to target from origin. Travel is an
    IntransitiveObject whose actor specifies the direct object. If the target
    or origin are not specified, either can be determined by context.
    """


class Announce(Activity):
    """
    Indicates that the actor is calling the target's attention the object.

    The origin typically has no defined meaning.
    """


class Block(Ignore):
    """
    Indicates that the actor is blocking the object. Blocking is a stronger
    form of Ignore. The typical use is to support social systems that allow
    one user to block activities or content of other users. The target and
    origin typically have no defined meaning.
    """


class Flag(Activity):
    """
    Indicates that the actor is "flagging" the object. Flagging is defined in
    the sense common to many social platforms as reporting content as being
    inappropriate for any number of reasons.
    """


class Dislike(Activity):
    """
    Indicates that the actor dislikes the object.
    """


class Question(IntransitiveActivity):
    """
    Represents a question being asked. Question objects are an extension of
    IntransitiveActivity. That is, the Question object is an Activity,
    but the direct object is the question itself and therefore it would not
    contain an object property.

    Either of the anyOf and oneOf properties MAY be used to express possible
    answers, but a Question object MUST NOT have both properties.
    """
    def __init__(self, id, one_of=None, any_of=None, closed=None, **kwargs):
        super().__init__(id, **kwargs)
        self.one_of = one_of
        self.any_of = any_of
        self.closed = closed


# ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//
#
#   The Actor Types
#       These classes describe the types of users and automated
#       processes that might be performing Actions on Objects
#
#  ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//
class Application(Object):
    """
    Describes a software application.
    """


class Group(Object):
    """
    Represents a formal or informal collective of Actors.
    """


class Organization(Object):
    """
    Represents an organization.
    """


class Person(Object):
    """
    Represents an individual person.
    """


class Service(Object):
    """
    Represents a service of any kind.
    """


# ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//
#
#   The Object/Link Types
#       These classes describe the types of Objects an Actor might
#       be performing some kind of Action on, and the conceptual
#       Links that bind Objects, Actors, and their interactions together
#
#  ==//==//==//==// ==//==//==//==// ==//==//==//==// ==//==//==//==//

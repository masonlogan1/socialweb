from models.models import ObjectModel, LinkModel, ActivityModel, \
    IntransitiveActivityModel, CollectionModel, OrderedCollectionModel, \
    CollectionPageModel, OrderedCollectionPageModel, AcceptModel, \
    TentativeAcceptModel, AddModel, ArriveModel, CreateModel, DeleteModel, \
    FollowModel, IgnoreModel, JoinModel, LeaveModel, LikeModel, OfferModel, \
    InviteModel, RejectModel, TentativeRejectModel, RemoveModel, UndoModel, \
    UpdateModel, ViewModel, ListenModel, ReadModel, MoveModel, TravelModel, \
    AnnounceModel, BlockModel, FlagModel, DislikeModel, QuestionModel, \
    ApplicationModel, GroupModel, OrganizationModel, PersonModel, \
    ServiceModel, RelationshipModel, ArticleModel, DocumentModel, AudioModel, \
    ImageModel, VideoModel, NoteModel, PageModel, EventModel, PlaceModel, \
    ProfileModel, TombstoneModel, MentionModel


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# CORE TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#types
#
#   These classes serve as the basis for all other classes
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

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
    :arg actor:
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


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# ACTIVITY TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#activity-types
#
#   These classes serve as the activities that actors perform
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class Accept(Activity, AcceptModel):
    """
    Indicates that the actor accepts the object. The target property can be
    used in certain circumstances to indicate the context into which the
    object has been accepted.
    """


class TentativeAccept(Accept, TentativeAcceptModel):
    """
    A specialization of Accept indicating that the acceptance is tentative.
    """


class Add(Activity, AddModel):
    """
    Indicates that the actor has added the object to the target. If the
    target property is not explicitly specified, the target would need to be
    determined implicitly by context. The origin can be used to identify the
    context from which the object originated.
    """


class Arrive(IntransitiveActivity, ArriveModel):
    """
    An IntransitiveActivity that indicates that the actor has arrived at the
    location. The origin can be used to identify the context from which the
    actor originated. The target typically has no defined meaning.
    """


class Create(Activity, CreateModel):
    """
    Indicates that the actor has created the object.
    """


class Delete(Activity, DeleteModel):
    """
    Indicates that the actor has deleted the object. If specified, the origin
    indicates the context from which the object was deleted.
    """


class Follow(Activity, FollowModel):
    """
    Indicates that the actor is "following" the object. Following is defined
    in the sense typically used within Social systems in which the actor is
    interested in any activity performed by or on the object. The target and
    origin typically have no defined meaning.
    """


class Ignore(Activity, IgnoreModel):
    """
    Indicates that the actor is ignoring the object. The target and origin
    typically have no defined meaning.
    """


class Join(Activity, JoinModel):
    """
    Indicates that the actor has joined the object. The target and origin
    typically have no defined meaning.
    """


class Leave(Activity, LeaveModel):
    """
    Indicates that the actor has left the object. The target and origin
    typically have no meaning.
    """


class Like(Activity, LikeModel):
    """
    Indicates that the actor likes, recommends or endorses the object. The
    target and origin typically have no defined meaning.
    """


class Offer(Activity, OfferModel):
    """
    Indicates that the actor is offering the object. If specified, the target
    indicates the entity to which the object is being offered.
    """


class Invite(Offer, InviteModel):
    """
    A specialization of Offer in which the actor is extending an invitation
    for the object to the target.
    """


class Reject(Activity, RejectModel):
    """
    Indicates that the actor is rejecting the object. The target and origin
    typically have no defined meaning.
    """


class TentativeReject(Reject, TentativeRejectModel):
    """
    A specialization of Reject in which the rejection is considered tentative.
    """


class Remove(Activity, RemoveModel):
    """
    Indicates that the actor is removing the object. If specified,
    the origin indicates the context from which the object is being removed.
    """


class Undo(Activity, UndoModel):
    """
    Indicates that the actor is undoing the object. In most cases, the object
    will be an Activity describing some previously performed action (for
    instance, a person may have previously "liked" an article but,
    for whatever reason, might choose to undo that like at some later point
    in time).

    The target and origin typically have no defined meaning.
    """


class Update(Activity, UpdateModel):
    """
    Indicates that the actor has updated the object. Note, however, that this
    vocabulary does not define a mechanism for describing the actual set of
    modifications made to object.

    The target and origin typically have no defined meaning.
    """


class View(Activity, ViewModel):
    """
    Indicates that the actor has viewed the object.
    """


class Listen(Activity, ListenModel):
    """
    Indicates that the actor has listened to the object.
    """


class Read(Activity, ReadModel):
    """
    Indicates that the actor has read the object.
    """


class Move(Activity, MoveModel):
    """
    Indicates that the actor has moved object from origin to target. If the
    origin or target are not specified, either can be determined by context.
    """


class Travel(IntransitiveActivity, TravelModel):
    """
    Indicates that the actor is traveling to target from origin. Travel is an
    IntransitiveObject whose actor specifies the direct object. If the target
    or origin are not specified, either can be determined by context.
    """


class Announce(Activity, AnnounceModel):
    """
    Indicates that the actor is calling the target's attention the object.

    The origin typically has no defined meaning.
    """


class Block(Ignore, BlockModel):
    """
    Indicates that the actor is blocking the object. Blocking is a stronger
    form of Ignore. The typical use is to support social systems that allow
    one user to block activities or content of other users. The target and
    origin typically have no defined meaning.
    """


class Flag(Activity, FlagModel):
    """
    Indicates that the actor is "flagging" the object. Flagging is defined in
    the sense common to many social platforms as reporting content as being
    inappropriate for any number of reasons.
    """


class Dislike(Activity, DislikeModel):
    """
    Indicates that the actor dislikes the object.
    """


class Question(IntransitiveActivity, QuestionModel):
    """
    Represents a question being asked. Question objects are an extension of
    IntransitiveActivity. That is, the Question object is an Activity,
    but the direct object is the question itself, therefore it would not
    contain an object property.

    Either of the anyOf and oneOf properties MAY be used to express possible
    answers, but a Question object MUST NOT have both properties.
    """


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# ACTOR TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#actor-types
#
#   These classes serve as the actors who interact with the objects on a site
#   and perform activities
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class Application(Object, ApplicationModel):
    """
    Describes a software application.
    """


class Group(Object, GroupModel):
    """
    Represents a formal or informal collective of Actors.
    """


class Organization(Object, OrganizationModel):
    """
    Represents an organization.
    """


class Person(Object, PersonModel):
    """
    Represents an individual person.
    """


class Service(Object, ServiceModel):
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

class Relationship(Object, RelationshipModel):
    """
    Describes a relationship between two individuals. The subject and object
    properties are used to identify the connected individuals.
    """


class Article(Object, ArticleModel):
    """
    Represents any kind of multi-paragraph written work.
    """


class Document(Object, DocumentModel):
    """
    Represents a document of any kind.
    """


class Audio(Object, AudioModel):
    """
    Represents an audio document of any kind.
    """


class Image(Document, ImageModel):
    """
    An image document of any kind
    """


class Video(Document, VideoModel):
    """
    Represents a video document of any kind.
    """


class Note(Object, NoteModel):
    """
    Represents a short written work typically less than a single paragraph in
    length.
    """


class Page(Document, PageModel):
    """
    Represents a Web Page.
    """


class Event(Object, EventModel):
    """
    Represents any kind of event.
    """


class Place(Object, PlaceModel):
    """
    Represents a logical or physical location. See 5.3 Representing Places
    for additional information.
    """


class Profile(Object, ProfileModel):
    """
    A Profile is a content object that describes another Object, typically
    used to describe Actor Type objects. The describes property is used to
    reference the object being described by the profile.
    """


class Tombstone(Object, TombstoneModel):
    """
    A Tombstone represents a content object that has been deleted. It can be
    used in Collections to signify that there used to be an object at this
    position, but it has been deleted.
    """


class Mention(Link, MentionModel):
    """
    A specialized Link that represents an @mention.
    """
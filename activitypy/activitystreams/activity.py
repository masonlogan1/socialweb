"""
All Activity Types inherit the properties of the base Activity type. Some
specific Activity Types are subtypes or specializations of more generalized
Activity Types (for instance, the Invite Activity Type is a more specific form
of the Offer Activity Type).
"""
__ref__ = "https://www.w3.org/TR/activitystreams-vocabulary/#activity-types"

from activitypy.activitystreams.core import Link, Activity, \
    IntransitiveActivity, Linkify
from activitypy.activitystreams.models import AcceptModel, TentativeAcceptModel, \
    AddModel, CreateModel, ArriveModel, DeleteModel, FollowModel, IgnoreModel, \
    JoinModel, LeaveModel, LikeModel, OfferModel, InviteModel, RejectModel, \
    TentativeRejectModel, RemoveModel, UndoModel, UpdateModel, ViewModel, \
    ListenModel, ReadModel, MoveModel, TravelModel, AnnounceModel, BlockModel, \
    FlagModel, DislikeModel, QuestionModel
from activitypy.activitystreams.models.properties import OneOf, \
    AnyOf, Closed
from activitypy.activitystreams.utils import validate_url


class Accept(Activity, AcceptModel):
    """
    Indicates that the actor accepts the object. The target property can be
    used in certain circumstances to indicate the context into which the
    object has been accepted.
    """
    type = "Accept"


class TentativeAccept(Accept, TentativeAcceptModel):
    """
    A specialization of Accept indicating that the acceptance is tentative.
    """
    type = "TentativeAccept"


class Add(Activity, AddModel):
    """
    Indicates that the actor has added the object to the target. If the
    target property is not explicitly specified, the target would need to be
    determined implicitly by context. The origin can be used to identify the
    context from which the object originated.
    """
    type = "Add"


class Arrive(IntransitiveActivity, ArriveModel):
    """
    An IntransitiveActivity that indicates that the actor has arrived at the
    location. The origin can be used to identify the context from which the
    actor originated. The target typically has no defined meaning.
    """
    type = "Arrive"


class Create(Activity, CreateModel):
    """
    Indicates that the actor has created the object.
    """
    type = "Create"


class Delete(Activity, DeleteModel):
    """
    Indicates that the actor has deleted the object. If specified, the origin
    indicates the context from which the object was deleted.
    """
    type = "Delete"


class Follow(Activity, FollowModel):
    """
    Indicates that the actor is "following" the object. Following is defined
    in the sense typically used within Social systems in which the actor is
    interested in any activity performed by or on the object. The target and
    origin typically have no defined meaning.
    """
    type = "Follow"


class Ignore(Activity, IgnoreModel):
    """
    Indicates that the actor is ignoring the object. The target and origin
    typically have no defined meaning.
    """
    type = "Ignore"


class Join(Activity, JoinModel):
    """
    Indicates that the actor has joined the object. The target and origin
    typically have no defined meaning.
    """
    type = "Join"


class Leave(Activity, LeaveModel):
    """
    Indicates that the actor has left the object. The target and origin
    typically have no meaning.
    """
    type = "Leave"


class Like(Activity, LikeModel):
    """
    Indicates that the actor likes, recommends or endorses the object. The
    target and origin typically have no defined meaning.
    """
    type = "Like"


class Offer(Activity, OfferModel):
    """
    Indicates that the actor is offering the object. If specified, the target
    indicates the entity to which the object is being offered.
    """
    type = "Offer"


class Invite(Offer, InviteModel):
    """
    A specialization of Offer in which the actor is extending an invitation
    for the object to the target.
    """
    type = "Invite"


class Reject(Activity, RejectModel):
    """
    Indicates that the actor is rejecting the object. The target and origin
    typically have no defined meaning.
    """
    type = "Reject"


class TentativeReject(Reject, TentativeRejectModel):
    """
    A specialization of Reject in which the rejection is considered tentative.
    """
    type = "TentativeReject"


class Remove(Activity, RemoveModel):
    """
    Indicates that the actor is removing the object. If specified,
    the origin indicates the context from which the object is being removed.
    """
    type = "Remove"


class Undo(Activity, UndoModel):
    """
    Indicates that the actor is undoing the object. In most cases, the object
    will be an Activity describing some previously performed action (for
    instance, a person may have previously "liked" an article but,
    for whatever reason, might choose to undo that like at some later point
    in time).

    The target and origin typically have no defined meaning.
    """
    type = "Undo"


class Update(Activity, UpdateModel):
    """
    Indicates that the actor has updated the object. Note, however, that this
    vocabulary does not define a mechanism for describing the actual set of
    modifications made to object.

    The target and origin typically have no defined meaning.
    """
    type = "Update"


class View(Activity, ViewModel):
    """
    Indicates that the actor has viewed the object.
    """
    type = "View"


class Listen(Activity, ListenModel):
    """
    Indicates that the actor has listened to the object.
    """
    type = "Listen"


class Read(Activity, ReadModel):
    """
    Indicates that the actor has read the object.
    """
    type = "Read"


class Move(Activity, MoveModel):
    """
    Indicates that the actor has moved object from origin to target. If the
    origin or target are not specified, either can be determined by context.
    """
    type = "Move"


class Travel(IntransitiveActivity, TravelModel):
    """
    Indicates that the actor is traveling to target from origin. Travel is an
    IntransitiveObject whose actor specifies the direct object. If the target
    or origin are not specified, either can be determined by context.
    """
    type = "Travel"


class Announce(Activity, AnnounceModel):
    """
    Indicates that the actor is calling the target's attention the object.

    The origin typically has no defined meaning.
    """
    type = "Announce"


class Block(Ignore, BlockModel):
    """
    Indicates that the actor is blocking the object. Blocking is a stronger
    form of Ignore. The typical use is to support social systems that allow
    one user to block activities or content of other users. The target and
    origin typically have no defined meaning.
    """
    type = "Block"


class Flag(Activity, FlagModel):
    """
    Indicates that the actor is "flagging" the object. Flagging is defined in
    the sense common to many social platforms as reporting content as being
    inappropriate for any number of reasons.
    """
    type = "Flag"


class Dislike(Activity, DislikeModel):
    """
    Indicates that the actor dislikes the object.
    """
    type = "Dislike"


class Question(IntransitiveActivity, QuestionModel):
    """
    Represents a question being asked. Question objects are an extension of
    IntransitiveActivity. That is, the Question object is an Activity,
    but the direct object is the question itself, therefore it would not
    contain an object property.

    Either of the anyOf and oneOf properties MAY be used to express possible
    answers, but a Question object MUST NOT have both properties.
    """
    type = "Question"

    @OneOf.oneOf.setter
    @Linkify()
    def oneOf(self, val):
        OneOf.oneOf.fset(self, val)

    @AnyOf.anyOf.setter
    @Linkify()
    def anyOf(self, val):
        AnyOf.anyOf.fset(self, val)

    @Closed.closed.setter
    @Linkify()
    def closed(self, val):
        Closed.closed.fset(self, val)

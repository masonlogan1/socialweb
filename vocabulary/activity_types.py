"""
AUTHOR:     Mason Logan <PythonActivityStreams@masonlogan.com>
CREATED:    November 16, 2023
UPDATED:    November 16, 2023
Implements core objects for working with ActivityStreams. Objects are intended
to be used as an alternative to working directly with JSON-LD data.
"""
# Yes, the docstrings for each class are directly taken from the ActivityStreams
# Vocabulary document. This whole module is intentionally barely one level of
# abstraction from the spec
from vocabulary import Activity, IntransitiveActivity


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

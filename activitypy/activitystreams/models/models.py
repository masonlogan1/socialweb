"""
Provides data structures for ActivityStreams vocabulary objects. These objects
are not a full implementation, just an outline that ensures attributes are
handled correctly.
"""
# Yes, the docstrings for each class are directly taken from the ActivityStreams
# Vocabulary document. This whole module is intentionally barely one level of
# abstraction from the spec
import logging
from collections.abc import Sized

from activitypy.jsonld import ApplicationActivityJson, register_property
from activitypy.activitystreams import properties

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SECURE_URLS_ONLY = False


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# CORE TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#types
#
#   These classes serve as the basis for all other classes
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

# this insane cluster of inheritance might look bad, but it's actually a lot
# easier to manage the properties if we make them their own classes
class ObjectModel(ApplicationActivityJson):
    """
    Describes an object of any kind. The Object type serves as the base type
    for most of the other kinds of objects defined in the Activity
    Vocabulary, including other Core types such as Activity,
    IntransitiveActivity, Collection and OrderedCollection.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None,
                 acontext='https://www.w3.org/ns/activitystreams',
                 **kwargs):
        ApplicationActivityJson.__init__(self, acontext=acontext)
        self.id = id
        self.type = type or self.type
        self.attachment = attachment
        self.attributedTo = attributedTo
        self.audience = audience
        self.content = content
        self.context = context
        self.name = name
        self.endTime = endTime
        self.generator = generator
        self.icon = icon
        self.image = image
        self.inReplyTo = inReplyTo
        self.location = location
        self.preview = preview
        self.published = published
        self.replies = replies
        self.startTime = startTime
        self.summary = summary
        self.tag = tag
        self.updated = updated
        self.url = url
        self.to = to
        self.bto = bto
        self.cc = cc
        self.bcc = bcc
        self.mediaType = mediaType
        self.duration = duration


register_property(properties.Id, ObjectModel)
register_property(properties.Type, ObjectModel)
register_property(properties.Attachment, ObjectModel)
register_property(properties.AttributedTo, ObjectModel)
register_property(properties.Audience, ObjectModel)
register_property(properties.Content, ObjectModel)
register_property(properties.Context, ObjectModel)
register_property(properties.Name, ObjectModel)
register_property(properties.EndTime, ObjectModel)
register_property(properties.Generator, ObjectModel)
register_property(properties.Icon, ObjectModel)
register_property(properties.Image, ObjectModel)
register_property(properties.InReplyTo, ObjectModel)
register_property(properties.Location, ObjectModel)
register_property(properties.Preview, ObjectModel)
register_property(properties.Published, ObjectModel)
register_property(properties.Replies, ObjectModel)
register_property(properties.StartTime, ObjectModel)
register_property(properties.Summary, ObjectModel)
register_property(properties.Tag, ObjectModel)
register_property(properties.Updated, ObjectModel)
register_property(properties.Url, ObjectModel)
register_property(properties.To, ObjectModel)
register_property(properties.Bto, ObjectModel)
register_property(properties.Cc, ObjectModel)
register_property(properties.Bcc, ObjectModel)
register_property(properties.MediaType, ObjectModel)
register_property(properties.Duration, ObjectModel)


class LinkModel(ApplicationActivityJson):
    """
    A Link is an indirect, qualified reference to a resource identified by a
    URL. The fundamental model for links is established by [RFC5988]. Many
    of the properties defined by the Activity Vocabulary allow values that are
    either instances of Object or Link. When a Link is used, it establishes a
    qualified relation connecting the subject (the containing object) to the
    resource identified by the href. Properties of the Link are properties of
    the reference as opposed to properties of the resource
    """

    def __init__(self, href=None, rel=None, mediaType=None, name=None,
                 hreflang=None, height=None, width=None, preview=None,
                 context=None, type=None,
                 acontext='https://www.w3.org/ns/activitystreams'):
        # grants the ability to access all @property objects associated with the
        # model via __properties__ on instantiated objects and
        # __get_properties__ on classes
        ApplicationActivityJson.__init__(self, acontext=acontext)
        self.href = href
        self.rel = rel
        self.mediaType = mediaType
        self.name = name
        self.hreflang = hreflang
        self.height = height
        self.width = width
        self.preview = preview
        self.context = context
        self.type = type or self.type


register_property(properties.Href, LinkModel)
register_property(properties.Rel, LinkModel)
register_property(properties.MediaType, LinkModel)
register_property(properties.Name, LinkModel)
register_property(properties.HrefLang, LinkModel)
register_property(properties.Height, LinkModel)
register_property(properties.Width, LinkModel)
register_property(properties.Preview, LinkModel)
register_property(properties.Context, LinkModel)
register_property(properties.Type, LinkModel)


class ActivityModel(ObjectModel):
    """
    An Activity is a subtype of Object that describes some form of action
    that may happen, is currently happening, or has already happened. The
    Activity type itself serves as an abstract base type for all types of
    activities. It is important to note that the Activity type itself does
    not carry any specific semantics about the kind of action being taken.
    :arg actor:
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, actor=None, object=None,
                 target=None, result=None, origin=None, instrument=None,
                 acontext='https://www.w3.org/ns/activitystreams', **kwargs):
        # "this looks so bad" I KNOW, but it's the only way to make all the
        # params show up in tooltips! Yes it looks bad! But it makes it easier
        # to work with!!
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType,
                         duration=duration, acontext=acontext, **kwargs)
        self.actor = actor
        self.object = object
        self.target = target
        self.result = result
        self.origin = origin
        self.instrument = instrument


register_property(properties.Actor, ActivityModel)
register_property(properties.Object, ActivityModel)
register_property(properties.Target, ActivityModel)
register_property(properties.Result, ActivityModel)
register_property(properties.Origin, ActivityModel)
register_property(properties.Instrument, ActivityModel)


class IntransitiveActivityModel(ActivityModel):
    """
    Instances of IntransitiveActivity are a subtype of Activity representing
    intransitive actions (actions that do not require an object to make sense).
    The object property is therefore inappropriate for these activities.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, actor=None, object=None,
                 target=None, result=None, origin=None, instrument=None,
                 acontext='https://www.w3.org/ns/activitystreams', **kwargs):
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType,
                         duration=duration, actor=actor, object=object,
                         target=target, result=result, origin=origin,
                         instrument=instrument, acontext=acontext, **kwargs)


class CollectionModel(ObjectModel):
    """
    A Collection is a subtype of Object that represents ordered or unordered
    sets of Object or Link instances.

    Refer to the Activity Streams 2.0 Core specification for a complete
    description of the Collection type.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, totalItems=None, current=None,
                 first=None, last=None, items=None,
                 acontext='https://www.w3.org/ns/activitystreams', **kwargs):
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType,
                         duration=duration, acontext=acontext, **kwargs)
        self.current = current
        self.first = first
        self.last = last
        # some inheritors may override this with more specific orderings,
        # they should be given precedence
        self.items = items if not hasattr(self, 'items') else self.items

        # supplied value takes priority, followed by size of items if they are
        # sizeable, defaulting to 0 if not
        self.totalItems = totalItems if totalItems else (
            0 if not isinstance(self.items, Sized) else len(self.items)
        )


register_property(properties.Current, CollectionModel)
register_property(properties.First, CollectionModel)
register_property(properties.Last, CollectionModel)
register_property(properties.Items, CollectionModel)
register_property(properties.TotalItems, CollectionModel)


class OrderedCollectionModel(CollectionModel):
    """
    A subtype of Collection in which members of the logical collection are
    assumed to always be strictly ordered.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, totalItems=None, current=None,
                 first=None, last=None, orderedItems=None, items=None,
                 acontext='https://www.w3.org/ns/activitystreams', **kwargs):
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType, items=items,
                         duration=duration, totalItems=totalItems,
                         current=current, first=first, last=last,
                         acontext=acontext, **kwargs)
        self.orderedItems = orderedItems


register_property(properties.OrderedItems, OrderedCollectionModel)


class CollectionPageModel(CollectionModel):
    """
    Used to represent distinct subsets of items from a Collection. Refer to the
    Activity Streams 2.0 Core for a complete description of the CollectionPage
    object.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, totalItems=None, current=None,
                 first=None, last=None, items=None, partOf=None, next=None,
                 prev=None, acontext='https://www.w3.org/ns/activitystreams',
                 **kwargs):
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType,
                         duration=duration, totalItems=totalItems,
                         current=current, first=first, last=last, items=items,
                         acontext=acontext, **kwargs)
        self.partOf = partOf
        self.next = next
        self.prev = prev


register_property(properties.PartOf, CollectionPageModel)
register_property(properties.Next, CollectionPageModel)
register_property(properties.Prev, CollectionPageModel)


class OrderedCollectionPageModel(OrderedCollectionModel, CollectionPageModel):
    """
    Used to represent ordered subsets of items from an OrderedCollection.
    Refer to the Activity Streams 2.0 Core for a complete description of the
    OrderedCollectionPage object.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, totalItems=None, current=None,
                 first=None, last=None, items=None, partOf=None, next=None,
                 prev=None, startIndex=None, orderedItems=None,
                 acontext='https://www.w3.org/ns/activitystreams', **kwargs):
        # OrderedCollection has no special handling in its init that
        # CollectionPage doesn't already do
        OrderedCollectionModel.__init__(self, orderedItems=orderedItems)
        CollectionPageModel.__init__(self, id=id, type=type,
                                     attachment=attachment,
                                     attributedTo=attributedTo,
                                     audience=audience,
                                     content=content, context=context,
                                     name=name,
                                     endTime=endTime, generator=generator,
                                     icon=icon,
                                     image=image, inReplyTo=inReplyTo,
                                     location=location, preview=preview,
                                     published=published, replies=replies,
                                     startTime=startTime, summary=summary,
                                     tag=tag, updated=updated, url=url, to=to,
                                     bto=bto,
                                     cc=cc, bcc=bcc, mediaType=mediaType,
                                     duration=duration, totalItems=totalItems,
                                     current=current, first=first, last=last,
                                     partOf=partOf, next=next, prev=prev,
                                     acontext=acontext)
        self.startIndex = startIndex if startIndex else 0


register_property(properties.StartIndex, OrderedCollectionPageModel)


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# ACTIVITY TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#activity-types
#
#   These classes serve as the activities that actors perform
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class AcceptModel(ActivityModel):
    """
    Indicates that the actor accepts the object. The target property can be
    used in certain circumstances to indicate the context into which the
    object has been accepted.
    """


class TentativeAcceptModel(AcceptModel):
    """
    A specialization of Accept indicating that the acceptance is tentative.
    """


class AddModel(ActivityModel):
    """
    Indicates that the actor has added the object to the target. If the
    target property is not explicitly specified, the target would need to be
    determined implicitly by context. The origin can be used to identify the
    context from which the object originated.
    """


class ArriveModel(IntransitiveActivityModel):
    """
    An IntransitiveActivity that indicates that the actor has arrived at the
    location. The origin can be used to identify the context from which the
    actor originated. The target typically has no defined meaning.
    """


class CreateModel(ActivityModel):
    """
    Indicates that the actor has created the object.
    """


class DeleteModel(ActivityModel):
    """
    Indicates that the actor has deleted the object. If specified, the origin
    indicates the context from which the object was deleted.
    """


class FollowModel(ActivityModel):
    """
    Indicates that the actor is "following" the object. Following is defined
    in the sense typically used within Social systems in which the actor is
    interested in any activity performed by or on the object. The target and
    origin typically have no defined meaning.
    """


class IgnoreModel(ActivityModel):
    """
    Indicates that the actor is ignoring the object. The target and origin
    typically have no defined meaning.
    """


class JoinModel(ActivityModel):
    """
    Indicates that the actor has joined the object. The target and origin
    typically have no defined meaning.
    """


class LeaveModel(ActivityModel):
    """
    Indicates that the actor has left the object. The target and origin
    typically have no meaning.
    """


class LikeModel(ActivityModel):
    """
    Indicates that the actor likes, recommends or endorses the object. The
    target and origin typically have no defined meaning.
    """


class OfferModel(ActivityModel):
    """
    Indicates that the actor is offering the object. If specified, the target
    indicates the entity to which the object is being offered.
    """


class InviteModel(OfferModel):
    """
    A specialization of Offer in which the actor is extending an invitation
    for the object to the target.
    """


class RejectModel(ActivityModel):
    """
    Indicates that the actor is rejecting the object. The target and origin
    typically have no defined meaning.
    """


class TentativeRejectModel(RejectModel):
    """
    A specialization of Reject in which the rejection is considered tentative.
    """


class RemoveModel(ActivityModel):
    """
    Indicates that the actor is removing the object. If specified,
    the origin indicates the context from which the object is being removed.
    """


class UndoModel(ActivityModel):
    """
    Indicates that the actor is undoing the object. In most cases, the object
    will be an Activity describing some previously performed action (for
    instance, a person may have previously "liked" an article but,
    for whatever reason, might choose to undo that like at some later point
    in time).

    The target and origin typically have no defined meaning.
    """


class UpdateModel(ActivityModel):
    """
    Indicates that the actor has updated the object. Note, however, that this
    vocabulary does not define a mechanism for describing the actual set of
    modifications made to object.

    The target and origin typically have no defined meaning.
    """


class ViewModel(ActivityModel):
    """
    Indicates that the actor has viewed the object.
    """


class ListenModel(ActivityModel):
    """
    Indicates that the actor has listened to the object.
    """


class ReadModel(ActivityModel):
    """
    Indicates that the actor has read the object.
    """


class MoveModel(ActivityModel):
    """
    Indicates that the actor has moved object from origin to target. If the
    origin or target are not specified, either can be determined by context.
    """


class TravelModel(IntransitiveActivityModel):
    """
    Indicates that the actor is traveling to target from origin. Travel is an
    IntransitiveObject whose actor specifies the direct object. If the target
    or origin are not specified, either can be determined by context.
    """


class AnnounceModel(ActivityModel):
    """
    Indicates that the actor is calling the target's attention the object.

    The origin typically has no defined meaning.
    """


class BlockModel(IgnoreModel):
    """
    Indicates that the actor is blocking the object. Blocking is a stronger
    form of Ignore. The typical use is to support social systems that allow
    one user to block activities or content of other users. The target and
    origin typically have no defined meaning.
    """


class FlagModel(ActivityModel):
    """
    Indicates that the actor is "flagging" the object. Flagging is defined in
    the sense common to many social platforms as reporting content as being
    inappropriate for any number of reasons.
    """


class DislikeModel(ActivityModel):
    """
    Indicates that the actor dislikes the object.
    """


class QuestionModel(IntransitiveActivityModel):
    """
    Represents a question being asked. Question objects are an extension of
    IntransitiveActivity. That is, the Question object is an Activity,
    but the direct object is the question itself, therefore it would not
    contain an object property.

    Either of the anyOf and oneOf properties MAY be used to express possible
    answers, but a Question object MUST NOT have both properties.
    """

    def __init__(self, id=None, type=None, attachment=None, attributedTo=None,
                 audience=None, content=None, context=None, name=None,
                 endTime=None, generator=None, icon=None, image=None,
                 inReplyTo=None, location=None, preview=None, published=None,
                 replies=None, startTime=None, summary=None, tag=None,
                 updated=None, url=None, to=None, bto=None, cc=None, bcc=None,
                 mediaType=None, duration=None, actor=None, object=None,
                 target=None, result=None, origin=None, instrument=None,
                 oneOf=None, anyOf=None, closed=None,
                 acontext='https://www.w3.org/ns/activitystreams', **kwargs):
        super().__init__(id=id, type=type, attachment=attachment,
                         attributedTo=attributedTo, audience=audience,
                         content=content, context=context, name=name,
                         endTime=endTime, generator=generator, icon=icon,
                         image=image, inReplyTo=inReplyTo,
                         location=location, preview=preview,
                         published=published, replies=replies,
                         startTime=startTime, summary=summary,
                         tag=tag, updated=updated, url=url, to=to, bto=bto,
                         cc=cc, bcc=bcc, mediaType=mediaType,
                         duration=duration, actor=actor, object=object,
                         target=target, result=result, origin=origin,
                         instrument=instrument, acontext=acontext, **kwargs)
        self.oneOf = oneOf
        self.anyOf = anyOf
        self.closed = closed


register_property(properties.OneOf, QuestionModel)
register_property(properties.AnyOf, QuestionModel)
register_property(properties.Closed, QuestionModel)


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# ACTOR TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#actor-types
#
#   These classes serve as the actors who interact with the objects on a site
#   and perform activities
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class ApplicationModel(ObjectModel):
    """
    Describes a software application.
    """


class GroupModel(ObjectModel):
    """
    Represents a formal or informal collective of Actors.
    """


class OrganizationModel(ObjectModel):
    """
    Represents an organization.
    """


class PersonModel(ObjectModel):
    """
    Represents an individual person.
    """


class ServiceModel(ObjectModel):
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

class RelationshipModel(ObjectModel):
    """
    Describes a relationship between two individuals. The subject and object
    properties are used to identify the connected individuals.
    """

    def __init__(self, id, subject=None, object=None, relationship=None,
                 **kwargs):
        super().__init__(id, **kwargs)
        self.subject = subject
        self.object = object
        self.relationship = relationship


register_property(properties.Subject, RelationshipModel)
register_property(properties.Object, RelationshipModel)
register_property(properties.Relationship, RelationshipModel)


class ArticleModel(ObjectModel):
    """
    Represents any kind of multi-paragraph written work.
    """


class DocumentModel(ObjectModel):
    """
    Represents a document of any kind.
    """


class AudioModel(DocumentModel):
    """
    Represents an audio document of any kind.
    """


class ImageModel(DocumentModel):
    """
    An image document of any kind
    """


class VideoModel(DocumentModel):
    """
    Represents a video document of any kind.
    """


class NoteModel(ObjectModel):
    """
    Represents a short written work typically less than a single paragraph in
    length.
    """


class PageModel(DocumentModel):
    """
    Represents a Web Page.
    """


class EventModel(ObjectModel):
    """
    Represents any kind of event.
    """


class PlaceModel(ObjectModel):
    """
    Represents a logical or physical location. See 5.3 Representing Places
    for additional information.
    """

    def __init__(self, id, accuracy=None, altitude=None, latitude=None,
                 longitude=None, radius=None, units=None, **kwargs):
        super().__init__(id, **kwargs)
        self.accuracy = accuracy
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.units = units


register_property(properties.Accuracy, PlaceModel)
register_property(properties.Altitude, PlaceModel)
register_property(properties.Latitude, PlaceModel)
register_property(properties.Longitude, PlaceModel)
register_property(properties.Radius, PlaceModel)
register_property(properties.Units, PlaceModel)


class ProfileModel(ObjectModel):
    """
    A Profile is a content object that describes another Object, typically
    used to describe Actor Type objects. The describes property is used to
    reference the object being described by the profile.
    """

    def __init__(self, id, describes=None, **kwargs):
        super().__init__(id, **kwargs)
        self.describes = describes


register_property(properties.Describes, ProfileModel)


class TombstoneModel(ObjectModel):
    """
    A Tombstone represents a content object that has been deleted. It can be
    used in Collections to signify that there used to be an object at this
    position, but it has been deleted.
    """

    def __init__(self, id, former_type=None, deleted=None, **kwargs):
        super().__init__(id, **kwargs)
        self.former_type = former_type
        self.deleted = deleted


register_property(properties.FormerType, TombstoneModel)
register_property(properties.Deleted, TombstoneModel)


class MentionModel(LinkModel):
    """
    A specialized Link that represents a @mention.
    """

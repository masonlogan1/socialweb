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

from jsonld import ApplicationActivityJson
from jsonld import jsonld_get
from jsonld.tools import validate_url, validate_acct_or_email

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ACTIVITYSTREAMS_NS = 'https://www.w3.org/ns/activitystreams'
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
class Object(ApplicationActivityJson):
    """
    Describes an object of any kind. The Object type serves as the base type
    for most of the other kinds of objects defined in the Activity
    Vocabulary, including other Core types such as Activity,
    IntransitiveActivity, Collection and OrderedCollection.
    """
    type = "Object"

    @classmethod
    def __get_namespace__(cls):
        # provides namespacing logic for ALL derived children
        return f'{ACTIVITYSTREAMS_NS}#{cls.type}'

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
        self.type = getattr(self, 'type', type)
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


class Link(ApplicationActivityJson):
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

    @classmethod
    def __get_namespace__(cls):
        # provides namespacing logic for ALL derived children
        return f'{ACTIVITYSTREAMS_NS}#{cls.type}'

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
        self.type = getattr(self, 'type', type)

    @staticmethod
    def expand_link(data, *args, **kwargs):
        # if LinkModel isn't registered or this isn't a Link, pass the data
        # without expanding
        if not isinstance(data, Link):
            return data

        link = data.__dict__.get('_Href__href', '')
        # if we don't have an href, we can't expand; pass the data forward
        if not link:
            return data

        try:
            resp_data = jsonld_get(link)
        except Exception as e:
            # if we hit an error, pass the data through
            logger.info(f'Encountered an error expanding url {link}' +
                        f'\n{e}')
            return data

        try:
            new_obj = ApplicationActivityJson.from_json(resp_data)
        except Exception as e:
            # if we fail to form the new object, pass the data through
            logger.exception(f'Encountered an error forming object ' +
                             f'from {link}\n{e}')
            return data
        return new_obj

    @classmethod
    def getter(cls, get_func, *args, **kwargs):
        """
        Decorator for automatically expanding Link objects
        """

        def decorator(obj):
            return cls.expand_link(get_func(obj))

        return decorator

    @classmethod
    def href_only(cls, get_func):
        """
        Decorator for getting only the href value back from a link
        :param get_func: getter function being decorated
        :return: the href of the link
        """

        def decorator(obj):
            val = get_func(obj)
            # if it's a single link, return the href
            if isinstance(val, Link):
                return val.href
            # if it's a list, return either the href or the item (if no href)
            if isinstance(val, list):
                return [item.href if isinstance(item, Link) else item
                        for item in val]
            # if we don't have a handler, just give back what we found
            return val

        return decorator

    @classmethod
    def from_str(cls, set_prop):
        """
        Decorator that allows the setter of a JsonProperty object to convert
        various data types into Link objects as a default
        """

        def create_link(v):
            # if it's a string representing an email, url, or account ref,
            # create a single link
            if (isinstance(v, str) and
                    (validate_url(v) or validate_acct_or_email(v))):
                return Link(href=v)
            if isinstance(v, dict) and v.get('href', None) and validate_url(
                    v.get('href', '')):
                return Link(**v)
            # if it's an iterable other than a string or dict, create many links
            if isinstance(v, (list, tuple, set)):
                return [create_link(item) for item in v]
            return v

        def linkify(obj, val):
            val = create_link(val)
            set_prop(obj, val)

            return set_prop

        return linkify


class Activity(Object):
    """
    An Activity is a subtype of Object that describes some form of action
    that may happen, is currently happening, or has already happened. The
    Activity type itself serves as an abstract base type for all types of
    activities. It is important to note that the Activity type itself does
    not carry any specific semantics about the kind of action being taken.
    :arg actor:
    """
    type = "Activity"

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


class IntransitiveActivity(Activity):
    """
    Instances of IntransitiveActivity are a subtype of Activity representing
    intransitive actions (actions that do not require an object to make sense).
    The object property is therefore inappropriate for these activities.
    """
    type = "IntransitiveActivity"

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


class Collection(Object):
    """
    A Collection is a subtype of Object that represents ordered or unordered
    sets of Object or Link instances.

    Refer to the Activity Streams 2.0 Core specification for a complete
    description of the Collection type.
    """
    type = "Collection"

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
        self.items = getattr(self, 'items', items)

        # supplied value takes priority, followed by size of items if they are
        # sizeable, defaulting to 0 if not
        self.totalItems = totalItems if totalItems else (
            0 if not isinstance(self.items, Sized) else len(self.items)
        )

    def __iter__(self):
        if not self.items:
            yield
        for item in self.items:
            yield item


class OrderedCollection(Collection):
    """
    A subtype of Collection in which members of the logical collection are
    assumed to always be strictly ordered.
    """
    type = "OrderedCollection"

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


class CollectionPage(Collection):
    """
    Used to represent distinct subsets of items from a Collection. Refer to the
    Activity Streams 2.0 Core for a complete description of the CollectionPage
    object.
    """
    type = "CollectionPage"

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


class OrderedCollectionPage(OrderedCollection, CollectionPage):
    """
    Used to represent ordered subsets of items from an OrderedCollection.
    Refer to the Activity Streams 2.0 Core for a complete description of the
    OrderedCollectionPage object.
    """
    type = "OrderedCollectionPage"

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
        OrderedCollection.__init__(self, orderedItems=orderedItems)
        CollectionPage.__init__(self, id=id, type=type,
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


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# ACTIVITY TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#activity-types
#
#   These classes serve as the activities that actors perform
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class Accept(Activity):
    """
    Indicates that the actor accepts the object. The target property can be
    used in certain circumstances to indicate the context into which the
    object has been accepted.
    """
    type = "Accept"


class TentativeAccept(Accept):
    """
    A specialization of Accept indicating that the acceptance is tentative.
    """
    type = "TentativeAccept"


class Add(Activity):
    """
    Indicates that the actor has added the object to the target. If the
    target property is not explicitly specified, the target would need to be
    determined implicitly by context. The origin can be used to identify the
    context from which the object originated.
    """
    type = "Add"


class Arrive(IntransitiveActivity):
    """
    An IntransitiveActivity that indicates that the actor has arrived at the
    location. The origin can be used to identify the context from which the
    actor originated. The target typically has no defined meaning.
    """
    type = "Arrive"


class Create(Activity):
    """
    Indicates that the actor has created the object.
    """
    type = "Create"


class Delete(Activity):
    """
    Indicates that the actor has deleted the object. If specified, the origin
    indicates the context from which the object was deleted.
    """
    type = "Delete"


class Follow(Activity):
    """
    Indicates that the actor is "following" the object. Following is defined
    in the sense typically used within Social systems in which the actor is
    interested in any activity performed by or on the object. The target and
    origin typically have no defined meaning.
    """
    type = "Follow"


class Ignore(Activity):
    """
    Indicates that the actor is ignoring the object. The target and origin
    typically have no defined meaning.
    """
    type = "Ignore"


class Join(Activity):
    """
    Indicates that the actor has joined the object. The target and origin
    typically have no defined meaning.
    """
    type = "Join"


class Leave(Activity):
    """
    Indicates that the actor has left the object. The target and origin
    typically have no meaning.
    """
    type = "Leave"


class Like(Activity):
    """
    Indicates that the actor likes, recommends or endorses the object. The
    target and origin typically have no defined meaning.
    """
    type = "Like"


class Offer(Activity):
    """
    Indicates that the actor is offering the object. If specified, the target
    indicates the entity to which the object is being offered.
    """
    type = "Offer"


class Invite(Offer):
    """
    A specialization of Offer in which the actor is extending an invitation
    for the object to the target.
    """
    type = "Invite"


class Reject(Activity):
    """
    Indicates that the actor is rejecting the object. The target and origin
    typically have no defined meaning.
    """
    type = "Reject"


class TentativeReject(Reject):
    """
    A specialization of Reject in which the rejection is considered tentative.
    """
    type = "TentativeReject"


class Remove(Activity):
    """
    Indicates that the actor is removing the object. If specified,
    the origin indicates the context from which the object is being removed.
    """
    type = "Remove"


class Undo(Activity):
    """
    Indicates that the actor is undoing the object. In most cases, the object
    will be an Activity describing some previously performed action (for
    instance, a person may have previously "liked" an article but,
    for whatever reason, might choose to undo that like at some later point
    in time).

    The target and origin typically have no defined meaning.
    """
    type = "Undo"


class Update(Activity):
    """
    Indicates that the actor has updated the object. Note, however, that this
    vocabulary does not define a mechanism for describing the actual set of
    modifications made to object.

    The target and origin typically have no defined meaning.
    """
    type = "Update"


class View(Activity):
    """
    Indicates that the actor has viewed the object.
    """
    type = "View"


class Listen(Activity):
    """
    Indicates that the actor has listened to the object.
    """
    type = "Listen"


class Read(Activity):
    """
    Indicates that the actor has read the object.
    """
    type = "Read"


class Move(Activity):
    """
    Indicates that the actor has moved object from origin to target. If the
    origin or target are not specified, either can be determined by context.
    """
    type = "Move"


class Travel(IntransitiveActivity):
    """
    Indicates that the actor is traveling to target from origin. Travel is an
    IntransitiveObject whose actor specifies the direct object. If the target
    or origin are not specified, either can be determined by context.
    """
    type = "Travel"


class Announce(Activity):
    """
    Indicates that the actor is calling the target's attention the object.

    The origin typically has no defined meaning.
    """
    type = "Announce"


class Block(Ignore):
    """
    Indicates that the actor is blocking the object. Blocking is a stronger
    form of Ignore. The typical use is to support social systems that allow
    one user to block activities or content of other users. The target and
    origin typically have no defined meaning.
    """
    type = "Block"


class Flag(Activity):
    """
    Indicates that the actor is "flagging" the object. Flagging is defined in
    the sense common to many social platforms as reporting content as being
    inappropriate for any number of reasons.
    """
    type = "Flag"


class Dislike(Activity):
    """
    Indicates that the actor dislikes the object.
    """
    type = "Dislike"


class Question(IntransitiveActivity):
    """
    Represents a question being asked. Question objects are an extension of
    IntransitiveActivity. That is, the Question object is an Activity,
    but the direct object is the question itself, therefore it would not
    contain an object property.

    Either of the anyOf and oneOf properties MAY be used to express possible
    answers, but a Question object MUST NOT have both properties.
    """
    type = "Question"

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


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# ACTOR TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#actor-types
#
#   These classes serve as the actors who interact with the objects on a site
#   and perform activities
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class Application(Object):
    """
    Describes a software application.
    """
    type = "Application"


class Group(Object):
    """
    Represents a formal or informal collective of Actors.
    """
    type = "Group"


class Organization(Object):
    """
    Represents an organization.
    """
    type = "Organization"


class Person(Object):
    """
    Represents an individual person.
    """
    type = "Person"


class Service(Object):
    """
    Represents a service of any kind.
    """
    type = "Service"


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# OBJECT TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#object-types
#
#   These classes serve as the objects that are acted upon by actors
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class Relationship(Object):
    """
    Describes a relationship between two individuals. The subject and object
    properties are used to identify the connected individuals.
    """
    type = "Relationship"

    def __init__(self, id, subject=None, object=None, relationship=None,
                 **kwargs):
        super().__init__(id, **kwargs)
        self.subject = subject
        self.object = object
        self.relationship = relationship


class Article(Object):
    """
    Represents any kind of multi-paragraph written work.
    """
    type = "Article"


class Document(Object):
    """
    Represents a document of any kind.
    """
    type = "Document"


class Audio(Document):
    """
    Represents an audio document of any kind.
    """
    type = "Audio"


class Image(Document):
    """
    An image document of any kind
    """
    type = "Image"


class Video(Document):
    """
    Represents a video document of any kind.
    """
    type = "Video"


class Note(Object):
    """
    Represents a short written work typically less than a single paragraph in
    length.
    """
    type = "Note"


class Page(Document):
    """
    Represents a Web Page.
    """
    type = "Page"


class Event(Object):
    """
    Represents any kind of event.
    """
    type = "Event"


class Place(Object):
    """
    Represents a logical or physical location. See 5.3 Representing Places
    for additional information.
    """
    type = "Place"

    def __init__(self, id, accuracy=None, altitude=None, latitude=None,
                 longitude=None, radius=None, units=None, **kwargs):
        super().__init__(id, **kwargs)
        self.accuracy = accuracy
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.units = units


class Profile(Object):
    """
    A Profile is a content object that describes another Object, typically
    used to describe Actor Type objects. The describes property is used to
    reference the object being described by the profile.
    """
    type = "Profile"

    def __init__(self, id, describes=None, **kwargs):
        super().__init__(id, **kwargs)
        self.describes = describes


class Tombstone(Object):
    """
    A Tombstone represents a content object that has been deleted. It can be
    used in Collections to signify that there used to be an object at this
    position, but it has been deleted.
    """
    type = "Tombstone"

    def __init__(self, id, former_type=None, deleted=None, **kwargs):
        super().__init__(id, **kwargs)
        self.former_type = former_type
        self.deleted = deleted


class Mention(Link):
    """
    A specialized Link that represents a @mention.
    """
    type = "Mention"

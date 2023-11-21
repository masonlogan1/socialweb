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
from validators import url

CONTEXT = "https://www.w3.org/ns/activitystreams"


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
                 media_type=None, duration=None, **kwargs):
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
                 hreflang=None, height=None, width=None, preview=None,
                 **kwargs):
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
        super().__init__(id, **kwargs)
        # intransitive activities do NOT inherit the 'object' attribute
        delattr(self, 'object')


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
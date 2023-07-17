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
                 url=None,
                 to=None, bto=None, cc=None, bcc=None, media_type=None,
                 duration=None):
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


class Activity(Object):
    """
    An Activity is a subtype of Object that describes some form of action
    that may happen, is currently happening, or has already happened. The
    Activity type itself serves as an abstract base type for all types of
    activities. It is important to note that the Activity type itself does
    not carry any specific semantics about the kind of action being taken.
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

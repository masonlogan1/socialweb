"""
Actor types are Object types that are capable of performing activities.
"""
__ref__ = "https://www.w3.org/TR/activitystreams-vocabulary/#actor-types"

from abc import ABC

from activitystreams.models import ApplicationModel, GroupModel, \
    OrganizationModel, PersonModel, ServiceModel
from activitystreams.core import Object
from activitystreams.objects import Relationship


class Actor(ABC):
    """
    Abstract class that provides methods that allow an Actor to create, update,
    and delete various objects. CANNOT BE INSTANTIATED! WILL RAISE AN EXCEPTION!
    """

    def create_relationship(self, id=None, attachment=None, attributedTo=None,
                            audience=None, content=None, context=None,
                            name=None, endTime=None, generator=None, icon=None,
                            image=None, inReplyTo=None, location=None,
                            preview=None, published=None, replies=None,
                            startTime=None, summary=None, tag=None,
                            updated=None, url=None, to=None, bto=None, cc=None,
                            bcc=None, mediaType=None,
                            duration=None):
        """
        Creates a Relationship object and creates a two-way link between the
        object and the creator
        :param id: the unique IRI for this resource
        :param attachment: a resource that potentially requires special handling
        :param attributedTo: one or more entities this object is attributed to
        :param audience: one or more entities this object is intended for
        :param content: the textual representation of the object as a string, should be html unless specified by mediaType
        :param context: the context in which the object exists
        :param name: human-readable plain-text description
        :param endTime: datetime for when an object "ends"
        :param generator: the entity that generated the object
        :param icon: the icon for the object
        :param image: the image for the object
        :param inReplyTo: one or more entities this object is a reply to
        :param location: one or more physical locations associated with this object
        :param preview: an entity providing a preview of the object
        :param published: datetime of when an object was originally published
        :param replies: a collection of objects considered to be responses to this object
        :param startTime: datetime for when an object "begins"
        :param summary: natural language summarization encoded as html
        :param tag: one or more "tags" associated with the object
        :param updated: datetime for when the object was last updated
        :param url: one or more links to representations of the object
        :param to: one or more members of the primary public audience
        :param bto: one or more members of the primary private audience
        :param cc: one or more members of the secondary public audience
        :param bcc: one or more members of the secondary private audience
        :param mediaType: identifies the MIME type of the object
        :param duration: describes a time-bound resource, such as the length of a video
        :return: a Relationship mutually linked to the calling object
        """
        obj = Relationship(id=id, attachment=attachment,
                           attributedTo=attributedTo, audience=audience,
                           content=content, context=context, name=name,
                           endTime=endTime, generator=generator, icon=icon,
                           image=image, inReplyTo=inReplyTo, location=location,
                           preview=preview, published=published,
                           replies=replies, startTime=startTime,
                           summary=summary, tag=tag, updated=updated, url=url,
                           to=to, bto=bto, cc=cc, bcc=bcc, mediaType=mediaType,
                           duration=duration)

    def create_article(self, id=None, attachment=None, attributedTo=None,
                       audience=None, content=None, context=None, name=None,
                       endTime=None, generator=None, icon=None, image=None,
                       inReplyTo=None, location=None, preview=None,
                       published=None, replies=None, startTime=None,
                       summary=None, tag=None, updated=None, url=None, to=None,
                       bto=None, cc=None, bcc=None, mediaType=None,
                       duration=None):
        pass

    def create_document(self, id=None, attachment=None, attributedTo=None,
                        audience=None, content=None, context=None, name=None,
                        endTime=None, generator=None, icon=None, image=None,
                        inReplyTo=None, location=None, preview=None,
                        published=None, replies=None, startTime=None,
                        summary=None, tag=None, updated=None, url=None, to=None,
                        bto=None, cc=None, bcc=None, mediaType=None,
                        duration=None):
        pass

    def create_audio(self, id=None, attachment=None, attributedTo=None,
                     audience=None, content=None, context=None, name=None,
                     endTime=None, generator=None, icon=None, image=None,
                     inReplyTo=None, location=None, preview=None,
                     published=None, replies=None, startTime=None, summary=None,
                     tag=None, updated=None, url=None, to=None, bto=None,
                     cc=None, bcc=None, mediaType=None, duration=None):
        pass

    def create_image(self, id=None, attachment=None, attributedTo=None,
                     audience=None, content=None, context=None, name=None,
                     endTime=None, generator=None, icon=None, image=None,
                     inReplyTo=None, location=None, preview=None,
                     published=None, replies=None, startTime=None, summary=None,
                     tag=None, updated=None, url=None, to=None, bto=None,
                     cc=None, bcc=None, mediaType=None, duration=None):
        pass

    def create_video(self, id=None, attachment=None, attributedTo=None,
                     audience=None, content=None, context=None, name=None,
                     endTime=None, generator=None, icon=None, image=None,
                     inReplyTo=None, location=None, preview=None,
                     published=None, replies=None, startTime=None, summary=None,
                     tag=None, updated=None, url=None, to=None, bto=None,
                     cc=None, bcc=None, mediaType=None, duration=None):
        pass

    def create_note(self, id=None, attachment=None, attributedTo=None,
                    audience=None, content=None, context=None, name=None,
                    endTime=None, generator=None, icon=None, image=None,
                    inReplyTo=None, location=None, preview=None, published=None,
                    replies=None, startTime=None, summary=None, tag=None,
                    updated=None, url=None, to=None, bto=None, cc=None,
                    bcc=None, mediaType=None, duration=None):
        pass

    def create_page(self, id=None, attachment=None, attributedTo=None,
                    audience=None, content=None, context=None, name=None,
                    endTime=None, generator=None, icon=None, image=None,
                    inReplyTo=None, location=None, preview=None, published=None,
                    replies=None, startTime=None, summary=None, tag=None,
                    updated=None, url=None, to=None, bto=None, cc=None,
                    bcc=None, mediaType=None, duration=None):
        pass

    def create_event(self, id=None, attachment=None, attributedTo=None,
                     audience=None, content=None, context=None, name=None,
                     endTime=None, generator=None, icon=None, image=None,
                     inReplyTo=None, location=None, preview=None,
                     published=None, replies=None, startTime=None, summary=None,
                     tag=None, updated=None, url=None, to=None, bto=None,
                     cc=None, bcc=None, mediaType=None, duration=None):
        pass

    def create_place(self, id=None, attachment=None, attributedTo=None,
                     audience=None, content=None, context=None, name=None,
                     endTime=None, generator=None, icon=None, image=None,
                     inReplyTo=None, location=None, preview=None,
                     published=None, replies=None, startTime=None, summary=None,
                     tag=None, updated=None, url=None, to=None, bto=None,
                     cc=None, bcc=None, mediaType=None, duration=None):
        pass

    def create_profile(self, id=None, attachment=None, attributedTo=None,
                       audience=None, content=None, context=None, name=None,
                       endTime=None, generator=None, icon=None, image=None,
                       inReplyTo=None, location=None, preview=None,
                       published=None, replies=None, startTime=None,
                       summary=None, tag=None, updated=None, url=None, to=None,
                       bto=None, cc=None, bcc=None, mediaType=None,
                       duration=None):
        pass

    def create_tombstone(self, id=None, attachment=None, attributedTo=None,
                         audience=None, content=None, context=None, name=None,
                         endTime=None, generator=None, icon=None, image=None,
                         inReplyTo=None, location=None, preview=None,
                         published=None, replies=None, startTime=None,
                         summary=None, tag=None, updated=None, url=None,
                         to=None, bto=None, cc=None, bcc=None, mediaType=None,
                         duration=None):
        pass


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# ACTOR TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#actor-types
#
#   These classes serve as the actors who interact with the objects on a site
#   and perform activities
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//


class Application(Actor, Object, ApplicationModel):
    """
    Describes a software application.
    """


class Group(Actor, Object, GroupModel):
    """
    Represents a formal or informal collective of Actors.
    """


class Organization(Actor, Object, OrganizationModel):
    """
    Represents an organization.
    """


class Person(Actor, Object, PersonModel):
    """
    Represents an individual person.
    """


class Service(Actor, Object, ServiceModel):
    """
    Represents a service of any kind.
    """

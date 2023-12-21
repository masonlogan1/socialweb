"""
Actor types are Object types that are capable of performing activities.
"""
__ref__ = "https://www.w3.org/TR/activitystreams-vocabulary/#actor-types"

from typing import List, Union
from datetime import datetime

from activitystreams.models import ApplicationModel, GroupModel, \
    OrganizationModel, PersonModel, ServiceModel
from activitystreams.core import Object, Link, Collection
from activitystreams.objects import Note
from activitystreams.activity import Create


class Actor(Object):
    """
    Base class that defines standardized behavior for actor objects
    """
    type = "Actor"

    def create(self, id, object, summary: str = None, to: List = None,
               **kwargs) -> Create:
        """
        Generic method for generating a Create object linked back to the actor
        :param id: the id for the new Create
        :param object: the object being created
        :param summary: brief summary of the created object
        :param to: audience intended for the created object
        :return: Create
        """
        new = Create(id=id, object=object, to=to, summary=summary,
                     actor=self, published=datetime.now(), **kwargs)
        return new

    def create_note(self, create_id: str, note_id: str, content: str, url: str,
                    summary: str = None, inReplyTo: Object = None,
                    name: str = None, to: List = None, cc: List = None,
                    attachment: Union[Object, Link] = None,
                    tag: List = None, replies: Collection = None) -> Create:
        note = Note(id=note_id, url=url, content=content, summary=summary,
                    inReplyTo=inReplyTo, to=to, cc=cc, attachment=attachment,
                    tag=tag, replies=replies, attributedTo=self, name=name)
        create_obj = self.create(id=create_id, object=note,
                                 summary=f"{self.name} created a note")
        return create_obj

    def serialize(self):
        return self.data(include=('id', 'name', 'type'))


# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//
# ACTOR TYPES
#   REF: https://www.w3.org/TR/activitystreams-vocabulary/#actor-types
#
#   These classes serve as the actors who interact with the objects on a site
#   and perform activities
#
# ==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//==//

class Application(Actor, ApplicationModel):
    """
    Describes a software application.
    """
    type = "Application"


class Group(Actor, GroupModel):
    """
    Represents a formal or informal collective of Actors.
    """
    type = "Group"


class Organization(Actor, OrganizationModel):
    """
    Represents an organization.
    """
    type = "Organization"


class Person(Actor, PersonModel):
    """
    Represents an individual person.
    """
    type = "Person"


class Service(Actor, ServiceModel):
    """
    Represents a service of any kind.
    """
    type = "Service"

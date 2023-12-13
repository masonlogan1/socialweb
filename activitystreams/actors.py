"""
Actor types are Object types that are capable of performing activities.
"""
__ref__ = "https://www.w3.org/TR/activitystreams-vocabulary/#actor-types"

from abc import ABC
from typing import List
from datetime import datetime

from activitystreams.models import ApplicationModel, GroupModel, \
    OrganizationModel, PersonModel, ServiceModel
from activitystreams.core import Object
from activitystreams.objects import Relationship
from activitystreams.activity import Create


class Actor(Object):
    """
    Base class that defines standardized behavior for actor objects
    """
    type = "Actor"
    context = "https://www.w3.org/ns/activitystreams"

    def _create(self, id, obj, summary: str = None, to: List = None,
                **kwargs) -> Create:
        """
        Generic method for generating a Create object linked back to the actor
        :param id: the id for the new Create
        :param object: the object linked to the new Create
        :return: Create
        """
        new = Create(id=id, object=obj, summary=summary, to=to,
                     actor=self, published=datetime.now(), **kwargs)
        return new


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
    type = "Application"
    context = "https://www.w3.org/ns/activitystreams#Application"


class Group(Actor, Object, GroupModel):
    """
    Represents a formal or informal collective of Actors.
    """
    type = "Group"
    context = "https://www.w3.org/ns/activitystreams#Group"


class Organization(Actor, Object, OrganizationModel):
    """
    Represents an organization.
    """
    type = "Organization"
    context = "https://www.w3.org/ns/activitystreams#Organization"


class Person(Actor, Object, PersonModel):
    """
    Represents an individual person.
    """
    type = "Person"
    context = "https://www.w3.org/ns/activitystreams#Person"


class Service(Actor, Object, ServiceModel):
    """
    Represents a service of any kind.
    """
    type = "Service"
    context = "https://www.w3.org/ns/activitystreams#Service"

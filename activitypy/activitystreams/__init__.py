__author__ = "Mason Logan"
__credits__ = ['Mason Logan']
__license__ = "MIT"
__version__ = "0.0.1dev"
__maintainer__ = "Mason Logan"
__email__ = "pyactivitystreams@masonlogan.com"
__status__ = "Development"
__source__ = "https://www.w3.org/TR/activitystreams-vocabulary/#properties"

import datetime

__created__ = datetime.datetime(2023, 7, 16)
__updated__ = datetime.datetime(2023, 12, 11)

from activitypy.activitystreams.core import Object, Link, Activity, IntransitiveActivity, \
    Collection, OrderedCollection, CollectionPage, OrderedCollectionPage
from activitypy.activitystreams.actors import Application, Group, Organization, Person, \
    Service
from activitypy.activitystreams.activity import Accept, TentativeAccept, Add, Arrive, \
    Create, Delete, Follow, Ignore, Join, Leave, Like, Offer, Invite, Reject, \
    TentativeReject, Remove, Undo, Update, View, Listen, Read, Move, Travel, \
    Announce, Block, Flag, Dislike, Question
from activitypy.activitystreams.objects import Relationship, Article, Document, Audio, \
    Image, Video, Note, Page, Event, Place, Profile, Tombstone, Mention


def update_stringify_map():
    # we can't import the objects directly into utils without causing a
    # circular import error, so we import the map and the objects and map
    # a function that runs obj.data(exclude=('acontext',)) on all
    # ActivityStreams objects
    from activitypy.activitystreams.utils import STRINGIFY_MAP

    def get_data(obj):
        return obj.data(exclude=('acontext',))
    
    STRINGIFY_MAP.update({
        Object: get_data,
        Link: get_data,
        Activity: get_data,
        IntransitiveActivity: get_data,
        Collection: get_data,
        OrderedCollection: get_data,
        CollectionPage: get_data,
        OrderedCollectionPage: get_data,
        Application: get_data,
        Group: get_data,
        Organization: get_data,
        Person: get_data,
        Service: get_data,
        Accept: get_data,
        TentativeAccept: get_data,
        Add: get_data,
        Arrive: get_data,
        Create: get_data,
        Delete: get_data,
        Follow: get_data,
        Ignore: get_data,
        Join: get_data,
        Leave: get_data,
        Like: get_data,
        Offer: get_data,
        Invite: get_data,
        Reject: get_data,
        TentativeReject: get_data,
        Remove: get_data,
        Undo: get_data,
        Update: get_data,
        View: get_data,
        Listen: get_data,
        Read: get_data,
        Move: get_data,
        Travel: get_data,
        Announce: get_data,
        Block: get_data,
        Flag: get_data,
        Dislike: get_data,
        Question: get_data,
        Relationship: get_data,
        Article: get_data,
        Document: get_data,
        Audio: get_data,
        Image: get_data,
        Video: get_data,
        Note: get_data,
        Page: get_data,
        Event: get_data,
        Place: get_data,
        Profile: get_data,
        Tombstone: get_data,
        Mention: get_data,
    })


update_stringify_map()
del update_stringify_map

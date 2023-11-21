__author__ = "Mason Logan"
__credits__ = ['Mason Logan']
__license__ = "MIT"
__version__ = "0.0.1dev"
__maintainer__ = "Mason Logan"
__email__ = "pyactivitystreams@masonlogan.com"
__status__ = "Development"
__source__ = "https://www.w3.org/TR/activitystreams-vocabulary/#properties"

# makes all objects and properties importable without having to import their
# specific modules
from vocabulary.core_types import Object, Link, Activity, \
    IntransitiveActivity, Collection, OrderedCollection, CollectionPage, \
    OrderedCollectionPage
from vocabulary.activity_types import Accept, TentativeAccept, Add, Arrive, \
    Create, Delete, Follow, Ignore, Join, Leave, Like, Offer, Invite, Reject, \
    TentativeReject, Remove, Undo, Update, View, Listen, Read, Move, Travel, \
    Announce, Block, Flag, Dislike, Question
from vocabulary.actor_types import Application, Group, Organization, Person, \
    Service
from vocabulary.object_types import Relationship, Article, Document, Audio, \
    Image, Video, Note, Page, Event, Place, Profile, Tombstone
from vocabulary.link_types import Mention
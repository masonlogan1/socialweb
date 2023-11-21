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
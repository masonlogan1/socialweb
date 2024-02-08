__author__ = "Mason Logan"
__credits__ = ['Mason Logan']
__license__ = "MIT"
__version__ = "0.0.1dev"
__maintainer__ = "Mason Logan"
__email__ = "pyactivitystreams@masonlogan.com"
__status__ = "Development"
__source__ = "https://www.w3.org/TR/activitystreams-vocabulary/#properties"

from pyld.jsonld import set_document_loader
from activitypy.jsonld import register_jsonld_type, update_jsonld_type, \
    register_property, JSON_TYPE_MAP

from activitypy.activitystreams import Object, Link, Activity, \
    IntransitiveActivity, Collection, OrderedCollection, CollectionPage, \
    OrderedCollectionPage, Application, Group, Organization, Person, \
    Service, Accept, TentativeAccept, Add, Arrive, Create, Delete, Follow, \
    Ignore, Join, Leave, Like, Offer, Invite, Reject, TentativeReject, Remove, \
    Undo, Update, View, Listen, Read, Move, Travel, Announce, Block, Flag, \
    Dislike, Question, Relationship, Article, Document, Audio, \
    Image, Video, Note, Page, Event, Place, Profile, Tombstone, Mention

# Registers the types from the activitystreams spec
register_jsonld_type('default', Object)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Object', Object)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Link', Link)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Activity', Activity)
register_jsonld_type('https://www.w3.org/ns/activitystreams#IntransitiveActivity', IntransitiveActivity)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Collection', Collection)
register_jsonld_type('https://www.w3.org/ns/activitystreams#OrderedCollection', OrderedCollection)
register_jsonld_type('https://www.w3.org/ns/activitystreams#CollectionPage', CollectionPage)
register_jsonld_type('https://www.w3.org/ns/activitystreams#OrderedCollectionPage', OrderedCollectionPage)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Application', Application)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Group', Group)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Organization', Organization)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Person', Person)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Service', Service)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Accept', Accept)
register_jsonld_type('https://www.w3.org/ns/activitystreams#TentativeAccept', TentativeAccept)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Add', Add)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Arrive', Arrive)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Create', Create)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Delete', Delete)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Follow', Follow)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Ignore', Ignore)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Join', Join)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Leave', Leave)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Like', Like)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Offer', Offer)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Invite', Invite)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Reject', Reject)
register_jsonld_type('https://www.w3.org/ns/activitystreams#TentativeReject', TentativeReject)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Remove', Remove)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Undo', Undo)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Update', Update)
register_jsonld_type('https://www.w3.org/ns/activitystreams#View', View)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Listen', Listen)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Read', Read)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Move', Move)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Travel', Travel)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Announce', Announce)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Block', Block)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Flag', Flag)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Dislike', Dislike)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Question', Question)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Relationship', Relationship)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Article', Article)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Document', Document)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Audio', Audio)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Image', Image)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Video', Video)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Note', Note)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Page', Page)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Event', Event)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Place', Place)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Profile', Profile)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Tombstone', Tombstone)
register_jsonld_type('https://www.w3.org/ns/activitystreams#Mention', Mention)

# establishes a configurable object as the document loader for the jsonld parser
JSONLD_DOCLOADER = jsonld.CachedRequestsJsonLoader()
set_document_loader(JSONLD_DOCLOADER)
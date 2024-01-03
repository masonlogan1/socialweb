"""
Unimplemented models for use in the activitystreams framework; models contain
the properties required to implement the objects but do not have any methods
or tools that make them useful.
"""
from activitypy.activitystreams.models.models import \
    AcceptModel, ActivityModel, AddModel, AnnounceModel, ApplicationModel, \
    ArriveModel, ArticleModel, AudioModel,BlockModel, \
    CollectionModel, CollectionPageModel, CreateModel, DeleteModel, \
    DislikeModel, DocumentModel, EventModel, FlagModel, FollowModel, \
    GroupModel, IgnoreModel, ImageModel, IntransitiveActivityModel, \
    InviteModel, JoinModel, LeaveModel, LikeModel, LinkModel, ListenModel, \
    MentionModel, MoveModel, NoteModel, ObjectModel, OfferModel, \
    OrderedCollectionModel, OrderedCollectionPageModel, OrganizationModel, \
    PageModel, PersonModel, PlaceModel, ProfileModel, QuestionModel, \
    ReadModel, RejectModel, RelationshipModel, RemoveModel, ServiceModel, \
    TentativeAcceptModel, TentativeRejectModel, TombstoneModel, TravelModel, \
    UndoModel, UpdateModel, VideoModel, ViewModel

def register_models():
    from inspect import getmembers, isclass
    from activitypy.activitystreams.models.utils import MODELS
    from activitypy.activitystreams.models import models
    from activitypy.jsonld import ApplicationActivityJson
    for name, cls in getmembers(models):
        if isclass(cls) and ApplicationActivityJson in cls.mro():
            MODELS.register_class(cls)

register_models()
del register_models
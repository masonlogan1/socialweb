from jsonld.jsonld import PropertyJsonLD, ApplicationActivityJson
from jsonld.base import JsonProperty, contextualproperty
from jsonld.utils import JSON_LD_KEYMAP, JSON_DATA_CONTEXT, jsonld_get
from jsonld.engine.jsonld_engine import JsonLdEngine
from jsonld.package import JsonLdPackage

from pyld.jsonld import set_document_loader
from jsonld.docloader import CachedRequestsJsonLoader

# establishes a configurable object as the document loader for the jsonld parser
JSONLD_DOCLOADER = CachedRequestsJsonLoader()
set_document_loader(JSONLD_DOCLOADER)
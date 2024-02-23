__author__ = "Mason Logan"
__credits__ = ['Mason Logan']
__license__ = "MIT"
__version__ = "0.0.1dev"
__maintainer__ = "Mason Logan"
__email__ = "pyactivitystreams@masonlogan.com"
__status__ = "Development"
__source__ = "https://www.w3.org/TR/activitystreams-vocabulary/#properties"

from pyld.jsonld import set_document_loader
from activitypy.jsonld import CachedRequestsJsonLoader

# establishes a configurable object as the document loader for the jsonld parser
JSONLD_DOCLOADER = CachedRequestsJsonLoader()
set_document_loader(JSONLD_DOCLOADER)

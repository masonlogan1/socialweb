"""
Tools for working with json-ld data
"""
import json
import logging
import re
from urllib import parse
from collections.abc import Iterable
from itertools import chain

from typing import Union

import requests

from pyld import jsonld
from pyld.jsonld import JsonLdError, parse_link_header, LINK_HEADER_REL, \
    expand

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

JSON_LD_KEYMAP = {
    'abase': '@base',
    'acontainer': '@container',
    'acontext': '@context',
    'adirection': '@direction',
    'agraph': '@graph',
    'aid': '@id',
    'aimport': '@import',
    'aincluded': '@included',
    'aindex': '@index',
    'ajson': '@json',
    'alanguage': '@language',
    'alist': '@list',
    'anest': '@nest',
    'anone': '@none',
    'aprefix': '@prefix',
    'apropagate': '@propagate',
    'aprotected': '@protected',
    'areverse': '@reverse',
    'aset': '@set',
    'atype': '@type',
    'avalue': '@value',
    'aversion': '@version',
    'avocab': '@vocab',
}

JSON_LD_URL_REGEX = re.compile('[^a-zA-Z0-9_\-.:]+')

# keys are "type" attributes on incoming json, values are classes they map to
# the __init__ file should be used to populate this to avoid circular imports
JSON_TYPE_MAP = {

}


# These are separate methods to ensure existing types are not accidentally
# overwritten; there are already so many that it's easy to mess up
def register_jsonld_type(name: str, cls: object):
    """
    Adds a name-class mapping to the JSON_TYPE_MAP
    """
    if name in JSON_TYPE_MAP.keys():
        raise ValueError(f'"{name}" already exists in mapping, cannot add new')
    JSON_TYPE_MAP.update({name: cls})


def update_jsonld_type(name: str, cls: object):
    """
    Updates an existing mapping to the JSON_TYPE_MAP
    """
    if name not in JSON_TYPE_MAP.keys():
        raise ValueError(f'"{name}" not in mapping yet, cannot update')
    JSON_TYPE_MAP.update({name: cls})


class PropertyObject:
    """
    Base object that provides tools for working with object properties.
    Provides a __get_properties__ method to produce a tuple for classes and a
    __properties__ variable to instances of inheriting classes
    """

    def __init__(self):
        self.__properties__ = self.__get_properties__()

    def __iter__(self):
        for prop in self.__properties__:
            yield prop, getattr(self, prop)

    def __getitem__(self, keys):
        keys = [keys] if isinstance(keys, str) else keys
        if any(key not in self.__properties__ for key in keys):
            bad_keys = [key for key in keys if key not in self.__properties__]
            raise KeyError(f'''Key{'s' if len(bad_keys) > 1 else ''} ''' +
                           f'''('{"', '".join(bad_keys)}') ''' +
                           f'''not in type '{self.__class__.__name__}\'''')
        return {key: getattr(self, key) for key in keys}

    @classmethod
    def __get_properties__(cls):
        """
        Creates a list of all @property objects defined and inherited in
        this class
        """
        props = tuple(chain(key for kls in cls.mro()
                            for key, value in kls.__dict__.items()
                            if isinstance(value, property)))
        return props


class AContext:
    __acontext = None

    @property
    def acontext(self):
        return self.__acontext

    @acontext.setter
    def acontext(self, value):
        self.__acontext = value


class RequestsJsonLoader:
    """
    Modified version of pyld.jsonld.requests_document_loader that fixes an
    issue where application/ld+json can be pushed aside in favor of text/html
    as the return type. Also tries to improve readability and documentation
    and makes the object callable rather than returning an internal function

    :param secure: require all requests to use HTTPS (default: False).
    :param **kwargs: extra keyword args for Requests get() call.

    :return: the RemoteDocument loader function.
    """

    headers = {'Accept': 'application/ld+json'}

    def __init__(self, secure=True, headers=None):
        self.secure = secure
        self.headers = headers if headers else self.headers

    def __call__(self, url, *args, **kwargs):
        """
        Passes the url into RequestsDocumentLoader().get(url)
        :param url:
        :return:
        """
        try:
            return self.get(url)
        except Exception as cause:
            # the only reason I'm keeping this is for consistency
            raise JsonLdError(
                'Could not retrieve a JSON-LD document from the URL.',
                'jsonld.LoadDocumentError', code='loading document failed',
                cause=cause)

    def get(self, url):
        """
        Retrieves JSON-LD at the given URL.
        :param url: the URL to retrieve.
        :return: the RemoteDocument.
        """
        pieces = parse.urlparse(url)
        # urls must start with "http" or "https"
        if not pieces.scheme or pieces.scheme not in ['http', 'https']:
            raise ValueError(
                'Cannot dereference url without valid scheme; add ' +
                f'''{'"http://" or' if not self.secure else ''} ''' +
                '"https://" to url')
        # urls must have a body
        if not pieces.netloc:
            raise ValueError('Cannot dereference url without body')
        # urls can only have certain characters
        if re.match(JSON_LD_URL_REGEX, pieces.netloc):
            raise ValueError('url cannot contain characters outside of' +
                             'alphanumeric (a-Z, 0-9), "-", "_", ":", and "."')
        # secure connections MUST use https
        if self.secure and pieces.scheme != 'https':
            raise ValueError('Cannot dereference non-"https://" url when ' +
                             'secure=True; set secure=False or change scheme')

        response = requests.get(url, headers=self.headers)

        content_type = response.headers.get('content-type')
        if not content_type:
            content_type = 'application/octet-stream'
        doc = {
            'contentType': content_type,
            'contextUrl': None,
            'documentUrl': response.url,
            'document': response.json()
        }
        link_header = response.headers.get('link')
        if link_header:
            linked_context = parse_link_header(link_header).get(LINK_HEADER_REL)
            # only 1 related link header permitted
            if linked_context and content_type != 'application/ld+json':
                if isinstance(linked_context, list):
                    raise JsonLdError(
                        'URL could not be dereferenced, '
                        'it has more than one '
                        'associated HTTP Link Header.',
                        'jsonld.LoadDocumentError',
                        {'url': url},
                        code='multiple context link headers')
                doc['contextUrl'] = linked_context['target']
            linked_alternate = parse_link_header(link_header).get('alternate')
            # if not JSON-LD, alternate may point there
            if linked_alternate and \
                    linked_alternate.get('type') == 'application/ld+json' and \
                    not re.match(r'^application/(\w*\+)?json$', content_type):
                doc['contentType'] = 'application/ld+json'
                doc['documentUrl'] = jsonld.prepend_base(
                    url, linked_alternate['target'])
        return doc


class JsonLD(PropertyObject, AContext):
    """
    Class for representing JSON-LD data. Utilizes @property objects for pulling
    instance data into JSON text representation
    """
    # overridable dict for mapping a transformation function to a property
    default_transforms = {}
    # overridable dict for mapping class types to a function for loading them
    # as objects
    type_constructor_map = {}

    def __init__(self, acontext):
        super().__init__()
        self.acontext = acontext

    def data(self, include: Iterable = (), exclude: Iterable = (),
             transforms: dict = None, rename: dict = None, include_none=False,
             reject_values: Iterable = ()) -> dict:
        """
        Returns the object's properties as a dictionary. Cannot include values
        that are not already a property of the object
        :param include: properties to include, defaults to all
        :param exclude: properties to exclude, defaults to none
        :param transforms: dict that maps data transformations by property name
        :param rename: dict that renames properties in the output dict
        :param include_none: includes pairs where value is None (defaults False)
        :param reject_values: values to refuse to include
        :return: dictionary of properties
        """
        transforms = {**self.default_transforms,
                      **(transforms if transforms else {})}
        rename = {**JSON_LD_KEYMAP, **(rename if rename else {})}
        data = {
            # change name of property, if provided in mapping
            rename.get(prop, prop):
            # change value (BY UNMAPPED NAME) with function, if provided
                transforms.get(prop, lambda o: getattr(o, prop))(self)
            for prop in self.__properties__
            # if include_null is True or the property is not None
            if (include_none or getattr(self, prop) is not None)
               # AND if including everything OR if specifically included
               and (not include or prop in include)
               # AND if excluding nothing OR if not specifically excluded
               and not (exclude and prop in exclude)
               and getattr(self, prop) not in reject_values}
        return data

    def json(self, include: Iterable = (), exclude: Iterable = (),
             transforms: dict = None, rename: dict = None, include_none=False,
             minified: bool = False) -> str:
        separators = (',', ':') if minified else None
        return json.dumps(self.data(include=include, exclude=exclude,
                                    transforms=transforms, rename=rename,
                                    include_none=include_none),
                          separators=separators)

    @classmethod
    def from_json(cls, data: Union[str, dict], classmap: dict = None):
        """
        Extracts fields from the provided JSON. Uses the @type value to
        determine the type of object to be created.
        :param data: JSON data to transform into Python object
        :param classmap: additional class mappings to use for conversion
        :return: Python object
        """
        # convert to dict and expand
        data = json.loads(data) if isinstance(data, str) else data
        expanded = expand(data)
        class_type = expanded.get('@type', '')
        if not class_type:
            logger.debug(f'Bad json-ld:\n{expanded}')
            raise ValueError('No @type value provided')

        # check that the @type value is in the mapping
        classmap = classmap if classmap else {}
        if class_type not in classmap.keys():
            raise ValueError('@type value not in mapping: "{class_type}"')

        # gets the class for the object that needs to be created from the
        object_class = classmap.get(class_type)
        if not object_class:
            ValueError(f'Provided data has invalid or missing "@type"')

        # filter out properties that are not part of the specified class and
        # populate None values where necessary
        expanded = {
            key: data.get(key, None)
            for key in object_class.__get_properties__()
        }

        return object_class(**expanded)

    def __str__(self):
        return self.json()

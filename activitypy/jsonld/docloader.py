"""
Classes used for loading jsonld documents with the pyld.jsonld package
"""
import logging
import re
from urllib import parse

import requests
from pyld import jsonld
from pyld.jsonld import JsonLdError, parse_link_header, LINK_HEADER_REL

JSON_LD_URL_REGEX = re.compile('[^a-zA-Z0-9_\-.:]+')


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
    logger = logging.getLogger('jsonld_request_loader')
    logger.setLevel(logging.INFO)
    headers = {'Accept': 'application/ld+json, application/activity+json'}

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

        self.logger.info(f'GET "{url}"; headers: {{{self.headers}}}')
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


class CachedRequestsJsonLoader(RequestsJsonLoader):
    """
    Modified version of the RequestsJsonLoader that caches schemas to prevent
    dozens of unnecessary calls when parsing large sets of jsonld data. Intended
    to be used as a singleton
    """

    cached_schemas = {}
    logger = logging.getLogger('cached-json-doc-loader')
    logger.setLevel(logging.INFO)

    def __init__(self, secure=True, headers=None):
        super().__init__(secure=secure, headers=headers)

    def __call__(self, url, *args, **kwargs):
        """
        Passes the url into RequestsDocumentLoader().get(url)
        :param url: the web location to get the jsonld document from
        :return:
        """
        try:
            if url not in self.cached_schemas.keys():
                self.logger.info(f'Caching schema for {url}')
                CachedRequestsJsonLoader.cached_schemas[url] = self.get(url)
            return self.cached_schemas.get(url)
        except Exception as cause:
            # the only reason I'm keeping this is for consistency
            raise JsonLdError(
                'Could not retrieve a JSON-LD document from the URL.',
                'jsonld.LoadDocumentError', code='loading document failed',
                cause=cause)

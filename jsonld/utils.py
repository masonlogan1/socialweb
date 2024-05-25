"""
Utility functions and constants for jsonld package
"""
import requests

JSON_DATA_CONTEXT = '_JSONLD_OUTPUT_CONTEXT_'
CLASS_CHANGE_CONTEXT = 'CLASS_CHANGE_CONTEXT'
SINGLE_NODE_CONTEXT = '_JSONLD_SINGLE_NODE_CONTEXT_'

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

DEFAULT_TYPE = 'https://www.w3.org/ns/activitystreams#Object'
DEFAULT_CONTEXT = "http://www.w3.org/ns/activitystreams#"

DEFAULT_HEADERS = {
    "Accept": "application/ld+json, application/activity+json, application/json"
}


def jsonld_get(url, headers: dict = None, json=True):
    """
    Makes a get request to retrieve jsonld data
    :param url: the url to make the request to
    :param headers: headers for the request
    :param json: whether to return a dict or the raw response
    :return: result of request
    """
    headers = {**DEFAULT_HEADERS, **(headers if headers else {})}
    resp = requests.get(url, headers=headers)
    return resp if not json else resp.json()

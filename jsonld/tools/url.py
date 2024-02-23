import logging
import re
from urllib import parse

import requests
from validate_email import validate_email

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

VALID_URL_REGEX = re.compile('[^a-zA-Z0-9_\-.:]+')

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

# TODO: ONE OF THESE NEEDS TO GO!
def validate_url(url, secure: bool = False):
    """
    Checks a provided URL to ensure it meets a handful of basic criteria for
    being a valid internet URL
    :param url: URL to validate
    :param secure: whether to accept only HTTPS urls
    :return: True if valid, False otherwise
    """
    pieces = parse.urlparse(url)
    if not pieces.scheme or pieces.scheme not in ['http', 'https']:
        logger.debug('Cannot dereference url without valid scheme; add ' +
                    f'''{'"http://" or' if not secure else ''} ''' +
                    '"https://" to url')
        return False
    # urls must have a body
    if not pieces.netloc:
        logger.debug('Cannot dereference url without body')
        return False
    # urls can only have certain characters
    if re.match(VALID_URL_REGEX, pieces.netloc):
        logger.debug('url cannot contain characters outside of' +
                    'alphanumeric (a-Z, 0-9), "-", "_", ":", and "."')
        return False
    # secure connections MUST use https
    if secure and pieces.scheme != 'https':
        logger.debug('Cannot dereference non-"https://" url when ' +
                    'secure=True; set secure=False or change scheme')
        return False
    return True


def validate_acct_or_email(val):
    """
    Validates whether the value is a valid email address or account link.
    Account links are formatted the same as email addresses, they just start
    with acct:
    :param val: the value to check
    :return: boolean to determine if the value is
    """
    # this is what's used in the AS examples, it may need further tuning!
    if val.startswith('acct:'):
        val = val[5:]
    return validate_email(val)
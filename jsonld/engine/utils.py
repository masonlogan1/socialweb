import logging
import re
from urllib import parse
from collections.abc import Iterable
from datetime import datetime, timedelta

from validate_email import validate_email

from jsonld.base import JsonProperty, PropertyAwareObject

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# TODO: temporary transitional files for refactor, clean up later!

VALID_URL_REGEX = re.compile('[^a-zA-Z0-9_\-.:]+')


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


def stringify_timedelta(obj) -> str:
    """
    Converts a timedelta to an ISO 8601 string
    :param obj: timedelta to convert
    :return: "P<years>Y<months>M<days>DT<hours>H<minutes>M<seconds>S" string
    """
    years = obj.days // 365
    months = (obj.days % 365) // 30
    days = (obj.days % 365) % 30
    hours = obj.seconds // 3600
    minutes = (obj.seconds % 3600) // 60
    seconds = (obj.seconds % 3600) % 60
    # P<years>Y<months>M<days>D
    ymd = 'P' + (f'{years}Y' if years else '') + \
          (f'{months}M' if months else '') + \
          (f'{days}D' if days else '')
    # T<hours>H<minutes>M<seconds>S
    hms = 'T' + (f'{hours}H' if hours else '') + \
          (f'{minutes}M' if minutes else '') + \
          (f'{seconds}S' if seconds else '')
    # The entire HMS section is optional, however we ALWAYS need at least the
    # "P" from the ymd section (indicates this is a "period")
    return f'{ymd}{hms if len(hms) > 1 else ""}'


def stringify_datetime(obj: datetime) -> str:
    """
    Converts a datetime object to ISO 8601 format
    :param obj: the datetime object to convert
    :return: "YYYY-mm-ddTHH:MM:SSZ" string
    """
    return obj.strftime('%Y-%m-%dT%H:%M:%SZ')


# matches a data type to a function
STRINGIFY_MAP = {
    datetime: stringify_datetime,
    float: float,
    timedelta: stringify_timedelta,
    str: str,
    int: int,
}


def stringify(obj):
    return STRINGIFY_MAP.get(obj.__class__, str)(obj)


def stringify_iterable(obj: Iterable):
    # we run the stringification process on every object in the iterable
    return [stringify(item) for item in obj]


def stringify_dict(obj: dict):
    # we want to ensure every key and value has been converted to a string
    # no one should be using a non-string key regardless!
    return {stringify(key): stringify(val) for key, val in obj.items()}


STRINGIFY_MAP.update({list: stringify_iterable, tuple: stringify_iterable,
                      set: stringify_iterable, dict: stringify_dict})


PROPERTY_TRANSFORM_MAP = {
    'accuracy': lambda obj: stringify(obj.accuracy),
    # DO NOT ALTER THE CONTEXT **EVER**, IT WILL BREAK THINGS BADLY!!
    'acontext': lambda obj: obj.acontext,
    'actor': lambda obj: stringify(obj.actor),
    'altitude': lambda obj: stringify(obj.altitude),
    'anyOf': lambda obj: stringify(obj.anyOf),
    'attachment': lambda obj: stringify(obj.attachment),
    'attributedTo': lambda obj: stringify(obj.attributedTo) if not hasattr(obj, 'actor') else None,
    'audience': lambda obj: stringify(obj.audience),
    'bcc': lambda obj: stringify(obj.bcc),
    'bto': lambda obj: stringify(obj.bto),
    'cc': lambda obj: stringify(obj.cc),
    'closed': lambda obj: stringify(obj.closed),
    'content': lambda obj: stringify(obj.content),
    'context': lambda obj: stringify(obj.context),
    'current': lambda obj: stringify(obj.current),
    'duration': lambda obj: stringify(obj.duration),
    'endTime': lambda obj: stringify(obj.endTime),
    'first': lambda obj: stringify(obj.first),
    'generator': lambda obj: stringify(obj.generator),
    'height': lambda obj: stringify(obj.height),
    'href': lambda obj: stringify(obj.href),
    'hrefLang': lambda obj: stringify(obj.hrefLang),
    'icon': lambda obj: stringify(obj.icon),
    'id': lambda obj: stringify(obj.id),
    'image': lambda obj: stringify(obj.image),
    'inReplyTo': lambda obj: stringify(obj.inReplyTo),
    'instrument': lambda obj: stringify(obj.instrument),
    'items': lambda obj: stringify(obj.items) if not hasattr(obj, 'orderedItems') else None,
    'last': lambda obj: stringify(obj.last),
    'location': lambda obj: stringify(obj.location),
    'mediaType': lambda obj: stringify(obj.mediaType),
    'name': lambda obj: stringify(obj.name),
    'next': lambda obj: stringify(obj.next),
    'object': lambda obj: stringify(obj.object),
    'oneOf': lambda obj: stringify(obj.oneOf),
    'orderedItems': lambda obj: stringify(obj.orderedItems),
    'origin': lambda obj: stringify(obj.origin),
    'partOf': lambda obj: stringify(obj.partOf),
    'prev': lambda obj: stringify(obj.prev),
    'preview': lambda obj: stringify(obj.preview),
    'published': lambda obj: stringify(obj.published),
    'replies': lambda obj: stringify(obj.replies),
    'result': lambda obj: stringify(obj),
    'startTime': lambda obj: stringify(obj.startTime),
    'summary': lambda obj: stringify(obj.summary),
    'tag': lambda obj: stringify(obj.tag),
    'target': lambda obj: stringify(obj.target),
    'to': lambda obj: stringify(obj.to),
    'type': lambda obj: stringify(obj.type),
    'updated': lambda obj: stringify(obj.updated),
    'url': lambda obj: stringify(obj.url),
}

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

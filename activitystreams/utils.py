"""
Utility functions for managing activitystreams data
"""
from collections.abc import Iterable
from datetime import datetime, timedelta


# used for mapping jsonld @ keys to proper names
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

# Compose multiple maps into this single one
STD_KEYMAP = {**JSON_LD_KEYMAP}


def object_or_string(obj):
    return obj if isinstance(obj, (str, Iterable, bool)) \
        else obj.data(exclude=('acontext',))


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


PROPERTY_TRANSFORM_MAP = {
    'accuracy': lambda obj: stringify(obj.accuracy),
    'acontext': lambda obj: stringify(obj.acontext),
    'actor': lambda obj: stringify(obj.actor),
    'altitude': lambda obj: stringify(obj.altitude),
    'anyOf': lambda obj: stringify(obj.anyOf),
    'attachment': lambda obj: stringify(obj.attachment),
    'attributedTo': lambda obj: stringify(obj.attributedTo),
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
    'items': lambda obj: stringify(obj.items),
    'last': lambda obj: stringify(obj.last),
    'location': lambda obj: stringify(obj.location),
    'mediaType': lambda obj: stringify(obj.mediaType),
    'name': lambda obj: stringify(obj.name),
    'next': lambda obj: stringify(obj.next),
    'object': lambda obj: stringify(obj.object),
    'oneOf': lambda obj: stringify(obj.oneOf),
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

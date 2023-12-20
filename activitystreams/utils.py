"""
Utility functions for managing activitystreams data
"""

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
    return obj if isinstance(obj, str) else obj.data(exclude=('acontext',))


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
    timedelta: stringify_timedelta
}


def stringify(obj):
    return STRINGIFY_MAP.get(obj.__class__, str)(obj)


PROPERTY_TRANSFORM_MAP = {
    'acontext': lambda obj: stringify(obj.acontext),
    'actor': lambda obj: object_or_string(obj.actor),
    'attachment': lambda obj: object_or_string(obj.attachment),
    'attributedTo': lambda obj: object_or_string(obj.attributedTo),
    'audience': lambda obj: object_or_string(obj.audience),
    'bcc': lambda obj: object_or_string(obj.bcc),
    'bto': lambda obj: object_or_string(obj.bto),
    'cc': lambda obj: object_or_string(obj.cc),
    'content': lambda obj: stringify(obj.content),
    'context': lambda obj: object_or_string(obj.context),
    'duration': lambda obj: stringify(obj.duration),
    'endTime': lambda obj: stringify(obj.endTime),
    'generator': lambda obj: object_or_string(obj.generator),
    'icon': lambda obj: object_or_string(obj.icon),
    'id': lambda obj: stringify(obj.id),
    'image': lambda obj: object_or_string(obj.image),
    'inReplyTo': lambda obj: object_or_string(obj.inReplyTo),
    'location': lambda obj: object_or_string(obj.location),
    'mediaType': lambda obj: stringify(obj.mediaType),
    'name': lambda obj: stringify(obj.name),
    'preview': lambda obj: object_or_string(obj.preview),
    'published': lambda obj: stringify(obj.published),
    'replies': lambda obj: object_or_string(obj.replies),
    'startTime': lambda obj: stringify(obj.startTime),
    'summary': lambda obj: stringify(obj.summary),
    'tag': lambda obj: object_or_string(obj.tag),
    'to': lambda obj: object_or_string(obj.to),
    'type': lambda obj: stringify(obj.type),
    'updated': lambda obj: stringify(obj.updated),
    'url': lambda obj: object_or_string(obj.url),
}

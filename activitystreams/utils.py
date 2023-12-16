"""
Utility functions for managing activitystreams data
"""

from datetime import datetime
from collections.abc import Iterable

# used for mapping jsonld @ keys to proper names
KEYMAP = {'abase': '@base',
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


def dt_str_convert(value: datetime) -> str:
    """
    Converts a datetime.datetime to an ActivityStreams datetime string
    """
    return value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def serialize(value) -> str:
    """
    Serializes an ActivityStreams Object and returns the string
    :param value: the object to be serialized into a string
    :return: the string value of the object
    """
    return value.serialize()

VALUEMAP = {
    datetime: dt_str_convert,
}
# Iterables should be turned into a json Array that iterates over every value,
# processes it with the relevant function from the VALUEMAP (or str as a
# default), and then concatenated together
VALUEMAP.update({Iterable: lambda value: \
    f'[{",".join(VALUEMAP.get(type(item), str)(item) for item in value)}]'})

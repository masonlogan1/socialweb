"""
Utility functions for managing activitystreams data
"""

from datetime import datetime
from collections.abc import Iterable
from itertools import chain

# used for mapping jsonld @ keys to proper names
JSON_LD_KEYMAP = {'abase': '@base',
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


def datetime_convert(value: datetime) -> str:
    """
    Converts a datetime.datetime to an ActivityStreams datetime string
    """
    return value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

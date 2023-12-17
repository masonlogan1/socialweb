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


class PropertyAnalyzerMixin:
    """
    Class that provides a __get_properties__ method and __properties__ variable
    to anything it is added to
    """

    def __init__(self):
        self.__get_properties__()

    @classmethod
    def __get_properties__(cls) -> list:
        """
        Creates a list of all @property objects defined and inherited in
        this class
        """
        cls.__properties__ = list(chain(key for kls in cls.mro()
                                        for key, value in kls.__dict__.items()
                                        if isinstance(value, property)))
        return cls.__properties__

    def __getattr__(self, key):
        if key not in self.__dict__.keys():
            if key != '__properties__':
                raise AttributeError(
                    f"'{self.__class__.__name__}' object has no attribute '{key}'")
            # if __properties__ does not exist, create it
            self.__properties__ = self.__get_properties__()
        return self.__dict__[key]

"""
Classes used to add specific functionality to their inheritors
"""
from datetime import datetime
from itertools import chain
import re

DATETIME_REGEX = re.compile('\d{4}-\d{2}-\d{2}T[012]\d:\d{2}:\d{2}Z')

def is_activity_datetime(val):
    return isinstance(val, datetime) or \
        re.search(DATETIME_REGEX, val) is not None

def parse_activitystream_datetime(val):
    if val is None:
        return None
    return val if isinstance(val, datetime) else \
        datetime.strptime(val, '%Y-%m-%dT%H:%M:%SZ')

class PropertyAnalyzerMixin:
    """
    Class that provides a __get_properties__ method to produce a tuple for
    Classes and a __properties__ variable to instances of inheriting classes
    """

    def __init__(self):
        self.__properties__ = self.__get_properties__()

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

"""
Classes used to add specific functionality to their inheritors
"""
import logging
import re
from collections.abc import Iterable
from datetime import datetime
from types import NoneType
from urllib import parse

from activitypy.activitystreams.utils import VALID_URL_REGEX

logger = logging.getLogger('activitystreams_model')
logger.setLevel(logging.INFO)

DATETIME_REGEX = re.compile('\d{4}-\d{2}-\d{2}T[012]\d:\d{2}:\d{2}Z')


def is_class(val, classes: Iterable, functional: bool = False):
    """
    Checks if the value is an instance of the provided classes
    """
    classes = classes if functional else (*classes, list)
    return isinstance(val, classes)


def is_activity_datetime(val, prop='', **kwargs):
    if isinstance(val, NoneType):
        return
    if not isinstance(val, (datetime, str)):
        raise ValueError(
            f'Property "{prop}" must be of type "datetime" or "str" ' +
            f'got {val} ({type(val)})')
    if isinstance(val, str) and re.search(DATETIME_REGEX, val) is None:
        raise ValueError(
            f'Property "{prop}" must be in "YYYY-mm-dd-THH:MM:SSZ" format; ' +
            f'got {val} ({type(val)})')


def parse_activitystream_datetime(val):
    if val is None:
        return None
    return val if isinstance(val, datetime) else \
        datetime.strptime(val, '%Y-%m-%dT%H:%M:%SZ')


def url_validator(url, secure: bool = False, skip_none=False, **kwargs):
    """
    Checks a provided URL to ensure it meets a handful of basic criteria for
    being a valid internet URL
    :param url: URL to validate
    :param secure: whether to accept only HTTPS urls
    :return: url if valid
    """
    if url is None and skip_none:
        return url
    pieces = parse.urlparse(url)
    if not pieces.scheme or pieces.scheme not in ['http', 'https']:
        raise ValueError('Cannot dereference url without valid scheme; add ' +
                         f'''{'"http://" or' if not secure else ''} ''' +
                         '"https://" to url')
    # urls must have a body
    if not pieces.netloc:
        raise ValueError('Cannot dereference url without body')
    # urls can only have certain characters
    if re.match(VALID_URL_REGEX, pieces.netloc):
        raise ValueError('url cannot contain characters outside of' +
                         'alphanumeric (a-Z, 0-9), "-", "_", ":", and "."')
    # secure connections MUST use https
    if secure and pieces.scheme != 'https':
        raise ValueError('Cannot dereference non-"https://" url when ' +
                         'secure=True; set secure=False or change scheme')
    return url


def is_nonnegative(val, prop='', **kwargs):
    if val is None:
        return
    if val < 0:
        raise ValueError(f'Property "{prop}" must be greater than 0; ' +
                         f'got {val}')


def evaluate_value(val, types: Iterable, prop: str,
                   functional: bool = False, additional=tuple(), **kwargs):
    # convert types to tuple to avoid issues with generators
    types = set(types)
    types = types if functional and list not in types else (set(types)|{list})
    if not isinstance(val, tuple(types)):
        raise ValueError(f"Property '{prop}' must be one of: ('" +
                         f'''{"', '".join(t.__name__ for t in types 
                                          if t != NoneType)}') ''' +
                         f'got "{val}" {type(val)}')
    if isinstance(val, (list, tuple, set)):
        # we should rerun the process on each of the values if the value is a
        # list, tuple, or set
        return [evaluate_value(v, types=types, prop=prop, functional=functional,
                               additional=additional, **kwargs)
                for v in val]
    for f in additional:
        # additional validation functions can be passed in but need to be
        # able to accept types, property, and functional as keyword args
        f(val, types=types, prop=prop, functional=functional, **kwargs)
    logger.debug(f'setting {prop} to {val}')
    return val


class ModelManager:
    """
    Class for making it easier to call models by their names, primarily used
    as a way of producing classes for the PropValidator class
    """
    # the way the import system works makes it difficult to implement type
    # checking. this class tries to fix that by making it possible to register
    # the objects to a class-level variable
    __classes = {}

    def register_class(self, cls):
        self.__classes[cls.__name__] = cls

    def __getitem__(self, names):
        if isinstance(names, str):
            return self.__classes.get(names, None)
        return tuple(self.__classes.get(name, None) for name in names
                if self.__classes.get(name, None))
MODELS = ModelManager()


class PropValidator:
    """
    Decorator class for managing property setters. Takes a set of valid types,
    a property name, whether the property is functional (can be a list), and
    any additional validation functions to run along with any keyword args that
    should be provided as input to the additional validators
    """

    def __init__(self, types: Iterable, functional: bool = False,
                 additional=tuple(), none_allowed = True, **kwargs):
        # allows us to pass object names as strings to avoid an issue where
        # we would be referencing a class type before it has been "created"
        self.types = set(types) if isinstance(types, Iterable) else {types}
        self.functional = functional
        self.additional = additional
        self.kwargs = kwargs
        if none_allowed:
            self.types = self.types | {NoneType}

    def check(self, set_prop, *args, **kwargs):
        # prop_func should be a SETTER
        def check_val(obj, val, *args, **kwargs):
            types = [MODELS[t] if isinstance(t, str) else t for t in self.types]
            set_prop(obj, evaluate_value(val, types=types,
                                         prop=set_prop.__name__,
                                         functional=self.functional,
                                         additional=self.additional,
                                         **self.kwargs))
        return check_val

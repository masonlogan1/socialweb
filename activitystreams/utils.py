"""
Utility functions for managing activitystreams data
"""
import logging
from collections.abc import Iterable

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# TODO: this logic needs to be moved into the base class for property objects

# matches a data type to a function
STRINGIFY_MAP = {
    float: float,
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

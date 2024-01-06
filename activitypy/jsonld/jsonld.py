"""
Tools for working with json-ld data
"""
import json
import logging
from collections.abc import Iterable
from itertools import chain
from numbers import Number
from typing import Union

from pyld.jsonld import expand

from activitypy.jsonld.utils import JSON_LD_KEYMAP, JSON_TYPE_MAP, \
    DEFAULT_TYPE, DEFAULT_CONTEXT
from activitypy.jsonld.base import PropertyAwareObject
from activitypy.jsonld.json_output import PropertyJsonGenerator
from activitypy.jsonld.json_input import PropertyJsonIntake

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PropertyJsonLD(PropertyJsonGenerator, PropertyJsonIntake):
    """
    Class for representing JSON-LD data. Utilizes @property objects for pulling
    instance data into JSON text representation
    """
    # overridable dict for mapping a transformation function to a property
    default_transforms = {}
    # overridable dict for mapping class types to a function for loading them
    # as objects
    type_constructor_map = {}

    def __init__(self, acontext):
        PropertyJsonGenerator.__init__(self, acontext)
        PropertyJsonIntake.__init__(self, acontext)

    def __str__(self):
        return self.json()


class ApplicationActivityJson(PropertyJsonLD):
    """
    Base class for representing application/activity+json type objects
    """

    def __init__(self, acontext):
        super().__init__(acontext=acontext)

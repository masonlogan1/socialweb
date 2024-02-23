"""
Module for separating logic for generating objects from JSON-LD input
"""
import json
import logging
from collections.abc import Iterable
from itertools import chain
from numbers import Number
from typing import Union

from pyld.jsonld import expand

from activitypy.jsonld.engine.utils import DEFAULT_CONTEXT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PropertyJsonIntake:
    """
    Base class for taking in jsonld data and populating relevant @property
    attributes with the content
    """

    @property
    def class_registry(self):
        # object should not be directly set, rather it dict should be updated.
        # the triple-underscore helps obscure this from some ides, which
        # makes reading the debugger a lot easier
        if not hasattr(self, '___class_registry___'):
            self.___class_registry___ = dict()
        return self.___class_registry___

    @property
    def property_registry(self):
        if not hasattr(self, '___property_registry___'):
            self.___property_registry___ = dict()
        return self.___property_registry___

    def _get_object_class(self, data, classmap=None):
        """
        If the data has a recognized @type value (after json-ld expansion) then
        returns the class registered to the given @type. Returns None otherwise
        :param data: json-ld data to examine
        :param classmap: additional type-class mappings outside the registry
        :return: object fitting the type or None
        """
        expanded = expand(data)
        if len(expanded) < 1:
            # if the list is empty, assume it is because there are no values
            # provided other than @context and id, which produces an empty list
            expanded = [{'@context': DEFAULT_CONTEXT}]
        expanded = expanded[0]
        class_type = expanded.get('@type', [''])[0]
        if not class_type:
            logger.debug(f'No @type value provided:\n{expanded}')

        # check that the @type value is in the mapping
        classmap = {**self.class_registry, **(classmap if classmap else {})}
        if class_type not in classmap.keys():
            # if the class type is not in our mapping, use the default value
            logger.debug(f'@type value not in mapping: "{class_type}"')
            class_type = 'default'

        # gets the class for the object that needs to be created from the
        object_class = classmap.get(class_type)
        if not object_class:
            ValueError(f'Provided data has invalid or missing "@type"')
        return object_class

    def _unpack_objects(self, data, context, classmap: dict = None):
        """
        Recursively unpacks a piece of data into flat values, lists (arrays),
        and linked objects
        :param data: the data to evaluate
        :param context: the json-ld context this is being performed under
        :param classmap: type-class mapping outside the typical registry
        :return: flat value, python object, or list
        """
        # if the value is a basic type (str, bool, or number) then return the
        # raw value, we don't need to handle those in a special way
        if data is None or isinstance(data, (Number, str, bool)):
            return data
        if isinstance(data, dict):
            # treat a nested dictionary like a linked object
            # context has to be appended to read objects individually
            context_val = {'@context': context, **data}

            # if there is no @type value in the expanded form, assume this is
            # just supposed to be a regular dictionary
            type = expand(context_val)
            if len(type) < 1 or type[0].get('@type', None) is None:
                return {key: self._unpack_objects(val, context, classmap)
                        for key, val in data.items()}

            if self._get_object_class(context_val, classmap=classmap):
                return self.from_json(context_val)
            return None
        if isinstance(data, Iterable):
            # turn iterables into lists and evaluate everything inside
            return [self._unpack_objects(item, context, classmap)
                    for item in data]

    def from_json(self, data: Union[str, dict], classmap: dict = None):
        """
        Extracts fields from the provided JSON. Uses the @type value to
        determine the type of object to be created.
        :param data: JSON data to transform into Python object
        :param classmap: additional class mappings to use for conversion
        :return: Python object
        """
        # convert to dict and expand
        data = json.loads(data) if isinstance(data, str) else data.copy()
        context = data.get('@context', DEFAULT_CONTEXT)
        if not data.get('@context', None):
            logger.debug(f"No '@context' provided, using '{DEFAULT_CONTEXT}'")
            data.update({'@context': DEFAULT_CONTEXT})
        object_class = self._get_object_class(data, classmap=classmap)

        # only include values from the json that are properties of the class
        # unpack data structures and populate None values where appropriate
        filtered_data = {
            key: self._unpack_objects(data.get(key, None), context,
                                     classmap=classmap)
            for key in object_class.__get_properties__()
        }

        return object_class(**{**filtered_data, 'acontext': context})

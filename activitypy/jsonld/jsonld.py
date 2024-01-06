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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# These are separate methods to ensure existing types are not accidentally
# overwritten; there are already so many that it's easy to mess up
def register_jsonld_type(name: str, cls: object):
    """
    Adds a name-class mapping to the JSON_TYPE_MAP
    :param name: the fully qualified namespace id to associate with the class
    :param cls: the new object class
    :
    """
    logger.info(f'Registering jsonld type "{name}" as {cls.__name__}')
    if name in JSON_TYPE_MAP.keys():
        raise ValueError(f'"{name}" already exists in mapping, cannot add new')
    JSON_TYPE_MAP.update({name: cls})


def update_jsonld_type(name: str, cls: object):
    """
    Updates an existing mapping to the JSON_TYPE_MAP
    :param name: the fully qualified namespace id associated with the class
    :param cls: the new object class
    :return: previous class
    :raises ValueError: if the name is not already in the mapping
    """
    logger.info(f'Updating jsonld type "{name}" to "{cls.__name__}"')
    if name not in JSON_TYPE_MAP.keys():
        raise ValueError(f'"{name}" not in mapping yet, cannot update')
    prior = JSON_TYPE_MAP.get(name)
    JSON_TYPE_MAP.update({name: cls})
    return prior


def remove_jsonld_type(name: str) -> object:
    """
    Removes an existing mapping from the JSON_TYPE_MAP
    :param name: the fully qualified namespace id of the class
    :return: removed class or None if it was not found
    """
    if name in JSON_TYPE_MAP.keys():
        logger.info(f'Removing jsonld type "{name}"')
        return JSON_TYPE_MAP.pop(name)
    logger.info(f'Cannot remove jsonld type "{name}", does not exist')
    return JSON_TYPE_MAP.pop(name, None)


class AContext:
    __acontext = None

    @property
    def acontext(self):
        return self.__acontext

    @acontext.setter
    def acontext(self, value):
        self.__acontext = value


class PropertyJsonLD(PropertyAwareObject, AContext):
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
        super().__init__()
        self.acontext = acontext

    def data(self, include: Iterable = (), exclude: Iterable = (),
             transforms: dict = None, rename: dict = None, include_none=False,
             reject_values: Iterable = ()) -> dict:
        """
        Returns the object's properties as a dictionary. Does not include values
        that are not a property of the object
        :param include: properties to include, defaults to all
        :param exclude: properties to exclude, defaults to none
        :param transforms: dict that maps data transformations by property name
        :param rename: dict that renames properties in the output dict
        :param include_none: includes pairs where value is None (defaults False)
        :param reject_values: values to refuse to include
        :return: dictionary of properties
        """
        transforms = {**self.default_transforms,
                      **(transforms if transforms else {})}
        rename = {**JSON_LD_KEYMAP, **(rename if rename else {})}
        data = {
            # change name of property, if provided in mapping
            rename.get(prop, prop):
            # change value (BY UNMAPPED NAME) with function, if provided
                transforms.get(prop, lambda o: getattr(o, prop))(self)
            for prop in self.__properties__
            # if include_null is True or the property is not None
            if (include_none or getattr(self, prop) is not None)
               # AND if including everything OR if specifically included
               and (not include or prop in include)
               # AND if excluding nothing OR if not specifically excluded
               and not (exclude and prop in exclude)
               and getattr(self, prop) not in reject_values}
        # second pass of the None filter to ensure anything that returned None
        # after being passed through a function is also captured. Removing the
        # first pass results in a recursion error. I do not understand why but
        # would love a solution
        return {key: val for key, val in data.items()
                if (include_none or val is not None)}

    def json(self, include: Iterable = (), exclude: Iterable = (),
             transforms: dict = None, rename: dict = None, include_none=False,
             minified: bool = False, indent: int = None) -> str:
        """
        Transforms the object into a json string
        :param include: properties to include, defaults to all
        :param exclude: properties to exclude, defaults to none
        :param transforms: dict that maps data transformations by property name
        :param rename: dict that renames properties in the output dict
        :param include_none: includes pairs where value is None (defaults False)
        :param minified: removes as much whitespace as possible in the output
        :param indent: indentation level; usually for readability
        :return:
        """
        separators = (',', ':') if minified else None
        return json.dumps(self.data(include=include, exclude=exclude,
                                    transforms=transforms, rename=rename,
                                    include_none=include_none),
                          separators=separators,
                          indent=indent)

    @staticmethod
    def _get_object_class(data, classmap=None):
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
            logger.warning(f'No @type value provided:\n{expanded}')

        # check that the @type value is in the mapping
        classmap = {**JSON_TYPE_MAP, **(classmap if classmap else {})}
        if class_type not in classmap.keys():
            # if the class type is not in our mapping, use the default value
            logger.warning(f'@type value not in mapping: "{class_type}"')
            class_type = 'default'

        # gets the class for the object that needs to be created from the
        object_class = classmap.get(class_type)
        if not object_class:
            ValueError(f'Provided data has invalid or missing "@type"')
        return object_class

    @classmethod
    def _unpack_objects(cls, data, context, classmap: dict = None):
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
                return {key: cls._unpack_objects(val, context, classmap)
                        for key, val in data.items()}

            if cls._get_object_class(context_val, classmap=classmap):
                return cls.from_json(context_val)
            return None
        if isinstance(data, Iterable):
            # turn iterables into lists and evaluate everything inside
            return [cls._unpack_objects(item, context, classmap)
                    for item in data]

    @classmethod
    def from_json(cls, data: Union[str, dict], classmap: dict = None):
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
            logger.warning(f"No '@context' provided, using '{DEFAULT_CONTEXT}'")
            data.update({'@context': DEFAULT_CONTEXT})
        object_class = cls._get_object_class(data, classmap=classmap)

        # only include values from the json that are properties of the class
        # unpack data structures and populate None values where appropriate
        filtered_data = {
            key: cls._unpack_objects(data.get(key, None), context,
                                     classmap=classmap)
            for key in object_class.__get_properties__()
        }

        return object_class(**{**filtered_data, 'acontext': context})

    def __str__(self):
        return self.json()


class ApplicationActivityJson(PropertyJsonLD):
    """
    Base class for representing application/activity+json type objects
    """

    def __init__(self, acontext):
        super().__init__(acontext=acontext)

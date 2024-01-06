"""
Module for separating out logic for generating json text output
"""
import json
from collections.abc import Iterable

from activitypy.jsonld.utils import JSON_LD_KEYMAP
from activitypy.jsonld.base import PropertyAwareObject


class PropertyJsonGenerator(PropertyAwareObject):
    """
    Base class for generating json output based on the @property attributes
    of implementing objects
    """
    default_transforms = {}
    __acontext = None

    # jsonld requires an @context attribute
    @property
    def acontext(self):
        """
        JSON-LD processing context
        """
        return self.__acontext

    @acontext.setter
    def acontext(self, value):
        self.__acontext = value

    def __init__(self, acontext, *args, **kwargs):
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
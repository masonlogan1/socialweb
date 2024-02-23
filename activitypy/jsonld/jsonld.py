"""
Tools for working with json-ld data
"""
import logging
import json
from collections.abc import Iterable

from activitypy.jsonld.base import PropertyAwareObject
from activitypy.jsonld.utils import JSON_LD_KEYMAP, JSON_DATA_CONTEXT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PropertyJsonLD(PropertyAwareObject):
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
        PropertyAwareObject.__init__(self)
        self.acontext = acontext

    def __str__(self):
        return self.json()

    @property
    def acontext(self):
        """
        JSON-LD processing context
        """
        return self.__acontext

    @acontext.setter
    def acontext(self, value):
        self.__acontext = value

    def data(self, include: Iterable = (), exclude: Iterable = (),
             transforms: dict = None, rename: dict = None, include_none=False,
             reject_values: Iterable = (), context=JSON_DATA_CONTEXT) -> dict:
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
        # TODO: reimplement automatic unpacking of iterables
        #   Special handling during json unpacking should be written in a
        #   getter function, with the exception of iterables (which we should
        #   handle here, putting "isinstance(obj, (list, tuple,...))" in each
        #   property will get messy FAST)
        with self.switch_context(context) as process_context:
            transforms = {**self.default_transforms,
                          **(transforms if transforms else {})}
            rename = {**JSON_LD_KEYMAP, **(rename if rename else {})}
            data = {
                # change name of property, if provided in mapping
                rename.get(prop, prop): getattr(self, prop, None)
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
                                    include_none=include_none,
                                    context=JSON_DATA_CONTEXT),
                          separators=separators,
                          indent=indent)


class ApplicationActivityJson(PropertyJsonLD):
    """
    Base class for representing application/activity+json type objects
    """
    # an object's namespace determines what engine it should be processed by.
    # generally speaking, an engine should stamp objects it generates with the
    # namespaces that were used to generate it; objects themselves should NOT
    # be messing with this, it could cause an object to become unusable

    def __init__(self, acontext):
        super().__init__(acontext=acontext)

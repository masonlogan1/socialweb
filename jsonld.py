"""
Tools for working with json-ld data
"""
import json
from collections.abc import Iterable
from itertools import chain


JSON_LD_KEYMAP = {
          'abase': '@base',
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


class PropertyObject:
    """
    Base object that provides tools for working with object properties.
    Provides a __get_properties__ method to produce a tuple for classes and a
    __properties__ variable to instances of inheriting classes
    """

    def __init__(self):
        self.__properties__ = self.__get_properties__()

    def __iter__(self):
        for prop in self.__properties__:
            yield prop, getattr(self, prop)

    def __getitem__(self, keys):
        keys = [keys] if isinstance(keys, str) else keys
        if any(key not in self.__properties__ for key in keys):
            bad_keys = [key for key in keys if key not in self.__properties__]
            raise KeyError(f'''Key{'s' if len(bad_keys) > 1 else ''} ''' +
                           f'''('{"', '".join(bad_keys)}') ''' +
                           f'''not in type '{self.__class__.__name__}\'''')
        return {key: getattr(self, key) for key in keys}

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


class AContext:
    __acontext = None

    @property
    def acontext(self):
        return self.__acontext

    @acontext.setter
    def acontext(self, value):
        self.__acontext = value


class JsonLD(PropertyObject, AContext):
    """
    Class for representing JSON-LD data. Utilizes @property objects for pulling
    instance data into JSON text representation
    """
    default_transforms = {}

    def __init__(self, acontext):
        super().__init__()
        self.acontext = acontext

    def data(self, include: Iterable = (), exclude: Iterable = (),
             transforms: dict = None, rename: dict = None, include_none=False,
             reject_values: Iterable = ()) -> dict:
        """
        Returns the object's properties as a dictionary. Cannot include values
        that are not already a property of the object
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
        return data

    def json(self, include: Iterable = (), exclude: Iterable = (),
             transforms: dict = None, rename: dict = None, include_none=False,
             minified: bool = False) -> str:
        separators = (',', ':') if minified else None
        return json.dumps(self.data(include=include, exclude=exclude,
                                    transforms=transforms, rename=rename,
                                    include_none=include_none),
                          separators=separators)

    def __str__(self):
        return self.json()

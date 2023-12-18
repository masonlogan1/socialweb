"""
Classes used to add specific functionality to their inheritors
"""
from itertools import chain
from json import JSONEncoder


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


class PropertyJsonEncoder(JSONEncoder):
    """
    Class for generating json strings for objects based on their properties
    """

    def __init__(self, skipkeys=False, ensure_ascii=True, check_circular=True,
                 allow_nan=True, sort_keys=False, indent=None, separators=None,
                 default=None):
        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
                         check_circular=check_circular, allow_nan=allow_nan,
                         sort_keys=sort_keys, indent=indent,
                         separators=separators, default=default)

    def json(self, obj, transforms: dict = None, rename: dict = None, *args,
                include = tuple(), exclude = ('acontext',), **kwargs):
        """
        Serializes objects based on their properties. Can utilize a dict of
        transform functions to apply specific functions to specific properties.
        Will map property names to alternatives by the rename dict.
        """
        transforms = transforms if transforms else {}
        rename = rename if rename else {}
        f = lambda obj: {rename.get(prop, prop):
                    transforms.get(prop, lambda o: getattr(o, prop))(obj)
                for prop in obj.__properties__
                # if the property is not None
                if getattr(obj, prop) is not None
                # AND if including everything OR if specifically included
                and (not include or prop in include)
                # AND if excluding nothing OR if not specifically excluded
                and not (exclude and prop in exclude)}
        # TODO: create an internal context manager to handle this
        previous_default = self.default
        self.default = f
        json_str = self.encode(obj)
        self.default = previous_default
        return json_str

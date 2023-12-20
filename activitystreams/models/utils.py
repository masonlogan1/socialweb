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

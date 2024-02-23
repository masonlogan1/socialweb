from collections.abc import Iterable
from types import NoneType


def evaluate_value(val, types: Iterable, prop: str,
                   functional: bool = False, additional=tuple(), **kwargs):
    # convert types to tuple to avoid issues with generators
    types = set(types)
    types = types if functional and list not in types else (set(types) | {list})
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
    return val


class SetterValidator:
    """
    Decorator class for managing property setters. Takes a set of valid types,
    a property name, whether the property is functional (can be a list), and
    any additional validation functions to run along with any keyword args that
    should be provided as input to the additional validators
    """

    def __init__(self, types: Iterable, functional: bool = False,
                 additional=tuple(), none_allowed=True, **kwargs):
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
            set_prop(obj, evaluate_value(val, types=self.types,
                                         prop=set_prop.__name__,
                                         functional=self.functional,
                                         additional=self.additional,
                                         **self.kwargs))

        return check_val
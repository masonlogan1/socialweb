"""
Module for splitting logic that allows objects to iterate and work with
@property objects stored inside of them
"""
import logging
from copy import copy
from itertools import chain

from activitypy.jsonld.utils import JSON_TYPE_MAP

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class JsonContextAwareManager:
    """
    Class for managing the context in which a @property is being modified or
    retrieved
    """

    def __init__(self):
        self.context = None
        self.active = False

    def __call__(self, context=None, *args, **kwargs):
        self.context = context
        return self

    def __enter__(self):
        self.active = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context = None
        self.active = False


class ContextualProperty(property):
    """
    Expanded version of the property class that allows objects to get, set, and
    delete properties based on the context of the object that has contextual
    properties
    """

    def __NO_GETTER(self, *args, **kwargs):
        raise AttributeError(f"""can't get attribute{
        "'"+self.__name+"'" if self.__name else ''}""")

    def __NO_SETTER(self, *args, **kwargs):
        raise AttributeError(f"""can't set attribute{
        "'"+self.__name+"'" if self.__name else ''}""")

    def __NO_DELETER(self, *args, **kwargs):
        raise AttributeError(f"""can't delete attribute{
        "'"+self.__name+"'" if self.__name else ''}""")

    def __init__(self, fget=None, fset=None, fdel=None, doc=None, name=None):
        self.__name = name
        self.__fget_contexts = {None: fget or self.__NO_GETTER}
        self.__fset_contexts = {None: fset or self.__NO_SETTER}
        self.__fdel_contexts = {None: fdel or self.__NO_DELETER}

        # replaces functions with wrappers that determine what actually gets
        # called based on the owning object's __context__
        super().__init__(
            fget=self.__fget,
            fset=self.__fset,
            fdel=self.__fdel,
            doc=doc
        )

    @staticmethod
    def get_context(obj):
        # gets the context of the object; returns default for
        # JsonContextAwareManager if the object does not have __context__
        return getattr(obj, '__context__', JsonContextAwareManager()).context

    def __fget(self, obj):
        """
        Grabs the correct getter function based on object context and returns
        the result of the getter
        :param obj: the object to retrieve data from
        :return: the context-dependent data
        """
        # if the context is not recognized, revert to None so we get the default
        # function
        context = self.get_context(obj)
        return self.__fget_contexts.get(
            context if context in self.__fget_contexts.keys() else None)(obj)

    def __fset(self, obj, val):
        """
        Sets the value of the given object to the given value using the
        appropriate function under the given context
        :param obj: object to modify
        :param val: incoming value to set
        """
        context = self.get_context(obj)
        return self.__fset_contexts.get(
            context if context in self.__fset_contexts.keys() else None)(obj, val)

    def __fdel(self, obj):
        """
        Deletes the property using the function appropriate under the given
        object's context
        :param obj: object to delete the property from
        """
        context = self.get_context(obj)
        return self.__fdel_contexts.get(
            context if context in self.__fdel_contexts.keys() else None)(obj)

    def setter(self, fset):
        """
        Changes the default setter function for the property. Should be used
        as a decorator
        :param fset: new default setter function
        :return:
        """
        prop = copy(self)
        prop.__fset_contexts[None] = fset
        return prop

    def getter(self, fget):
        """
        Changes the default getter function for the property. Should be used
        as a decorator
        :param fget: new default getter function
        :return:
        """
        prop = copy(self)
        prop.__fget_contexts[None] = fget
        return prop

    def deleter(self, fdel):
        """
        Changes the default deleter function for the property. Should be used
        as a decorator
        :param fdel: new default deleter function
        :return:
        """
        prop = copy(self)
        prop.__fdel_contexts[None] = fdel
        return prop

    def setter_context(self, context):
        """
        Decorator for adding a context-dependent setter to the property. The
        function will be used when the __context__ attribute of the property
        matches the identifying value of the contextual function
        :param context: identifier for the contextual function
        """
        def decorator(fn):
            self.__fset_contexts[context] = fn
            return self
        return decorator

    def getter_context(self, context):
        """
        Decorator for adding a context-dependent getter to the property. The
        function will be used when the __context__ attribute of the property
        matches the identifying value of the contextual function
        :param context: identifier for the contextual function
        """
        def decorator(fn):
            self.__fget_contexts[context] = fn
            return self
        return decorator

    def deleter_context(self, context):
        """
        Decorator for adding a context-dependent deleter to the property. The
        function will be used when the __context__ attribute of the property
        matches the identifying value of the contextual function
        :param context: identifier for the contextual function
        """
        def decorator(fn):
            self.__fdel_contexts[context] = fn
            return self
        return decorator

    def __copy__(self):
        new_prop = ContextualProperty(doc=self.__doc__)
        new_prop.__fget_contexts = self.__fget_contexts.copy()
        new_prop.__fset_contexts = self.__fset_contexts.copy()
        new_prop.__fdel_contexts = self.__fdel_contexts.copy()
        return new_prop


def contextualproperty(fn) -> ContextualProperty:
    """
    Wrapper function that allows for @contextualproperty decorators
    without needlessly complex code in the actual object. The doc property will
    be derived from the docstring of the getter function.
    :param fn: getter function that serves as a starting point for the property
    :return: ContextualProperty with a getter and documentation, if provided
    """
    # there are ways to make this part of the class but I'm not doing it. I
    # have spent way too much time making this thing work and I am not about to
    # drive myself insane over this one design choice.
    return ContextualProperty(fget=fn, doc=fn.__doc__)


class JsonProperty:
    """
    Base object for managing properties that can be registered to a class.
    Supports one and only one property.
    """

    # This class is useless on its own, it needs to be inherited by a class that
    # implements a single @property value. The primary use for this is so that
    # object derived from PropertyAwareObject can register new properties,
    # allowing for extensions and on-the-fly class modification when handling
    # JSONLD structures that utilize aspects from multiple schemas.

    def __init__(self):
        self.__property_name__ = self.__get_property_name__()
        self.__registration__ = self.__get_registration__()

    def __getattr__(self, item):
        if item == '__registration__' and not hasattr(self, '__registration__'):
            self.__registration__ = self.__get_registration__()
            return self.__registration__
        if item not in self.__dict__.keys():
            raise ValueError(f"'{self.__class__.__name__}' has no " +
                             f"attribute '{item}'")
        return self.__dict__[item]

    @classmethod
    def __get_property_name__(cls, refresh=False):
        """
        Locates the name of the property. Will raise a value error if more or
        less than one property is present.
        :param refresh:
        :return:
        """
        if not hasattr(cls, '__property_name__') or refresh:
            prop = [key for key, value in cls.__dict__.items()
                    if isinstance(value, property)]
            # the registration process only supports ONE property per class;
            # this is intentional
            if len(prop) != 1:
                raise ValueError(f'"JsonProperty" objects must have one and ' +
                                 f'only one property, found {len(prop)} for ' +
                                 f'{cls.__name__}')
            cls.__property_name__ = prop[0]
        return cls.__property_name__

    @classmethod
    def __get_registration__(cls, refresh=False):
        """
        Retrieves all necessary info to register the property of this class
        onto another class and stores it in self.__registration__
        :param refresh:
        :return:
        """
        if not hasattr(cls, '__property_name__') or refresh:
            cls.__property_name__ = cls.__get_property_name__(refresh=True)
        # caches the registration for ease of use
        if not hasattr(cls, '__registration__') or refresh:
            prop = getattr(cls, cls.__property_name__, None)
            if prop:
                cls.__registration__ = (prop.fget, prop.fset, prop.fdel,
                                        prop.__doc__)
            else:
                cls.__registration__ = None
        return cls.__registration__


class PropertyAwareObject:
    """
    Base object that provides tools for working with object properties.
    Provides a __get_properties__ method to produce a tuple for classes and a
    __properties__ variable to instances of inheriting classes
    """

    def __init__(self):
        self.__properties__ = self.__get_properties__()
        self.__context__ = JsonContextAwareManager()

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
    def __get_properties__(cls, refresh=False):
        """
        Creates a list of all @property objects defined and inherited in
        this class
        """
        if not hasattr(cls, '__properties__') or refresh:
            # we cache a copy
            cls.__properties__ = tuple(chain(key for kls in cls.mro()
                                             for key, value in
                                             kls.__dict__.items()
                                             if isinstance(value, property)))
        return cls.__properties__


# These are separate methods to ensure existing types are not accidentally
# overwritten; there are already so many that it's easy to mess up
def register_property(property_class, object_class):
    if JsonProperty not in property_class.mro():
        raise TypeError('Cannot register non-JsonProperty class to ' +
                        'PropertyAwareObject class; got ' +
                        f'{property_class.__class__.__name__}')
    if PropertyAwareObject not in object_class.mro():
        raise TypeError('Cannot register JsonProperty class to non-' +
                        'PropertyAwareObject object; got ' +
                        f'{object_class.__class__.__name__}')
    setattr(object_class, property_class.__get_property_name__(),
            property(*property_class.__get_registration__()))


def update_property(property_class, object_class):
    if JsonProperty not in property_class.mro():
        raise TypeError('Cannot register non-JsonProperty class to ' +
                        'PropertyAwareObject class; got ' +
                        f'{property_class.__class__.__name__}')
    if PropertyAwareObject not in object_class.mro():
        raise TypeError('Cannot register JsonProperty class to non-' +
                        'PropertyAwareObject object; got ' +
                        f'{object_class.__class__.__name__}')
    setattr(object_class, property_class.__get_property_name__(),
            property(*property_class.__get_registration__()))


def remove_property(property_name: str, object_class):
    if PropertyAwareObject not in object_class.mro():
        raise TypeError('Cannot alter registration of non-' +
                        'PropertyAwareObject object; got ' +
                        f'{object.__class__.__name__}')
    delattr(object_class, property_name)


def register_jsonld_type(name: str, cls: object):
    """
    Adds a name-class mapping to the JSON_TYPE_MAP
    :param name: the fully qualified namespace id to associate with the class
    :param cls: the new object class
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

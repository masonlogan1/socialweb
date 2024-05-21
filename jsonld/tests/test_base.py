from unittest import TestCase, main


class ContextualPropertyConstructor(TestCase):
    """
    Tests for the methods a ContextualProperty can be created
    """


class ContextualPropertyGetter(TestCase):
    """
    Tests to ensure that a ContextualProperty's getter and getter_context
    work as expected
    """


class ContextualPropertySetter(TestCase):
    """
    Tests to ensure that a ContextualProperty's setter and setter_context
    work as expected
    """


class ContextualPropertyDeleter(TestCase):
    """
    Tests to ensure that a ContextualProperty's deleter and deleter_context
    work as expected
    """


class ContextualPropertyFunction(TestCase):
    """
    Tests to ensure that the contextualproperty function works as a simplified
    decorator for creating contextualproperty objects on classes
    """


class NamespacedObjectConstructor(TestCase):
    """
    Tests to ensure that the NamespacedObject constructor works as expected
    """


class NamespacedObjectGetters(TestCase):
    """
    Tests to ensure that the NamespacedObject has a __namespace__ attribute,
    that instances of NamespacedObject can access this attribute's getters,
    that the __get_namespace__ class function does not work on the
    base object, that an overriding class can properly assign itself a
    namespace, and that attempting to access the NamespacedObject in the
    JSON_DATA_CONTEXT will return nothing
    """


class NamespacedObjectSetters(TestCase):
    """
    Tests to ensure that the NamespacedObject __namespace__ setter can change
    the class namespace
    """


class JsonContextAwareManagerTests(TestCase):
    """
    Tests to ensure that a JsonContextAwareManager can be used as a context
    manager to create a stack of last-in-first-out context values. Each
    nested context manager should add a new value to the top of the stack
    and when the context manager exits it should remove the associated
    context value.
    """


class JsonPropertyTests(TestCase):
    """
    Tests that a JsonProperty object will automatically pick up a single
    @property (or similarly derived object) from an implementing class,
    set the __property_name__, set the __registration__, and that the
    __get_registration__ and __set_registration__ methods work independently
    """


class PropertyAwareObjectConstructor(TestCase):
    """
    Tests that a PropertyAwareObject constructor can automatically pick up
    the names of all associated properties and create a JsonContextAwareManager
    """


class PropertyAwareObjectIterator(TestCase):
    """
    Tests that when a PropertyAwareObject is iterated over, it yields
    name-property pairs of all properties in the object
    """


class PropertyAwareObjectGetitem(TestCase):
    """
    Tests that when a PropertyAwareObject is accessed with indexes it will
    return a dictionary mapping property names to their properties, and that
    if a value in the indexes is not a valid property it will raise a
    KeyError
    """


if __name__ == '__main__':
    main()

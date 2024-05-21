from unittest import TestCase, main


class ContextualPropertyConstructor(TestCase):
    """
    Tests for the methods a ContextualProperty can be created
    """

    def test_name_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the
        name argument and have __name set
        """

    def test_fget_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the
        fget argument and have __fget set and the get method added to the
        __fget_contexts
        """

    def test_fset_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the
        fset argument and have __fset set and the set method added to the
        __fset_contexts
        """

    def test_fdel_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the
        fdel argument and have __fdel set and the del method added to the
        __fdel_contexts
        """

    def test_doc_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the doc
        argument and that the property's __doc__ method returns the provided
        text
        """

    def test_fget_fset(self):
        """
        Tests that a ContextualProperty can be constructed with the fget and
        fset arguments, that the __fget and __fset functions will perform their
        actions using the correct functions, and that __fget_contexts and
        __fset_contexts contain the functions
        """

    def test_fset_fdel(self):
        """
        Tests that a ContextualProperty can be constructed with the fset and
        fdel arguments, that the __fset and __fdel functions will perform their
        actions using the correct functions, and that __fset_contexts and
        __fdel_contexts contain the functions
        """

    def test_fget_fdel(self):
        """
        Tests that a ContextualProperty can be constructed with the fget and
        fdel arguments, that the __fget and __fdel functions will perform their
        actions using the correct functions, and that __fget_contexts and
        __fdel_contexts contain the functions
        """

    def test_fget_fset_fdel(self):
        """
        Tests that a ContextualProperty can be constructed with all three
        function arguments, __fget/__fset/__fdel methods perform their
        actions using the correct functions, and that the context dicts
        contain the functions
        """

    def test_fget_fset_fdel_doc(self):
        """
        Tests that a ContextualProperty can be constructed with all three
        function arguments, __fget/__fset/__fdel methods perform their
        actions using the correct functions, that the context dicts contain
        the functions, and that the doc has been set
        """

    def test_fget_fset_fdel_doc_name(self):
        """
        Tests that a ContextualProperty can be constructed with all three
        function arguments, __fget/__fset/__fdel methods perform their
        actions using the correct functions, that the context dicts contain
        the functions, and that the doc and name have been set
        """


class ContextualPropertyGetter(TestCase):
    """
    Tests to ensure that a ContextualProperty's getter and getter_context
    work as expected
    """
    def test_fget_default_only(self):
        """
        Tests that when a ContextualProperty only has the initially provided
        getter function it will execute that function
        """

    def test_fget_one_additional_context(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected
        """

    def test_fget_multiple_additional_contexts(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected
        """

    def test_fget_nonexistent_context_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty getter is used with a nonexistent
        context, a MissingContextError is raised
        """

    def test_no_fget_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty has no getter, an AttributeError
        is raised with a message matching the default from property
        """


class ContextualPropertySetter(TestCase):
    """
    Tests to ensure that a ContextualProperty's setter and setter_context
    work as expected
    """
    def test_fset_default_only(self):
        """
        Tests that when a ContextualProperty only has the initially provided
        getter function it will execute that function
        """

    def test_fset_one_additional_context(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected
        """

    def test_fset_multiple_additional_contexts(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected
        """

    def test_fset_nonexistent_context_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty getter is used with a nonexistent
        context, a MissingContextError is raised
        """

    def test_no_fset_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty has no getter, an AttributeError
        is raised with a message matching the default from property
        """


class ContextualPropertyDeleter(TestCase):
    """
    Tests to ensure that a ContextualProperty's deleter and deleter_context
    work as expected
    """
    def test_fdel_default_only(self):
        """
        Tests that when a ContextualProperty only has the initially provided
        getter function it will execute that function
        """

    def test_fdel_one_additional_context(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected
        """

    def test_fdel_multiple_additional_contexts(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected
        """

    def test_fdel_nonexistent_context_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty getter is used with a nonexistent
        context, a MissingContextError is raised
        """

    def test_no_fdel_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty has no getter, an AttributeError
        is raised with a message matching the default from property
        """


class ContextualPropertyFunction(TestCase):
    """
    Tests to ensure that the contextualproperty function works as a simplified
    decorator for creating contextualproperty objects on classes
    """

    def test_decorator(self):
        """
        Tests that when the contextualproperty function is used as a decorator,
        it will create a new ContextualProperty on a class
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

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
        assert False

    def test_fget_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the
        fget argument and have __fget set and the get method added to the
        __fget_contexts
        """
        assert False

    def test_fset_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the
        fset argument and have __fset set and the set method added to the
        __fset_contexts
        """
        assert False

    def test_fdel_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the
        fdel argument and have __fdel set and the del method added to the
        __fdel_contexts
        """
        assert False

    def test_doc_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the doc
        argument and that the property's __doc__ method returns the provided
        text
        """
        assert False

    def test_fget_fset(self):
        """
        Tests that a ContextualProperty can be constructed with the fget and
        fset arguments, that the __fget and __fset functions will perform their
        actions using the correct functions, and that __fget_contexts and
        __fset_contexts contain the functions
        """
        assert False

    def test_fset_fdel(self):
        """
        Tests that a ContextualProperty can be constructed with the fset and
        fdel arguments, that the __fset and __fdel functions will perform their
        actions using the correct functions, and that __fset_contexts and
        __fdel_contexts contain the functions
        """
        assert False

    def test_fget_fdel(self):
        """
        Tests that a ContextualProperty can be constructed with the fget and
        fdel arguments, that the __fget and __fdel functions will perform their
        actions using the correct functions, and that __fget_contexts and
        __fdel_contexts contain the functions
        """
        assert False

    def test_fget_fset_fdel(self):
        """
        Tests that a ContextualProperty can be constructed with all three
        function arguments, __fget/__fset/__fdel methods perform their
        actions using the correct functions, and that the context dicts
        contain the functions
        """
        assert False

    def test_fget_fset_fdel_doc(self):
        """
        Tests that a ContextualProperty can be constructed with all three
        function arguments, __fget/__fset/__fdel methods perform their
        actions using the correct functions, that the context dicts contain
        the functions, and that the doc has been set
        """
        assert False

    def test_fget_fset_fdel_doc_name(self):
        """
        Tests that a ContextualProperty can be constructed with all three
        function arguments, __fget/__fset/__fdel methods perform their
        actions using the correct functions, that the context dicts contain
        the functions, and that the doc and name have been set
        """
        assert False


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
        assert False

    def test_fget_one_additional_context(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected
        """
        assert False

    def test_fget_multiple_additional_contexts(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected
        """
        assert False

    def test_fget_nonexistent_context_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty getter is used with a nonexistent
        context, a MissingContextError is raised
        """
        assert False

    def test_no_fget_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty has no getter, an AttributeError
        is raised with a message matching the default from property
        """
        assert False


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
        assert False

    def test_fset_one_additional_context(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected
        """
        assert False

    def test_fset_multiple_additional_contexts(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected
        """
        assert False

    def test_fset_nonexistent_context_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty getter is used with a nonexistent
        context, a MissingContextError is raised
        """
        assert False

    def test_no_fset_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty has no getter, an AttributeError
        is raised with a message matching the default from property
        """
        assert False


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
        assert False

    def test_fdel_one_additional_context(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected
        """
        assert False

    def test_fdel_multiple_additional_contexts(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected
        """
        assert False

    def test_fdel_nonexistent_context_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty getter is used with a nonexistent
        context, a MissingContextError is raised
        """
        assert False

    def test_no_fdel_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty has no getter, an AttributeError
        is raised with a message matching the default from property
        """
        assert False


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
        assert False


class NamespacedObjectConstructor(TestCase):
    """
    Tests to ensure that the NamespacedObject constructor works as expected
    """

    # there's really no defined constructor, so we just need to make sure an
    # object CAN be created
    def test_standard_constructor(self):
        """
        Tests a constructor without an assigned namespace to ensure the
        object can be created
        """
        assert False


class NamespacedObjectGetters(TestCase):
    """
    Tests to ensure that the NamespacedObject has a __namespace__ attribute,
    that instances of NamespacedObject can access this attribute's getters,
    that the __get_namespace__ class function does not work on the
    base object, that an overriding class can properly assign itself a
    namespace, and that attempting to access the NamespacedObject in the
    JSON_DATA_CONTEXT will return nothing
    """

    def test_namespace_standard_context(self):
        """
        Tests that an object implementing get_namespace works as expected
        """
        assert False

    def test_no_namespace(self):
        """
        Test that an object without a namespace produces a None value
        """
        assert False

    def test_json_data_context_namespace(self):
        """
        Test that an object with the JSON_DATA_CONTEXT context returns None as
        its namespace
        """
        assert False


class NamespacedObjectSetters(TestCase):
    """
    Tests to ensure that the NamespacedObject __namespace__ setter can change
    the class namespace
    """

    def test_namespace_change_outside_class_change_context(self):
        """
        Tests that a namespace value cannot be changed outside the
        class change context
        """
        assert False

    def test_namespace_change_with_class_change_context(self):
        """
        Tests that when an object is in the class change context, the
        namespace value can be changed
        """
        assert False

    def test_namespace_reset_on_delete(self):
        """
        Tests that when the namespace property is deleted, it does not remove
        the namespace entirely but rather resets it to the default for that
        class (reverses changes done under class change context)
        """
        assert False


class JsonContextAwareManagerTests(TestCase):
    """
    Tests to ensure that a JsonContextAwareManager can be used as a context
    manager to create a stack of last-in-first-out context values. Each
    nested context manager should add a new value to the top of the stack
    and when the context manager exits it should remove the associated
    context value.
    """

    def test_json_context_constructor(self):
        """
        Tests that a context manager can be constructed and has an
        active context, an active flag, and an empty stack
        """
        assert False

    def test_json_context_callable_adds_to_stack(self):
        """
        Tests that a json context manager can be called to add a new item to
        the stop of the stack, but does not set the active flag
        """
        assert False

    def test_json_context_aware_manager_single_context(self):
        """
        Tests that when a JsonContextAwareManager is called and used as a
        context manager, it automatically sets the provided value as the new
        context, adds it to the stack, and marks the active flag; also tests
        that when the context manager ends, the stack is empty, context is None,
        and the active flag is unset
        """
        assert False

    def test_json_context_aware_manager_nested_contexts(self):
        """
        Tests that when the same JsonContextAwareManager is used as a context
        manager in a nested way, the last applied context will be the active
        context, the stack will be in the correct order, and the active flag
        will be set; also tests that when the context manager ends at each
        level, the active context is returned to the next item on the stack
        and the active flag remains marked until the stack is completely empty
        """
        assert False


class JsonPropertyTests(TestCase):
    """
    Tests that a JsonProperty object will automatically pick up a single
    @property (or similarly derived object) from an implementing class,
    set the __property_name__, set the __registration__, and that the
    __get_registration__ and __set_registration__ methods work independently
    """

    def test_get_property_name(self):
        """
        Tests that __get_property_name__ will return the name of a single
        property, raise a ValueError if more or less than one property is
        present, will cache the name in __property_name__, and will refresh
        the cache if refresh == True
        """
        assert False

    def test_get_registration(self):
        """
        Tests that __get_registration__ will return a 4-tuple of values
        containing the fget, fset, fdel, and doc properties of the property
        identified by cls.__property_name__, will cache the registration in
        __registration__, and will refresh the cache if refresh == True
        """
        assert False

    def test_constructor_single_property(self):
        """
        Tests that a JsonProperty object with a single property will
        successfully instantiate, pick up the property name, and create
        the registration from the property's getter/setter/deleter/doc
        """
        assert False

    def test_constructor_multiple_properties(self):
        """
        Tests that a JsonProperty object with multiple properties will
        raise a ValueError
        """
        assert False

    def test_constructor_no_properties(self):
        """
        Tests that a JsonProperty object with no properties will raise a
        ValueError
        """
        assert False


class PropertyAwareObjectConstructor(TestCase):
    """
    Tests that a PropertyAwareObject constructor can automatically pick up
    the names of all associated properties and create a JsonContextAwareManager
    """

    def test_get_properties(self):
        """
        Tests that __get_properties__ will return the names of all properties
        """
        assert False

    def test_construction_without_additional_properties(self):
        """
        Tests that a PropertyAwareObject can be created even when no
        properties are found
        """
        assert False

    def test_construction_with_one_property(self):
        """
        Tests that a PropertyAwareObject can be created and pick up the
        details for a single property
        """
        assert False

    def test_constructor_with_multiple_properties(self):
        """
        Test that a PropertyAwareObject ccan be created and pick up the
        details for multiple properties
        """
        assert False

    def test_constructor_context_manager(self):
        """
        Test that a PropertyAwareObject has a context manager when created
        """
        assert False


class PropertyAwareObjectIterator(TestCase):
    """
    Tests that when a PropertyAwareObject is iterated over, it yields
    name-property pairs of all properties in the object
    """

    def test_iterator_with_no_properties(self):
        """
        Tests that a PropertyAwareObject can be iterated over without throwing
        an exception when no properties are present
        """
        assert False

    def test_iterator_with_one_property(self):
        """
        Tests that a PropertyAwareObject can be iterated over when a single
        property is present
        """
        assert False

    def test_iterator_with_multiple_properties(self):
        """
        Tests that a PropertyAwareObject can be iterated over when multiple
        properties are present
        """
        assert False


class PropertyAwareObjectGetitem(TestCase):
    """
    Tests that when a PropertyAwareObject is accessed with indexes it will
    return a dictionary mapping property names to their properties, and that
    if a value in the indexes is not a valid property it will raise a
    KeyError
    """

    def test_get_nonexistent_property(self):
        """
        Tests that when a single invalid key is used as an index on a
        PropertyAwareObject, it will raise a KeyError
        """
        assert False

    def test_get_multiple_nonexistent_properties(self):
        """
        Tests that when multiple invalid keys are used as indexes on a
        PropertyAwareObject, it will raise a KeyError
        """
        assert False

    def test_get_single_property(self):
        """
        Tests that a PropertyAwareObject returns a dictionary with a single
        key-value pair matching the requested property
        """
        assert False

    def test_get_multiple_properties(self):
        """
        Tests that a PropertyAwareObject returns a dictionary with multiple
        key-value pairs matching the requested properties
        """
        assert False

    def test_get_multiple_properties_some_nonexistent(self):
        """
        Tests that even if some properties are present, a KeyError is raised
        if any of the indexes are not present
        """
        assert False


if __name__ == '__main__':
    main()

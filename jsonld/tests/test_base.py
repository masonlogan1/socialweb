from unittest import TestCase, main
from unittest.mock import patch, MagicMock

from jsonld import base
from jsonld.base import NamespacedObject, JsonContextAwareManager
from jsonld.exceptions import MissingContextError
from jsonld.utils import CLASS_CHANGE_CONTEXT, JSON_DATA_CONTEXT


class ContextualPropertyConstructor(TestCase):
    """
    Tests for the methods a ContextualProperty can be created
    """

    def test_name_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the
        name argument and have __name set
        """
        sample_name = 'sample_name'

        prop = base.ContextualProperty(name=sample_name)

        # check the name matches
        self.assertEqual(getattr(prop, '_ContextualProperty__name', 'bad_name'),
                         sample_name)

        # check that fget, fset, and fdel use their fallback functions
        empty_fget_contexts = {None: prop._ContextualProperty__NO_GETTER}
        empty_fset_contexts = {None: prop._ContextualProperty__NO_SETTER}
        empty_fdel_contexts = {None: prop._ContextualProperty__NO_DELETER}
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fget_contexts', {}),
            empty_fget_contexts
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fset_contexts', {}),
            empty_fset_contexts
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fdel_contexts', {}),
            empty_fdel_contexts
        )

    def test_fget_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the
        fget argument and have __fget set and the get method added to the
        __fget_contexts
        """
        sample_fget = MagicMock()
        sample_input = MagicMock()

        prop = base.ContextualProperty(fget=sample_fget)

        # check that the fget contexts dict has our function mapped to None
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fget_contexts', {}),
            {None: sample_fget}
        )

        # check that when __fget is run, the provided fget is used by default
        prop._ContextualProperty__fget(sample_input)
        sample_fget.assert_called_once_with(sample_input)

        # check that fset and fdel use their fallback functions
        empty_fset_contexts = {None: prop._ContextualProperty__NO_SETTER}
        empty_fdel_contexts = {None: prop._ContextualProperty__NO_DELETER}
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fset_contexts', {}),
            empty_fset_contexts
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fdel_contexts', {}),
            empty_fdel_contexts
        )

    def test_fset_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the
        fset argument and have __fset set and the set method added to the
        __fset_contexts
        """
        sample_fset = MagicMock()
        sample_input_obj = MagicMock()
        sample_input_val = MagicMock()

        prop = base.ContextualProperty(fset=sample_fset)

        # check that the fset contexts dict has our function mapped to None
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fset_contexts', {}),
            {None: sample_fset}
        )

        # check that when __fget is run, the provided fget is used by default
        prop._ContextualProperty__fset(sample_input_obj, sample_input_val)
        sample_fset.assert_called_once_with(sample_input_obj, sample_input_val)

        # check that fget and fdel use their fallback functions
        empty_fget_contexts = {None: prop._ContextualProperty__NO_GETTER}
        empty_fdel_contexts = {None: prop._ContextualProperty__NO_DELETER}
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fget_contexts', {}),
            empty_fget_contexts
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fdel_contexts', {}),
            empty_fdel_contexts
        )

    def test_fdel_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the
        fdel argument and have __fdel set and the del method added to the
        __fdel_contexts
        """
        sample_fdel = MagicMock()
        sample_input = MagicMock()

        prop = base.ContextualProperty(fdel=sample_fdel)

        # check that the fdel contexts dict has our function mapped to None
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fdel_contexts', {}),
            {None: sample_fdel}
        )

        # check that when __fdel is run, the provided fdel is used by default
        prop._ContextualProperty__fdel(sample_input)
        sample_fdel.assert_called_once_with(sample_input)

        # check that fget and fset use their fallback functions
        empty_fget_contexts = {None: prop._ContextualProperty__NO_GETTER}
        empty_fset_contexts = {None: prop._ContextualProperty__NO_SETTER}
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fget_contexts', {}),
            empty_fget_contexts
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fset_contexts', {}),
            empty_fset_contexts
        )

    def test_doc_only(self):
        """
        Tests that a ContextualProperty can be constructed with only the doc
        argument and that the property's __doc__ method returns the provided
        text
        """
        sample_doc = 'sample doc sample doc sample doc'

        prop = base.ContextualProperty(doc=sample_doc)

        # check the name matches
        self.assertEqual(prop.__doc__, sample_doc)

        # check that fget, fset, and fdel use their fallback functions
        empty_fget_contexts = {None: prop._ContextualProperty__NO_GETTER}
        empty_fset_contexts = {None: prop._ContextualProperty__NO_SETTER}
        empty_fdel_contexts = {None: prop._ContextualProperty__NO_DELETER}
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fget_contexts', {}),
            empty_fget_contexts
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fset_contexts', {}),
            empty_fset_contexts
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fdel_contexts', {}),
            empty_fdel_contexts
        )

    def test_fget_fset(self):
        """
        Tests that a ContextualProperty can be constructed with the fget and
        fset arguments, that the __fget and __fset functions will perform their
        actions using the correct functions, and that __fget_contexts and
        __fset_contexts contain the functions
        """
        sample_fget = MagicMock()
        sample_fget_input = MagicMock()

        sample_fset = MagicMock()
        sample_fset_input_obj = MagicMock()
        sample_fset_input_val = MagicMock()

        prop = base.ContextualProperty(fget=sample_fget, fset=sample_fset)

        # check that the fget contexts dict has our function mapped to None
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fget_contexts', {}),
            {None: sample_fget}
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fset_contexts', {}),
            {None: sample_fset}
        )

        # check that when __fget is run, the provided fget is used by default
        prop._ContextualProperty__fget(sample_fget_input)
        sample_fget.assert_called_once_with(sample_fget_input)
        # check that when __fset is run, the provided fset is used by default
        prop._ContextualProperty__fset(
            sample_fset_input_obj, sample_fset_input_val
        )
        sample_fset.assert_called_once_with(
            sample_fset_input_obj, sample_fset_input_val
        )

        # check that fdel uses its fallback function
        empty_fdel_contexts = {None: prop._ContextualProperty__NO_DELETER}
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fdel_contexts', {}),
            empty_fdel_contexts
        )

    def test_fset_fdel(self):
        """
        Tests that a ContextualProperty can be constructed with the fset and
        fdel arguments, that the __fset and __fdel functions will perform their
        actions using the correct functions, and that __fset_contexts and
        __fdel_contexts contain the functions
        """
        sample_fset = MagicMock()
        sample_fset_input_obj = MagicMock()
        sample_fset_input_val = MagicMock()

        sample_fdel = MagicMock()
        sample_fdel_input = MagicMock()

        prop = base.ContextualProperty(fset=sample_fset, fdel=sample_fdel)

        # check that the fget contexts dict has our function mapped to None
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fset_contexts', {}),
            {None: sample_fset}
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fdel_contexts', {}),
            {None: sample_fdel}
        )

        # check that when __fset is run, the provided fset is used by default
        prop._ContextualProperty__fset(
            sample_fset_input_obj, sample_fset_input_val
        )
        sample_fset.assert_called_once_with(
            sample_fset_input_obj, sample_fset_input_val
        )
        # check that when __fdel is run, the provided fdel is used by default
        prop._ContextualProperty__fdel(sample_fdel_input)
        sample_fdel.assert_called_once_with(sample_fdel_input)

        # check that fget uses its fallback function
        empty_fget_contexts = {None: prop._ContextualProperty__NO_GETTER}
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fget_contexts', {}),
            empty_fget_contexts
        )

    def test_fget_fdel(self):
        """
        Tests that a ContextualProperty can be constructed with the fget and
        fdel arguments, that the __fget and __fdel functions will perform their
        actions using the correct functions, and that __fget_contexts and
        __fdel_contexts contain the functions
        """
        sample_fget = MagicMock()
        sample_fget_input = MagicMock()

        sample_fdel = MagicMock()
        sample_fdel_input = MagicMock()

        prop = base.ContextualProperty(fget=sample_fget, fdel=sample_fdel)

        # check that the fget contexts dict has our function mapped to None
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fget_contexts', {}),
            {None: sample_fget}
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fdel_contexts', {}),
            {None: sample_fdel}
        )

        # check that when __fget is run, the provided fget is used by default
        prop._ContextualProperty__fget(sample_fget_input)
        sample_fget.assert_called_once_with(sample_fget_input)
        # check that when __fdel is run, the provided fdel is used by default
        prop._ContextualProperty__fdel(sample_fdel_input)
        sample_fdel.assert_called_once_with(sample_fdel_input)

        # check that fset uses its fallback function
        empty_fset_contexts = {None: prop._ContextualProperty__NO_SETTER}
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fset_contexts', {}),
            empty_fset_contexts
        )

    def test_fget_fset_fdel(self):
        """
        Tests that a ContextualProperty can be constructed with all three
        function arguments, __fget/__fset/__fdel methods perform their
        actions using the correct functions, and that the context dicts
        contain the functions
        """
        sample_fget = MagicMock()
        sample_fget_input = MagicMock()

        sample_fset = MagicMock()
        sample_fset_input_obj = MagicMock()
        sample_fset_input_val = MagicMock()

        sample_fdel = MagicMock()
        sample_fdel_input = MagicMock()

        prop = base.ContextualProperty(fget=sample_fget, fset=sample_fset,
                                       fdel=sample_fdel)

        # check that the fget contexts dict has our function mapped to None
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fget_contexts', {}),
            {None: sample_fget}
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fset_contexts', {}),
            {None: sample_fset}
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fdel_contexts', {}),
            {None: sample_fdel}
        )

        # check that when __fget is run, the provided fget is used by default
        prop._ContextualProperty__fget(sample_fget_input)
        sample_fget.assert_called_once_with(sample_fget_input)
        # check that when __fset is run, the provided fset is used by default
        prop._ContextualProperty__fset(
            sample_fset_input_obj, sample_fset_input_val
        )
        sample_fset.assert_called_once_with(
            sample_fset_input_obj, sample_fset_input_val
        )
        # check that when __fdel is run, the provided fdel is used by default
        prop._ContextualProperty__fdel(sample_fdel_input)
        sample_fdel.assert_called_once_with(sample_fdel_input)

    def test_fget_fset_fdel_doc(self):
        """
        Tests that a ContextualProperty can be constructed with all three
        function arguments, __fget/__fset/__fdel methods perform their
        actions using the correct functions, that the context dicts contain
        the functions, and that the doc has been set
        """
        sample_fget = MagicMock()
        sample_fget_input = MagicMock()

        sample_fset = MagicMock()
        sample_fset_input_obj = MagicMock()
        sample_fset_input_val = MagicMock()

        sample_fdel = MagicMock()
        sample_fdel_input = MagicMock()

        sample_doc = 'sample_doc sample_doc sample_doc'

        prop = base.ContextualProperty(fget=sample_fget, fset=sample_fset,
                                       fdel=sample_fdel, doc=sample_doc)

        self.assertEqual(prop.__doc__, sample_doc)

        # check that the fget contexts dict has our function mapped to None
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fget_contexts', {}),
            {None: sample_fget}
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fset_contexts', {}),
            {None: sample_fset}
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fdel_contexts', {}),
            {None: sample_fdel}
        )

        # check that when __fget is run, the provided fget is used by default
        prop._ContextualProperty__fget(sample_fget_input)
        sample_fget.assert_called_once_with(sample_fget_input)
        # check that when __fset is run, the provided fset is used by default
        prop._ContextualProperty__fset(
            sample_fset_input_obj, sample_fset_input_val
        )
        sample_fset.assert_called_once_with(
            sample_fset_input_obj, sample_fset_input_val
        )
        # check that when __fdel is run, the provided fdel is used by default
        prop._ContextualProperty__fdel(sample_fdel_input)
        sample_fdel.assert_called_once_with(sample_fdel_input)

    def test_fget_fset_fdel_doc_name(self):
        """
        Tests that a ContextualProperty can be constructed with all three
        function arguments, __fget/__fset/__fdel methods perform their
        actions using the correct functions, that the context dicts contain
        the functions, and that the doc and name have been set
        """
        sample_fget = MagicMock()
        sample_fget_input = MagicMock()

        sample_fset = MagicMock()
        sample_fset_input_obj = MagicMock()
        sample_fset_input_val = MagicMock()

        sample_fdel = MagicMock()
        sample_fdel_input = MagicMock()

        sample_doc = 'sample_doc sample_doc sample_doc'

        sample_name = 'sample name'

        prop = base.ContextualProperty(fget=sample_fget, fset=sample_fset,
                                       fdel=sample_fdel, doc=sample_doc,
                                       name=sample_name)

        self.assertEqual(prop.__doc__, sample_doc)

        self.assertEqual(
            getattr(prop, '_ContextualProperty__name', ''), sample_name
        )

        # check that the fget contexts dict has our function mapped to None
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fget_contexts', {}),
            {None: sample_fget}
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fset_contexts', {}),
            {None: sample_fset}
        )
        self.assertEqual(
            getattr(prop, '_ContextualProperty__fdel_contexts', {}),
            {None: sample_fdel}
        )

        # check that when __fget is run, the provided fget is used by default
        prop._ContextualProperty__fget(sample_fget_input)
        sample_fget.assert_called_once_with(sample_fget_input)
        # check that when __fset is run, the provided fset is used by default
        prop._ContextualProperty__fset(
            sample_fset_input_obj, sample_fset_input_val
        )
        sample_fset.assert_called_once_with(
            sample_fset_input_obj, sample_fset_input_val
        )
        # check that when __fdel is run, the provided fdel is used by default
        prop._ContextualProperty__fdel(sample_fdel_input)
        sample_fdel.assert_called_once_with(sample_fdel_input)


class ContextualPropertyGetter(TestCase):
    """
    Tests to ensure that a ContextualProperty's getter and getter_context
    work as expected
    """
    def test_fget_default_only(self):
        """
        Tests that when a ContextualProperty only has the initially provided
        getter function it will execute that function. Creates the property
        by using the constructor
        """
        # returns the .attr attribute of whatever is passed in
        getter_fn = lambda obj: obj.attr

        sample_value = 'sample_value'
        context_mock = MagicMock(context=None)
        obj = MagicMock(attr=sample_value, __context__=context_mock)

        prop = base.ContextualProperty(fget=getter_fn)
        prop.getter_context('other context'),

        result = prop.fget(obj)

        self.assertEqual(result, sample_value)

    def test_fget_default_only_decorator(self):
        """
        Tests that when a ContextualProperty only has the initially provided
        getter function it will execute that function. Creates the property
        using the decorator
        """
        default_val = 'default_val'

        class TestClass:
            @base.ContextualProperty
            def attr(self):
                return default_val

        sample = TestClass()

        self.assertEqual(sample.attr, default_val)

    def test_fget_one_additional_context(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected.
        Creates the property by using the constructor
        """
        getter_fn = lambda obj: obj.attr0
        alt_getter_1 = lambda obj: obj.attr1

        sample_attr0 = 'sample_value 0'
        sample_attr1 = 'sample_value 1'
        context_mock = MagicMock(context=None)
        obj = MagicMock(attr0=sample_attr0, attr1=sample_attr1,
                        __context__=context_mock)

        prop = base.ContextualProperty(fget=getter_fn)
        prop.getter_context('alt context 1')(alt_getter_1)

        # test default
        result = prop.fget(obj)
        self.assertEqual(result, sample_attr0)

        #test alt context 1
        context_mock.context = 'alt context 1'
        result = prop.fget(obj)
        self.assertEqual(result, sample_attr1)

    def test_fget_one_additional_context_decorator(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected.
        Creates the property by using the decorator
        """
        default_val = 'default val'
        context_val_0 = 'context value 0'

        context_0 = 'context_0'

        class TestClass:
            __context__ = MagicMock(context=None)
            @base.ContextualProperty
            def attr(self):
                return default_val

            @attr.getter_context(context_0)
            def attr(self):
                return context_val_0

        sample = TestClass()

        # test default
        self.assertEqual(sample.attr, default_val)

        # test alt context 1
        sample.__context__.context = context_0
        self.assertEqual(sample.attr, context_val_0)


    def test_fget_multiple_additional_contexts(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected.
        Creates the property by using the constructor
        """
        getter_fn = lambda obj: obj.attr0
        alt_getter_1 = lambda obj: obj.attr1
        alt_getter_2 = lambda obj: obj.attr2

        sample_attr0 = 'sample_value 0'
        sample_attr1 = 'sample_value 1'
        sample_attr2 = 'sample_value 2'
        context_mock = MagicMock(context=None)
        obj = MagicMock(attr0=sample_attr0, attr1=sample_attr1,
                        attr2=sample_attr2, __context__=context_mock)

        prop = base.ContextualProperty(fget=getter_fn)
        prop.getter_context('alt context 1')(alt_getter_1)
        prop.getter_context('alt context 2')(alt_getter_2)

        # test default
        result = prop.fget(obj)
        self.assertEqual(result, sample_attr0)

        # test alt context 1
        context_mock.context = 'alt context 1'
        result = prop.fget(obj)
        self.assertEqual(result, sample_attr1)

        # test alt context 2
        context_mock.context = 'alt context 2'
        result = prop.fget(obj)
        self.assertEqual(result, sample_attr2)

    def test_fget_multiple_additional_contexts_decorator(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected.
        Creates the property by using the decorator
        """
        default_val = 'default val'
        context_val_0 = 'context value 0'
        context_val_1 = 'context value 1'

        context_0 = 'context_0'
        context_1 = 'context_1'

        class TestClass:
            __context__ = MagicMock(context=None)

            @base.ContextualProperty
            def attr(self):
                return default_val

            @attr.getter_context(context_0)
            def attr(self):
                return context_val_0

            @attr.getter_context(context_1)
            def attr(self):
                return context_val_1

        sample = TestClass()

        # test default
        self.assertEqual(sample.attr, default_val)

        # test alt context 0
        sample.__context__.context = context_0
        self.assertEqual(sample.attr, context_val_0)

        # test alt context 1
        sample.__context__.context = context_1
        self.assertEqual(sample.attr, context_val_1)

    def test_fget_nonexistent_context_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty getter is used with a nonexistent
        context and no default, a MissingContextError is raised. Creates the
        property by using the constructor
        """
        alt_getter_1 = lambda obj: obj.attr1
        sample_attr1 = 'sample_value 1'
        context_mock = MagicMock(context=None)

        obj = MagicMock(attr1=sample_attr1, __context__=context_mock)

        prop = base.ContextualProperty(name='test_prop')
        prop.getter_context('alt context 1')(alt_getter_1)

        # test that registered contexts can be accessed
        context_mock.context = 'alt context 1'
        result = prop.fget(obj)
        self.assertEqual(result, sample_attr1)

        # nonexistent context
        context_mock.context = 'bad context'
        msg = ("ContextualProperty has no default getter for 'test_prop' " +
               "and is missing context 'bad context'")
        with self.assertRaises(MissingContextError, msg=msg):
            result = prop.fget(obj)

    def test_no_fget_raises_MissingContextError(self):
        """
        Tests that when a ContextualProperty has no getter, an AttributeError
        is raised with a message matching the default from property. Creates
        the property by using the constructor
        """
        context_mock = MagicMock(context=None)
        obj = MagicMock(__context__=context_mock)

        prop = base.ContextualProperty()
        msg = "ContextualProperty has no default getter"
        with self.assertRaises(MissingContextError, msg=msg):
            result = prop.fget(obj)

        prop = base.ContextualProperty(name='test_prop')
        msg = "ContextualProperty has no default getter for 'test_prop'"
        with self.assertRaises(MissingContextError, msg=msg):
            result = prop.fget(obj)


class ContextualPropertySetter(TestCase):
    """
    Tests to ensure that a ContextualProperty's setter and setter_context
    work as expected
    """
    def test_fset_default_only(self):
        """
        Tests that when a ContextualProperty only has the initially provided
        getter function it will execute that function. Creates the property
        by using the constructor
        """
        setter_fn = lambda obj, val: setattr(obj, 'attr', val)

        context_mock = MagicMock(context=None)
        obj = MagicMock(attr='', __context__=context_mock)

        prop = base.ContextualProperty(fset=setter_fn)

        # test default
        sample_value = 'val0.'
        expected_value = sample_value
        result = prop.fset(obj, sample_value)
        self.assertEqual(obj.attr, expected_value)

    def test_fset_default_only_decorator(self):
        """
        Tests that when a ContextualProperty only has the initially provided
        getter function it will execute that function. Creates the property
        by using the decorator
        """

        class TestClass:
            __context__ = MagicMock(context=None)

            @base.contextualproperty
            def attr(self):
                return getattr(self, '_attr', None)

            @attr.setter
            def attr(self, val):
                setattr(self, '_attr', val)

        sample = TestClass()

        # test default
        default_val = 'default value'
        expected_value = default_val
        sample.attr = default_val
        self.assertEqual(sample.attr, expected_value)

    def test_fset_one_additional_context(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected.
        Creates the property by using the constructor
        """
        setter_fn = lambda obj, val: setattr(obj, 'attr', val)
        alt_setter_1 = lambda obj, val: setattr(obj, 'attr', f'{val}1')

        context_mock = MagicMock(context=None)
        obj = MagicMock(attr='', __context__=context_mock)

        prop = base.ContextualProperty(fset=setter_fn)
        prop.setter_context('alt context 1')(alt_setter_1)

        # test default
        sample_value = 'val0.'
        expected_value = sample_value
        result = prop.fset(obj, sample_value)
        self.assertEqual(obj.attr, expected_value)

        # test alt context 1
        context_mock.context = 'alt context 1'
        sample_value = 'val0.'
        expected_value = 'val0.1'
        result = prop.fset(obj, sample_value)
        self.assertEqual(obj.attr, expected_value)

    def test_fset_one_additional_context_decorator(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected.
        Creates the property by using the decorator
        """

        context_0 = 'context_0'

        class TestClass:
            __context__ = MagicMock(context=None)

            @base.contextualproperty
            def attr(self):
                return getattr(self, '_attr', None)

            @attr.setter
            def attr(self, val):
                setattr(self, '_attr', val)

            @attr.setter_context(context_0)
            def attr(self, val):
                setattr(self, '_attr', val+'_0')

        sample = TestClass()

        # test default
        default_val = 'default value'
        expected_value = default_val
        sample.attr = default_val
        self.assertEqual(sample.attr, expected_value)

        # test alt context 1
        sample.__context__.context = context_0
        context_val_0 = 'context value'
        expected_value = context_val_0 + '_0'
        sample.attr = context_val_0
        self.assertEqual(sample.attr, expected_value)

    def test_fset_multiple_additional_contexts(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected.
        Creates the property by using the constructor
        """
        setter_fn = lambda obj, val: setattr(obj, 'attr', val)
        alt_setter_1 = lambda obj, val: setattr(obj, 'attr', f'{val}1')
        alt_setter_2 = lambda obj, val: setattr(obj, 'attr', f'{val}2')

        context_mock = MagicMock(context=None)
        obj = MagicMock(attr='', __context__=context_mock)

        prop = base.ContextualProperty(fset=setter_fn)
        prop.setter_context('alt context 1')(alt_setter_1)
        prop.setter_context('alt context 2')(alt_setter_2)

        # test default
        sample_value = 'val'
        expected_value = sample_value
        result = prop.fset(obj, sample_value)
        self.assertEqual(obj.attr, expected_value)

        # test alt context 1
        context_mock.context = 'alt context 1'
        sample_value = 'val'
        expected_value = 'val1'
        result = prop.fset(obj, sample_value)
        self.assertEqual(obj.attr, expected_value)

        # test alt context 2
        context_mock.context = 'alt context 2'
        sample_value = 'val'
        expected_value = 'val2'
        result = prop.fset(obj, sample_value)
        self.assertEqual(obj.attr, expected_value)

    def test_fset_multiple_additional_contexts_decorator(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected.
        Creates the property by using the decorator
        """
        context_0 = 'context_0'
        context_1 = 'context_1'

        class TestClass:
            __context__ = MagicMock(context=None)

            @base.contextualproperty
            def attr(self):
                return getattr(self, '_attr', None)

            @attr.setter
            def attr(self, val):
                setattr(self, '_attr', val)

            @attr.setter_context(context_0)
            def attr(self, val):
                setattr(self, '_attr', val + '_0')

            @attr.setter_context(context_1)
            def attr(self, val):
                setattr(self, '_attr', val + '_1')

        sample = TestClass()

        # test default
        default_val = 'default value'
        expected_value = default_val
        sample.attr = default_val
        self.assertEqual(sample.attr, expected_value)

        # test alt context 0
        sample.__context__.context = context_0
        context_val_0 = 'context value'
        expected_value = context_val_0 + '_0'
        sample.attr = context_val_0
        self.assertEqual(sample.attr, expected_value)

        # test alt context 1
        sample.__context__.context = context_1
        context_val_1 = 'context value'
        expected_value = context_val_1 + '_1'
        sample.attr = context_val_1
        self.assertEqual(sample.attr, expected_value)

    def test_fset_nonexistent_context_raises_MissingContextError_decorator(self):
        """
        Tests that when a ContextualProperty getter is used with a nonexistent
        context and no default, a MissingContextError is raised. Creates the
        property by using the decorator
        """
        context_0 = 'context_0'

        class TestClass:
            __context__ = MagicMock(context=None)

            @base.contextualproperty
            def attr(self):
                return getattr(self, '_attr', None)

            @attr.setter_context(context_0)
            def attr(self, val):
                setattr(self, '_attr', val + '_0')

        sample = TestClass()

        # test that an explicitly defined setter works
        sample.__context__.context = context_0
        context_val_0 = 'context value'
        expected_value = context_val_0 + '_0'
        sample.attr = context_val_0
        self.assertEqual(sample.attr, expected_value)

        # test that trying to set without a default fails
        sample.__context__.context = 'nonexistent context'
        new_value = "can't set"
        msg = ("ContextualProperty has no default setter for 'attr' and is " +
               "missing context 'nonexistent context'")
        with self.assertRaises(MissingContextError, msg=msg):
            sample.attr = new_value

    def test_no_fset_raises_MissingContextError_decorator(self):
        """
        Tests that when a ContextualProperty has no getter, an AttributeError
        is raised with a message matching the default from property. Creates
        the property by using the decorator
        """
        context_0 = 'context_0'
        context_1 = 'context_1'

        class TestClass:
            __context__ = MagicMock(context=None)

            @base.contextualproperty
            def attr(self):
                return getattr(self, '_attr', None)

        sample = TestClass()

        # test that trying to set with no setter raises an exception
        new_value = "can't set"
        msg = "ContextualProperty has no default setter for 'attr'"
        with self.assertRaises(MissingContextError, msg=msg):
            sample.attr = new_value


class ContextualPropertyDeleter(TestCase):
    """
    Tests to ensure that a ContextualProperty's deleter and deleter_context
    work as expected
    """
    def test_fdel_default_only(self):
        """
        Tests that when a ContextualProperty only has the initially provided
        deleter function it will execute that function. Creates the
        property by using the decorator
        """
        deleter_fn = lambda obj: setattr(obj, 'attr', 'deleted')

        context_mock = MagicMock(context=None)
        obj = MagicMock(attr='', __context__=context_mock)

        prop = base.ContextualProperty(fdel=deleter_fn)

        # test default
        expected_value = 'deleted'
        prop.fdel(obj)
        self.assertEqual(obj.attr, expected_value)

    def test_fdel_default_only_decorator(self):
        """
        Tests that when a ContextualProperty only has the initially provided
        deleter function it will execute that function. Creates the
        property by using the decorator
        """

        class TestClass:
            __context__ = MagicMock(context=None)

            @base.contextualproperty
            def attr(self):
                return getattr(self, '_attr', None)

            @attr.deleter
            def attr(self):
                setattr(self, '_attr', 'deleted')

        sample = TestClass()

        # test default
        expected_value = 'deleted'
        del sample.attr
        self.assertEqual(sample.attr, expected_value)

    def test_fdel_one_additional_context(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected.
        Creates the property by using the constructor
        """
        deleter_fn = lambda obj: setattr(obj, 'attr', 'deleted')
        alt_deleter_1 = lambda obj: setattr(obj, 'attr', f'deleted1')

        context_mock = MagicMock(context=None)
        obj = MagicMock(attr='', __context__=context_mock)

        prop = base.ContextualProperty(fdel=deleter_fn)
        prop.deleter_context('alt context 1')(alt_deleter_1)

        # test default
        expected_value = 'deleted'
        prop.fdel(obj)
        self.assertEqual(obj.attr, expected_value)

        # test alt context 1
        context_mock.context = 'alt context 1'
        expected_value = 'deleted1'
        prop.fdel(obj)
        self.assertEqual(obj.attr, expected_value)

    def test_fdel_one_additional_context_decorator(self):
        """
        Tests that when a ContextualProperty has one additional context
        function, both the default and secondary functions work as expected.
        Creates the property by using the decorator
        """
        context_0 = 'context_0'

        class TestClass:
            __context__ = MagicMock(context=None)

            @base.contextualproperty
            def attr(self):
                return getattr(self, '_attr', None)

            @attr.deleter
            def attr(self):
                setattr(self, '_attr', 'deleted')

            @attr.deleter_context(context_0)
            def attr(self):
                setattr(self, '_attr', 'deleted_0')

        sample = TestClass()

        # test default
        expected_value = 'deleted'
        del sample.attr
        self.assertEqual(sample.attr, expected_value)

        # test alt context 1
        sample.__context__.context = context_0
        expected_value = 'deleted_0'
        del sample.attr
        self.assertEqual(sample.attr, expected_value)

    def test_fdel_multiple_additional_contexts(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected.
        Creates the property by using the constructor
        """
        deleter_fn = lambda obj: setattr(obj, 'attr', 'deleted')
        alt_deleter_1 = lambda obj: setattr(obj, 'attr', f'deleted1')
        alt_deleter_2 = lambda obj: setattr(obj, 'attr', f'deleted2')

        context_mock = MagicMock(context=None)
        obj = MagicMock(attr='', __context__=context_mock)

        prop = base.ContextualProperty(fdel=deleter_fn)
        prop.deleter_context('alt context 1')(alt_deleter_1)
        prop.deleter_context('alt context 2')(alt_deleter_2)

        # test default
        expected_value = 'deleted'
        prop.fdel(obj)
        self.assertEqual(obj.attr, expected_value)

        # test alt context 1
        context_mock.context = 'alt context 1'
        expected_value = 'deleted1'
        prop.fdel(obj)
        self.assertEqual(obj.attr, expected_value)

        # test alt context 2
        context_mock.context = 'alt context 2'
        expected_value = 'deleted2'
        prop.fdel(obj)
        self.assertEqual(obj.attr, expected_value)

    def test_fdel_multiple_additional_contexts_decorator(self):
        """
        Tests that when a ContextualProperty has more than one additional
        context function, all functions (including default) work as expected.
        Creates the property by using the decorator
        """
        context_0 = 'context_0'
        context_1 = 'context_1'

        class TestClass:
            __context__ = MagicMock(context=None)

            @base.contextualproperty
            def attr(self):
                return getattr(self, '_attr', None)

            @attr.deleter
            def attr(self):
                setattr(self, '_attr', 'deleted')

            @attr.deleter_context(context_0)
            def attr(self):
                setattr(self, '_attr', 'deleted_0')

            @attr.deleter_context(context_1)
            def attr(self):
                setattr(self, '_attr', 'deleted_1')

        sample = TestClass()

        # test default
        expected_value = 'deleted'
        del sample.attr
        self.assertEqual(sample.attr, expected_value)

        # test alt context 0
        sample.__context__.context = context_0
        expected_value = 'deleted_0'
        del sample.attr
        self.assertEqual(sample.attr, expected_value)

        # test alt context 1
        sample.__context__.context = context_1
        expected_value = 'deleted_1'
        del sample.attr
        self.assertEqual(sample.attr, expected_value)


    def test_fset_nonexistent_context_raises_MissingContextError_decorator(
            self):
        """
        Tests that when a ContextualProperty deleter is used with a nonexistent
        context and no default, a MissingContextError is raised. Creates the
        property by using the decorator
        """
        context_0 = 'context_0'

        class TestClass:
            __context__ = MagicMock(context=None)

            @base.contextualproperty
            def attr(self):
                return getattr(self, '_attr', None)

            @attr.setter
            def attr(self, val):
                setattr(self, '_attr', val)

            @attr.deleter_context(context_0)
            def attr(self):
                # not actually deleting, just marking we were in this method
                setattr(self, '_attr', 'deleted_0')

        sample = TestClass()

        # test that an explicitly defined setter works
        sample.__context__.context = context_0
        context_val_0 = 'context value'
        expected_value = 'deleted_0'
        sample.attr = context_val_0
        del sample.attr
        self.assertEqual(sample.attr, expected_value)

        # test that trying to set without a default fails
        sample.__context__.context = 'nonexistent context'
        msg = ("ContextualProperty has no default deleter for 'attr' and is " +
               "missing context 'nonexistent context'")
        with self.assertRaises(MissingContextError, msg=msg):
            del sample.attr

    def test_no_fset_raises_MissingContextError_decorator(self):
        """
        Tests that when a ContextualProperty has no default deleter, a
        MissingContextError is raised with a message matching the default from
        property. Creates the property by using the decorator
        """

        class TestClass:
            __context__ = MagicMock(context=None)

            @base.contextualproperty
            def attr(self):
                return getattr(self, '_attr', None)

        sample = TestClass()

        # test that trying to set with no setter raises an exception
        msg = "ContextualProperty has no default setter for 'attr'"
        with self.assertRaises(MissingContextError, msg=msg):
            del sample.attr


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
        def test_function(obj):
            """testdoc"""
            return 'test value'

        prop = base.contextualproperty(test_function)

        expected_name = 'test_function'
        expected_doc = 'testdoc'
        expected_fget = test_function

        self.assertEqual(prop._ContextualProperty__fget_contexts[None],
                         expected_fget)
        self.assertEqual(prop._ContextualProperty__name, expected_name)
        self.assertEqual(prop.__doc__, expected_doc)



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
        obj = NamespacedObject()
        self.assertIsInstance(obj, NamespacedObject)


class NamespacedObjectGetters(TestCase):
    """
    Tests to ensure that the NamespacedObject has a __namespace__ attribute,
    that instances of NamespacedObject can access this attribute's getters,
    that the __get_namespace__ class function does not work on the
    base object, that an overriding class can properly assign itself a
    namespace, and that attempting to access the NamespacedObject in the
    JSON_DATA_CONTEXT will return nothing
    """
    sample_namespace = 'sample_namespace'

    class ImplementingClass(base.NamespacedObject):
        __context__ = MagicMock(context=None)

        @classmethod
        def __get_namespace__(cls):
            return 'sample_namespace'

    def test_namespace_standard_context(self):
        """
        Tests that an object implementing get_namespace works as expected
        """
        # test that we can get the __namespace__ based on the overridden
        # __get_namespace__ method
        obj = self.ImplementingClass()
        self.assertEqual(obj.__namespace__, self.sample_namespace)

    def test_no_namespace(self):
        """
        Test that an object without a namespace produces a None value
        """
        obj = base.NamespacedObject()
        self.assertIsNone(obj.__namespace__)

    def test_json_data_context_namespace(self):
        """
        Test that an object with the JSON_DATA_CONTEXT context returns None as
        its namespace
        """
        # check the default namespace
        obj = self.ImplementingClass()
        self.assertEqual(obj.__namespace__, self.sample_namespace)

        # test that if the object's context is the JSON_DATA_CONTEXT the
        # __namespace__ value will show as None
        obj.__context__.context = JSON_DATA_CONTEXT
        self.assertIsNone(obj.__namespace__)
        obj.__context__.context = None


class NamespacedObjectSetters(TestCase):
    """
    Tests to ensure that the NamespacedObject __namespace__ setter can change
    the class namespace
    """

    def setUp(self):
        self.sample_namespace = 'sample_namespace'

        class ImplementingClass(base.NamespacedObject):
            __context__ = MagicMock(context=None)

            @classmethod
            def __get_namespace__(cls):
                return 'sample_namespace'

        self.ImplementingClass = ImplementingClass

    def test_namespace_change_outside_class_change_context(self):
        """
        Tests that a namespace value cannot be changed outside the
        class change context
        """
        # test that we can get the __namespace__ based on the overridden
        # __get_namespace__ method
        obj = self.ImplementingClass()
        self.assertEqual(obj.__namespace__, self.sample_namespace)

        # test that we cannot change the __namespace__ value without the
        # correct context
        with self.assertRaises(MissingContextError):
            obj.__namespace__ = 'cannot change'

    def test_namespace_change_with_class_change_context(self):
        """
        Tests that when an object is in the class change context, the
        namespace value can be changed
        """
        # test that we can get the __namespace__ based on the overridden
        # __get_namespace__ method
        obj = self.ImplementingClass()
        self.assertEqual(obj.__namespace__, self.sample_namespace)

        # test that we can change the __namespace__ in the CLASS_CHANGE_CONTEXT
        new_namespace = 'changed'
        obj.__context__.context = CLASS_CHANGE_CONTEXT
        obj.__namespace__ = new_namespace
        self.assertEqual(obj.__namespace__, new_namespace)

    def test_namespace_reset_on_delete(self):
        """
        Tests that when the namespace property is deleted, it does not remove
        the namespace entirely but rather resets it to the default for that
        class (reverses changes done under class change context)
        """
        # check default namespace
        obj = self.ImplementingClass()
        self.assertEqual(obj.__namespace__, self.sample_namespace)

        # check namespace change
        new_namespace = 'changed'
        obj.__context__.context = CLASS_CHANGE_CONTEXT
        obj.__namespace__ = new_namespace
        self.assertEqual(obj.__namespace__, new_namespace)

        # test that the namespace is REVERTED TO DEFAULT on delete
        del obj.__namespace__
        self.assertEqual(obj.__namespace__, self.sample_namespace)


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
        obj = JsonContextAwareManager()

        self.assertIsInstance(obj._stack, list)
        self.assertIsNone(obj.context)
        self.assertFalse(obj.active)

    def test_json_context_callable_adds_to_stack(self):
        """
        Tests that a json context manager can be called to add a new item to
        the stop of the stack, but does not set the active flag
        """
        sample_context0 = 'sample_context0'
        sample_context1 = 'sample_context1'

        obj = JsonContextAwareManager()

        obj(sample_context0)
        self.assertEqual(obj._stack, [None])
        self.assertEqual(obj.context, sample_context0)
        self.assertFalse(obj.active)

        obj(sample_context1)
        self.assertEqual(obj._stack, [None, sample_context0])
        self.assertEqual(obj.context, sample_context1)
        self.assertFalse(obj.active)

    def test_json_context_aware_manager_single_context(self):
        """
        Tests that when a JsonContextAwareManager is called and used as a
        context manager, it automatically sets the provided value as the new
        context, adds it to the stack, and marks the active flag; also tests
        that when the context manager ends, the stack is empty, context is None,
        and the active flag is unset
        """
        sample_context0 = 'sample_context0'

        obj = JsonContextAwareManager()

        with obj(sample_context0):
            self.assertEqual(obj._stack, [None])
            self.assertEqual(obj.context, sample_context0)
            self.assertTrue(obj.active)

    def test_json_context_aware_manager_nested_contexts(self):
        """
        Tests that when the same JsonContextAwareManager is used as a context
        manager in a nested way, the last applied context will be the active
        context, the stack will be in the correct order, and the active flag
        will be set; also tests that when the context manager ends at each
        level, the active context is returned to the next item on the stack
        and the active flag remains marked until the stack is completely empty
        """
        sample_context0 = 'sample_context0'
        sample_context1 = 'sample_context1'

        obj = JsonContextAwareManager()

        with obj(sample_context0):
            # check values before nesting
            self.assertEqual(obj._stack, [None])
            self.assertEqual(obj.context, sample_context0)
            self.assertTrue(obj.active)

            with obj(sample_context1):
                # check nested values are as expected
                self.assertEqual(obj._stack, [None, sample_context0])
                self.assertEqual(obj.context, sample_context1)
                self.assertTrue(obj.active)

            # check that un-nesting was successful
            self.assertEqual(obj._stack, [None])
            self.assertEqual(obj.context, sample_context0)
            self.assertTrue(obj.active)

        self.assertEqual(obj._stack, [])
        self.assertEqual(obj.context, None)
        self.assertFalse(obj.active)


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

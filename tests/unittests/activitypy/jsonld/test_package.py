"""
Unit tests for jsonld package objects
"""
import unittest.main
from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from jsonld import package
from jsonld import ApplicationActivityJson, JsonProperty


class JsonLdPackageTests(TestCase):
    """
    Tests that JsonLdPackage objects are able to be constructed, iterated,
    retrieved from via index, hashed, and have a string representation created
    from them. Also tests that the classes, properties, and json transformation
    functions are properly stored and that logging is correctly implemented
    """

    def test_namespace_from_constructor(self, *args):
        """
        Tests that the constructor sets the namespace value when a string is
        provided
        """
        sample_namespace = 'https://sample-namespace.org/ns/'
        pkg = package.JsonLdPackage(sample_namespace)

        self.assertEqual(sample_namespace, pkg.namespace)

    def test_namespace_cannot_be_changed(self, *args):
        """
        Tests that after a JsonLdPackage object has been created, the namespace
        value cannot be changed and will raise an AttributeError if reassignment
        is attempted
        """
        sample_namespace = 'https://sample-namespace.org/ns/'
        sample_alt_namespace = 'https://alt-namespace.org/ns/'
        pkg = package.JsonLdPackage(sample_namespace)

        with self.assertRaises(AttributeError,
                               msg='JsonLdPackage namespace is immutable'):
            pkg.namespace = sample_alt_namespace

        self.assertEqual(sample_namespace, pkg.namespace)

    def test_namespace_must_be_a_string(self, *args):
        """
        Tests that when a JsonLdPackage object is provided a namespace value
        that is not a string, it will raise a TypeError
        """
        bad_namespace_0 = 5
        bad_namespace_1 = None

        with self.assertRaises(TypeError,
                               msg="JsonLdPackage namespace must be a " +
                                   "string, got <class 'int'>"):
            pkg = package.JsonLdPackage(bad_namespace_0)
        with self.assertRaises(TypeError,
                               msg="JsonLdPackage namespace must be a " +
                                   "string, got <class 'NoneType'>"):
            pkg = package.JsonLdPackage(bad_namespace_1)

    def test_namespace_property_defaults_are_correct(self, *args):
        """
        Tests that the default values for "classes", "properties", and
        "transforms" are all empty dictionaries
        """
        sample_namespace = 'https://sample-namespace.org/ns/'
        pkg = package.JsonLdPackage(sample_namespace)

        self.assertIsInstance(pkg.classes, dict)
        self.assertIsInstance(pkg.properties, dict)
        self.assertIsInstance(pkg.transforms, dict)

    @patch.object(package, 'logger')
    def test_classes_property_setter(self, mock_logger, *args):
        """
        Tests that the classes property sets a dictionary correctly, raises
        a TypeError when attempting to set classes to a non-dictionary, and that
        the logger is producing info messages for each change to the package
        """

        class TestClass0(ApplicationActivityJson):
            """Junk class for test"""

        class TestClass1(ApplicationActivityJson):
            """Junk class for test"""

        class TestClass2(ApplicationActivityJson):
            """Junk class for test"""

        class IncorrectClass:
            """Junk class for testing that should NOT be allowed into the
            package"""

        # checks that all elements from the dictionary will be added
        sample_namespace = 'https://sample-namespace.org/ns/'
        sample_classes = {'https://sample-namespace.org/ns/0': TestClass0,
                          'https://sample-namespace.org/ns/1': TestClass1}
        pkg0 = package.JsonLdPackage(sample_namespace, classes=sample_classes)
        self.assertEqual(pkg0.classes, sample_classes)

        # checks that attempting assignment of non-dict will raise a TypeError
        bad_classes = (TestClass0, TestClass1)
        with self.assertRaises(TypeError,
                               msg="'classes' MUST be a dict or dict-like" +
                                   "object"):
            pkg1 = package.JsonLdPackage(sample_namespace, classes=bad_classes)

        mock_logger.info.assert_has_calls([
            call(f'Setting "https://sample-namespace.org/ns/0" ' +
                 f'in package "https://sample-namespace.org/ns/" ' +
                 f'to class "TestClass0"'),
            call(f'Setting "https://sample-namespace.org/ns/1" ' +
                 f'in package "https://sample-namespace.org/ns/" ' +
                 f'to class "TestClass1"'),
        ])

        # checks that attempting to add classes not inherited from the jsonld
        # engine's expected base class will raise a ValueError
        incorrect_classes = {'https://sample-namespace.org/ns/2': TestClass2,
                             'https://sample-namespace.org/ns/x': IncorrectClass
                             }
        pkg2 = package.JsonLdPackage(sample_namespace)
        with self.assertRaises(ValueError,
                               msg='cannot add "https://sample-namespace.org/ns/x" ' +
                                   'to package "https://sample-namespace.org/ns/", ' +
                                   'classes added to package MUST inherit from ' +
                                   'activitypy.jsonld.ApplicationActivityJson'):
            pkg2.classes = incorrect_classes
        # if ANY of the incoming values are wrong, NOTHING should be changed
        self.assertNotIn('https://sample-namespace.org/ns/2',
                         pkg2.classes.keys())

    @patch.object(package, 'logger')
    def test_properties_property_setter(self, mock_logger, *args):
        """
        Tests that the setter for the 'properties' property works as expected.
        Should raise a TypeError attempting to assign a non-dictionary, a
        ValueError if any values in the assigned dict are not descendents of
        the JsonProperty class, and that adequate logging is occurring
        """

        class TestProp0(JsonProperty):
            """Junk class for testing properties"""

        class TestProp1(JsonProperty):
            """Junk class for testing properties"""

        class TestProp2(JsonProperty):
            """Junk class for testing properties"""

        class TestPropX:
            """Junk class for testing properties that raises a ValueError"""

        sample_namespace = 'https://sample-namespace.org/ns/'
        sample_properties = {'https://sample-namespace.org/ns/p0': TestProp0,
                             'https://sample-namespace.org/ns/p1': TestProp1}

        # tests that all provided properties get added to the dictionary
        pkg0 = package.JsonLdPackage(sample_namespace,
                                     properties=sample_properties)
        self.assertEqual(pkg0.properties, sample_properties)

        # tests that proper logging occurred while setting each value
        mock_logger.assert_has_calls([
            call.info('Setting "https://sample-namespace.org/ns/p0" in ' +
                      'package "https://sample-namespace.org/ns/" to property ' +
                      'class "TestProp0"'),
            call.info('Setting "https://sample-namespace.org/ns/p1" in ' +
                      'package "https://sample-namespace.org/ns/" to property ' +
                      'class "TestProp1"')
        ])

        # tests that a TypeError is raised when trying to assign a non-dict
        bad_prop_type = (TestProp0, TestProp1)
        with self.assertRaises(TypeError,
                               msg="'properties' MUST be a dict or dict-like " +
                                   "object"):
            pkg1 = package.JsonLdPackage(sample_namespace,
                                         properties=bad_prop_type)

        # tests that adding properties not inheriting from JsonProperty will
        # result in a ValueError
        incorrect_prop_type = {'https://sample-namespace.org/ns/p2': TestProp2,
                               'https://sample-namespace.org/ns/x': TestPropX}
        pkg2 = package.JsonLdPackage(sample_namespace,
                                     properties=sample_properties)
        with self.assertRaises(ValueError,
                               msg='cannot add' +
                                   '"https://sample-namespace.org/ns/x" to ' +
                                   'package "https://sample-namespace.org/ns", ' +
                                   'properties added to package MUST inherit ' +
                                   'from activitypy.jsonld.JsonProperty'):
            pkg2.properties = incorrect_prop_type

        # tests that if there is an error with one property, the existing props
        # remain unchanged
        self.assertEqual(pkg2.properties, sample_properties)

    @patch.object(package, 'logger')
    def test_transforms_property_setter(self, mock_logger, *args):
        """
        Tests that the setter for the 'transforms' property works as expected.
        Should raise a TypeError attempting to assign a non-dictionary, a
        ValueError if any keys in the assigned dict are not descendents of
        the ApplicationActivityJson class, a KeyError if any of the values in
        the assigned dict are not callables, and that proper logging is
        occurring
        """

        class TestClass0(ApplicationActivityJson):
            """Junk class for testing"""

        class TestClass1(ApplicationActivityJson):
            """Junk class for testing"""

        class TestClass2(ApplicationActivityJson):
            """Junk class for testing"""

        class IncorrectClass:
            """Junk class for testing that should raise a ValueError"""

        def test_func0():
            """Junk function for testing"""

        def test_func1():
            """Junk function for testing"""

        def test_func2():
            """Junk function for testing"""

        sample_namespace = 'https://sample-namespace.org/ns/'
        sample_transforms = {TestClass0: test_func0, TestClass1: test_func1}

        # tests that the mapping is added without alterations
        pkg0 = package.JsonLdPackage(sample_namespace,
                                     transforms=sample_transforms)
        self.assertEqual(pkg0.transforms, sample_transforms)

        # tests that proper logging occurred while setting each value
        mock_logger.assert_has_calls([
            call.info('Setting transform function for "TestClass0" in ' +
                      'package "https://sample-namespace.org/ns/" to ' +
                      'function "test_func0"'),
            call.info('Setting transform function for "TestClass1" in ' +
                      'package "https://sample-namespace.org/ns/" to ' +
                      'function "test_func1"')
        ])

        # tests that a TypeError is raised when trying to assign a non-dict
        bad_transforms_type = (TestClass0, TestClass1)
        with self.assertRaises(TypeError, msg="'transforms' must be a dict " +
                                              "or dict-like object"):
            pkg1 = package.JsonLdPackage(sample_namespace,
                                         transforms=bad_transforms_type)

        # tests that keys not inheriting from ApplicationActivityJson will
        # result in a ValueError
        pkg2 = package.JsonLdPackage(sample_namespace,
                                     transforms=sample_transforms)
        incorrect_transforms_0 = {
            TestClass2: test_func2, IncorrectClass: test_func0
        }
        incorrect_transforms_1 = {
            TestClass2: test_func2, TestClass0: 'bad_value'
        }

        fail_msg = ('cannot add transforms to package ' +
                    '"https://sample-namespace.org/ns/", each transform ' +
                    'must map a class inheriting from activitypy.jsonld.' +
                    'ApplicationActivityJson to a callable; found {errs}')
        with self.assertRaises(ValueError, msg=fail_msg.format(
                errs='(IncorrectClass: test_func0)')):
            pkg2.transforms = incorrect_transforms_0
        # tests that values that are not callable will result in a ValueError
        with self.assertRaises(ValueError, msg=fail_msg.format(
                errs='(TestClass0: int)')):
            pkg2.transforms = incorrect_transforms_1

        # tests that if there is an error with one pair, nothing is changed
        self.assertEqual(pkg2.transforms, sample_transforms)

    def test_hash_gets_correct_values(self, *args):
        namespace_0 = 'https://sample-namespace-0.org/ns/'
        namespace_1 = 'https://sample-namespace-1.org/ns/'

        expected_hash_0 = hash(namespace_0)
        expected_hash_1 = hash(namespace_1)

        pkg0 = package.JsonLdPackage(namespace_0)
        pkg1 = package.JsonLdPackage(namespace_1)

        self.assertEqual(expected_hash_0, hash(pkg0))
        self.assertEqual(expected_hash_1, hash(pkg1))


if __name__ == '__main__':
    unittest.main()

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


if __name__ == '__main__':
    unittest.main()

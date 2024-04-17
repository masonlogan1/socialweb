import unittest

from activitystreams import create_engine
import json


class TestSampleData:
    engine = create_engine()

    def test_ex1(self):
        with open("core-ex1-jsonld.json") as test_file:
            # Store raw json string and dictionary.
            test_data_raw = test_file.read()
            test_data_dict = json.loads(test_data_raw)

            # Create an engine object with the raw json string, store object's data and json output.
            obj_raw = TestSampleData.engine.from_json(test_data_raw)
            obj_raw_data = obj_raw.data()
            obj_raw_json = obj_raw.json()

            # Create an engine object with the dictionary, store object's data and json output.
            obj_dict = TestSampleData.engine.from_json(test_data_dict)
            obj_dict_data = obj_dict.data()
            obj_dict_json = obj_dict.json()

            # Create dictionaries based-off engine json output for json validation.
            obj_raw_json_dict = json.loads(obj_raw_json)
            obj_dict_json_dict = json.loads(obj_dict_json)

            # Assert both engine objects are of same length with same entries as original dictionary,
            # as well as dictionaries created from the JSON output of both engine objects.
            assert len(test_data_dict.keys()) == len(obj_raw_data.keys()) == len(obj_dict_data.keys()) == len(obj_raw_json_dict.keys()) == len(obj_dict_json_dict.keys())
            for attr in test_data_dict:
                assert test_data_dict[attr] == obj_raw_data[attr] == obj_dict_data[attr] == obj_raw_json_dict[attr] == obj_dict_json_dict[attr]


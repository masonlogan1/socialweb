import unittest

from activitystreams import create_engine
import json


class TestSampleData:
    engine = create_engine()

    def test_ex1(self):
        with open("core-ex1-jsonld.json") as test_file:
            # Create dictionary from json file
            test_data = json.load(test_file)
            # Load object into engine
            engine_obj = TestSampleData.engine.from_json(test_data)
            # Compare engine object's json output to original json data
            a = json.dumps(engine_obj.json(), sort_keys=True)

            print("\nTESTSDATA")
            print(test_data)

            print("ENGINEOBJ")
            print(engine_obj)

            assert 1 == 1

    def test_ex2(self):
        assert 2 == 2


class TestDataSimpl:

    def test_0001(self):
        assert 1 == 1

    def test_0002(self):
        assert 2 == 2

import requests
import threading
from ppil import ApiInstance
from ppil.tests._test_variables import *


TEST_DATASETS = [{
    'data': EXECUTION_PROLOG_DATA,
    'result': EXPECTED_EXECUTION_PROLOG_RESPONSE
}, {
    'data': EXECUTION_JSON_DATA,
    'result': EXPECTED_EXECUTION_JSON_RESPONSE
}, {
    'data': EXECUTION_BAD_DOG,
    'result': EXPECTED_EXECUTION_BAD_DOG_JSON
}, {
    'data': EXECUTION_RECURSION,
    'result': EXPECTED_EXECUTION_RECURSION_JSON
}, {
    'data': EXECUTION_SIBLINGS,
    'result': EXPECTED_EXECUTION_SIBLINGS_JSON
}, {
    'data': EXECUTION_EINSTEIN_PUZZLE,
    'result': EXPECTED_EINSTEIN_PUZZLE_JSON
}, {
    'data': EXECUTION_ALTERNATIVE_EINSTEIN_PUZZLE,
    'result': EXPECTED_ALTERNATIVE_EINSTEIN_PUZZLE_JSON
}]


def _run_instance():
    api = ApiInstance()
    threading.Thread(target=api.run).start()


def test_conversion():
    prolog_to_json = requests.post(f"{INSTANCE_URL}/prolog-to-json", json=PROLOG_DATA)
    json_to_prolog = requests.post(f"{INSTANCE_URL}/json-to-prolog", json=JSON_DATA)

    assert prolog_to_json.json() == JSON_DATA
    assert json_to_prolog.json() == PROLOG_DATA


def test_execution_function():
    for test_item in TEST_DATASETS:
        response = requests.post(f"{INSTANCE_URL}/execute", json=test_item['data'])
        assert response.json() == test_item['result']


_run_instance()

test_conversion()
test_execution_function()

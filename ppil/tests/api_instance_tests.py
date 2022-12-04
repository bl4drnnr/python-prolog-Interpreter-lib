import requests
import threading
from ppil import ApiInstance
from ppil.tests._test_variables import \
    INSTANCE_URL,\
    PROLOG_DATA,\
    JSON_DATA, \
    EXECUTION_PROLOG_DATA, \
    EXPECTED_EXECUTION_PROLOG_RESPONSE, \
    EXECUTION_JSON_DATA, \
    EXPECTED_EXECUTION_JSON_RESPONSE


def _run_instance():
    api = ApiInstance()
    threading.Thread(target=api.run).start()


def test_conversion():
    prolog_to_json = requests.post(f"{INSTANCE_URL}/prolog-to-json", json=PROLOG_DATA)
    json_to_prolog = requests.post(f"{INSTANCE_URL}/json-to-prolog", json=JSON_DATA)

    assert prolog_to_json.json() == JSON_DATA
    assert json_to_prolog.json() == PROLOG_DATA


def test_execution_from_prolog():
    response = requests.post(f"{INSTANCE_URL}/execute", json=EXECUTION_PROLOG_DATA)

    assert response.json() == EXPECTED_EXECUTION_PROLOG_RESPONSE


def test_execution_from_json():
    response = requests.post(f"{INSTANCE_URL}/execute", json=EXECUTION_JSON_DATA)

    assert response.json() == EXPECTED_EXECUTION_JSON_RESPONSE


_run_instance()

test_conversion()
test_execution_from_prolog()
test_execution_from_json()

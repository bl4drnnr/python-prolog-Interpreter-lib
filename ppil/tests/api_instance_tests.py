import requests
import threading
from ppil import ApiInstance

INSTANCE_URL = 'http://127.0.0.1:5000'

PROLOG_DATA = "predicate_name(arg1, 'str_arg', [list, [X]]) :- 5 + 2 > 1 + 3, inner_predicate([V, 100], arg1)."
JSON_DATA = {
    "data": [
        {
            "arguments": [
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "arg1"
                },
                {
                    "data_type": "string",
                    "type": "atom",
                    "value": "str_arg"
                },
                {
                    "items": [
                        {
                            "data_type": "atom",
                            "type": "atom",
                            "value": "list"
                        },
                        {
                            "items": [
                                {
                                    "data_type": "variable",
                                    "type": "atom",
                                    "value": "X"
                                }
                            ],
                            "type": "list"
                        }
                    ],
                    "type": "list"
                }
            ],
            "conditions": [
                {
                    "left_side": "5+2",
                    "right_side": "1+3",
                    "separator": ">",
                    "type": "condition"
                },
                {
                    "arguments": [
                        {
                            "items": [
                                {
                                    "data_type": "variable",
                                    "type": "atom",
                                    "value": "V"
                                },
                                {
                                    "data_type": "number",
                                    "type": "atom",
                                    "value": 100
                                }
                            ],
                            "type": "list"
                        },
                        {
                            "data_type": "atom",
                            "type": "atom",
                            "value": "arg1"
                        }
                    ],
                    "name": "inner_predicate",
                    "type": "predicate"
                }
            ],
            "joins": [
                ","
            ],
            "name": "predicate_name",
            "type": "fact"
        }
    ],
    "statusCode": 200
}

EXECUTION_PROLOG_DATA = """
    person(michal, aleh, larysa, m, 19).
    person(aleh, wlodzimierz, ania, m, 56).
    person(larysa, andrzej, ola, f, 45).
    person(maciej, andrzej, ola, m, 48).
    person(andrzej, person1, person2, m, 82).
    person(ola, person3, person4, f, 75).
    person(wlodzimierz, person5, person6, m, 81).
    person(ania, person7, person8, f, 77).
    mother(X, Y):-person(X, _, _, _, E), person(Y, _, W, _, L), W = X, M1 is L + 14, E >= M1.
    father(X, Y):-person(X, _, _, _, E), person(Y, W, _, _, L), W = X, M1 is L + 14, E >= M1.
    brother(X, Y):-person(X,B,C,D,_), person(Y,P,M,_,_), B=P, C=M, D = m, X\\=Y.
    sister(X, Y):-person(X,Q,W,E,_), person(Y,A,B,_,_), Q=A, W=B, E = f, X\\=Y.
    grandmother(X, Y):-(((mother(A, Y), mother(X, B)); (mother(X, A), father(B, Y))), A = B).
    grandad(X, Y):-(((father(A, Y), father(X, B)); (father(X, A), mother(B, Y))), A = B).
"""
EXECUTION_JSON_DATA = {}


def _run_instance():
    api = ApiInstance()
    threading.Thread(target=api.run).start()


def test_prolog_to_json():
    response = requests.post(f"{INSTANCE_URL}/prolog-to-json", json={
        "data": PROLOG_DATA
    })
    assert response.json() == JSON_DATA


def test_json_to_prolog():
    response = requests.post(f"{INSTANCE_URL}/json-to-prolog", json=JSON_DATA)
    prolog_string = response.json().get('data').replace('\n', '').strip()
    expected_prolog_string = PROLOG_DATA.replace('\n', '').replace(' ', '')

    assert prolog_string == expected_prolog_string


def test_execution_from_prolog():
    response = requests.post(f"{INSTANCE_URL}/execute", json={
        "data": EXECUTION_PROLOG_DATA,
        "query": ["grandad(X, Y)"]
    })
    expected_response = {
        "data": [
            {
                "X": "wlodzimierz",
                "Y": "michal"
            },
            {
                "X": "andrzej",
                "Y": "michal"
            }
        ],
        "statusCode": 200
    }

    assert response.json() == expected_response


def test_execution_from_json():
    response = requests.post(f"{INSTANCE_URL}/execute", json={
        "data": EXECUTION_JSON_DATA,
        "query": ["mother(X, Y)", "father(X, Y)"]
    })
    expected_response = {}

    assert response.json() == expected_response


def test_execution_prolog_and_json():
    pass


_run_instance()

test_prolog_to_json()
test_json_to_prolog()
test_execution_from_prolog()
test_execution_from_json()
test_execution_prolog_and_json()

import requests
import threading
from ppil import ApiInstance

INSTANCE_URL = 'http://127.0.0.1:5000'

PROLOG_DATA = """
    predicate_name(arg1, 'str_arg', [list, [X]]) :- 5 + 2 > 1 + 3, inner_predicate([V, 100], arg1).
"""
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
EXPECTED_EXECUTION_PROLOG_RESPONSE = {
        "data": {
            "grandad": [
                {
                    "X": "wlodzimierz",
                    "Y": "michal"
                },
                {
                    "X": "andrzej",
                    "Y": "michal"
                }
            ]
        },
        "statusCode": 200
    }
EXECUTION_JSON_DATA = [
        {
            "arguments": [
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "michal"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "aleh"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "larysa"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "m"
                },
                {
                    "data_type": "number",
                    "type": "atom",
                    "value": 19
                }
            ],
            "name": "person",
            "type": "predicate"
        },
        {
            "arguments": [
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "aleh"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "wlodzimierz"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "ania"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "m"
                },
                {
                    "data_type": "number",
                    "type": "atom",
                    "value": 56
                }
            ],
            "name": "person",
            "type": "predicate"
        },
        {
            "arguments": [
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "larysa"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "andrzej"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "ola"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "f"
                },
                {
                    "data_type": "number",
                    "type": "atom",
                    "value": 45
                }
            ],
            "name": "person",
            "type": "predicate"
        },
        {
            "arguments": [
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "maciej"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "andrzej"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "ola"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "m"
                },
                {
                    "data_type": "number",
                    "type": "atom",
                    "value": 48
                }
            ],
            "name": "person",
            "type": "predicate"
        },
        {
            "arguments": [
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "andrzej"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "person1"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "person2"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "m"
                },
                {
                    "data_type": "number",
                    "type": "atom",
                    "value": 82
                }
            ],
            "name": "person",
            "type": "predicate"
        },
        {
            "arguments": [
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "ola"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "person3"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "person4"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "f"
                },
                {
                    "data_type": "number",
                    "type": "atom",
                    "value": 75
                }
            ],
            "name": "person",
            "type": "predicate"
        },
        {
            "arguments": [
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "wlodzimierz"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "person5"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "person6"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "m"
                },
                {
                    "data_type": "number",
                    "type": "atom",
                    "value": 81
                }
            ],
            "name": "person",
            "type": "predicate"
        },
        {
            "arguments": [
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "ania"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "person7"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "person8"
                },
                {
                    "data_type": "atom",
                    "type": "atom",
                    "value": "f"
                },
                {
                    "data_type": "number",
                    "type": "atom",
                    "value": 77
                }
            ],
            "name": "person",
            "type": "predicate"
        },
        {
            "arguments": [
                {
                    "data_type": "variable",
                    "type": "atom",
                    "value": "X"
                },
                {
                    "data_type": "variable",
                    "type": "atom",
                    "value": "Y"
                }
            ],
            "conditions": [
                {
                    "arguments": [
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "X"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "E"
                        }
                    ],
                    "name": "person",
                    "type": "predicate"
                },
                {
                    "arguments": [
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "Y"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "W"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "L"
                        }
                    ],
                    "name": "person",
                    "type": "predicate"
                },
                {
                    "left_side": "W",
                    "right_side": "X",
                    "separator": "=",
                    "type": "condition"
                }
            ],
            "joins": [
                ",",
                ","
            ],
            "name": "mother",
            "type": "fact"
        },
        {
            "arguments": [
                {
                    "data_type": "variable",
                    "type": "atom",
                    "value": "X"
                },
                {
                    "data_type": "variable",
                    "type": "atom",
                    "value": "Y"
                }
            ],
            "conditions": [
                {
                    "arguments": [
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "X"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "E"
                        }
                    ],
                    "name": "person",
                    "type": "predicate"
                },
                {
                    "arguments": [
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "Y"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "W"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "L"
                        }
                    ],
                    "name": "person",
                    "type": "predicate"
                },
                {
                    "left_side": "W",
                    "right_side": "X",
                    "separator": "=",
                    "type": "condition"
                }
            ],
            "joins": [
                ",",
                ","
            ],
            "name": "father",
            "type": "fact"
        }
    ]
EXPECTED_EXECUTION_JSON_RESPONSE = {
    'data':
        {
            'father': [
                {
                    'X': 'aleh',
                    'Y': 'michal'
                },
                {
                    'X': 'andrzej',
                    'Y': 'larysa'
                },
                {
                    'X': 'andrzej',
                    'Y': 'maciej'
                },
                {
                    'X': 'wlodzimierz',
                    'Y': 'aleh'
                }
            ],
            'mother': [
                {
                    'X': 'larysa',
                    'Y': 'michal'
                },
                {
                    'X': 'ola',
                    'Y': 'larysa'
                },
                {
                    'X': 'ola',
                    'Y': 'maciej'
                },
                {
                    'X': 'ania',
                    'Y': 'aleh'
                }
            ]
        },
    'statusCode': 200
}


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

    assert response.json() == EXPECTED_EXECUTION_PROLOG_RESPONSE


def test_execution_from_json():
    response = requests.post(f"{INSTANCE_URL}/execute", json={
        "data": EXECUTION_JSON_DATA,
        "query": ["mother(X, Y)", "father(X, Y)"]
    })

    assert response.json() == EXPECTED_EXECUTION_JSON_RESPONSE


_run_instance()

test_prolog_to_json()
test_json_to_prolog()
test_execution_from_prolog()
test_execution_from_json()

INSTANCE_URL = 'http://127.0.0.1:5000'

PROLOG_DATA = {
    "data": "predicate_name(arg1,'str_arg',[list,[X]]):-5+2 > 1+3,inner_predicate([V,100],arg1), (5+2 >= 2*2 -> else_clause(); [[TestVar], then_clause]).\n",
    "statusCode": 200
}
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
                },
                {
                    "else_clause": [
                        {
                            "arguments": [],
                            "name": "else_clause",
                            "type": "predicate"
                        }
                    ],
                    "if_condition": {
                        "left_side": "5+2",
                        "right_side": "2*2",
                        "separator": ">=",
                        "type": "condition"
                    },
                    "then_clause": [
                        {
                            "items": [
                                {
                                    "items": [
                                        {
                                            "data_type": "variable",
                                            "type": "atom",
                                            "value": "TestVar"
                                        }
                                    ],
                                    "type": "list"
                                },
                                {
                                    "data_type": "atom",
                                    "type": "atom",
                                    "value": "then_clause"
                                }
                            ],
                            "type": "list"
                        }
                    ],
                    "type": "condition_statement"
                }
            ],
            "joins": [
                ",",
                ","
            ],
            "name": "predicate_name",
            "type": "fact"
        }
    ],
    "statusCode": 200
}

EXECUTION_PROLOG_DATA = {
    "data": "person(michal, aleh, larysa, m, 19).person(aleh, wlodzimierz, ania, m, 56).person(larysa, andrzej, ola, f, 45).person(maciej, andrzej, ola, m, 48).person(andrzej, person1, person2, m, 82).person(ola, person3, person4, f, 75).person(wlodzimierz, person5, person6, m, 81).person(ania, person7, person8, f, 77).mother(X, Y):-person(X, _, _, _, E), person(Y, _, W, _, L), W = X, M1 is L + 14, E >= M1.father(X, Y):-person(X, _, _, _, E), person(Y, W, _, _, L), W = X, M1 is L + 14, E >= M1.brother(X, Y):-person(X,B,C,D,_), person(Y,P,M,_,_), B=P, C=M, D = m, X\=Y.sister(X, Y):-person(X,Q,W,E,_), person(Y,A,B,_,_), Q=A, W=B, E = f, X\=Y.grandmother(X, Y):-(((mother(A, Y), mother(X, B)); (mother(X, A), father(B, Y))), A = B).grandad(X, Y):-(((father(A, Y), father(X, B)); (father(X, A), mother(B, Y))), A = B).",
    "query": ["grandad(X, Y)", "grandmother(X, Y)"]
}
EXPECTED_EXECUTION_PROLOG_RESPONSE = {"data": {"grandad": [{"X": "wlodzimierz", "Y": "michal"}, {"X": "andrzej", "Y": "michal"}], "grandmother": [{"X": "ola", "Y": "michal"}, {"X": "ania", "Y": "michal"}]}, "statusCode": 200}

EXECUTION_JSON_DATA = {
    "data": [
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
                },
                {
                    "left_side": "M1",
                    "right_side": "L+14",
                    "separator": "is",
                    "type": "condition"
                },
                {
                    "left_side": "E",
                    "right_side": "M1",
                    "separator": ">=",
                    "type": "condition"
                }
            ],
            "joins": [
                ",",
                ",",
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
                },
                {
                    "left_side": "M1",
                    "right_side": "L+14",
                    "separator": "is",
                    "type": "condition"
                },
                {
                    "left_side": "E",
                    "right_side": "M1",
                    "separator": ">=",
                    "type": "condition"
                }
            ],
            "joins": [
                ",",
                ",",
                ",",
                ","
            ],
            "name": "father",
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
                            "value": "B"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "C"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "D"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
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
                            "value": "P"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "M"
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
                        }
                    ],
                    "name": "person",
                    "type": "predicate"
                },
                {
                    "left_side": "B",
                    "right_side": "P",
                    "separator": "=",
                    "type": "condition"
                },
                {
                    "left_side": "C",
                    "right_side": "M",
                    "separator": "=",
                    "type": "condition"
                },
                {
                    "left_side": "D",
                    "right_side": "m",
                    "separator": "=",
                    "type": "condition"
                },
                {
                    "left_side": "X",
                    "right_side": "Y",
                    "separator": "\\=",
                    "type": "condition"
                }
            ],
            "joins": [
                ",",
                ",",
                ",",
                ",",
                ","
            ],
            "name": "brother",
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
                            "value": "Q"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "W"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "E"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "_"
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
                            "value": "A"
                        },
                        {
                            "data_type": "variable",
                            "type": "atom",
                            "value": "B"
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
                        }
                    ],
                    "name": "person",
                    "type": "predicate"
                },
                {
                    "left_side": "Q",
                    "right_side": "A",
                    "separator": "=",
                    "type": "condition"
                },
                {
                    "left_side": "W",
                    "right_side": "B",
                    "separator": "=",
                    "type": "condition"
                },
                {
                    "left_side": "E",
                    "right_side": "f",
                    "separator": "=",
                    "type": "condition"
                },
                {
                    "left_side": "X",
                    "right_side": "Y",
                    "separator": "\\=",
                    "type": "condition"
                }
            ],
            "joins": [
                ",",
                ",",
                ",",
                ",",
                ","
            ],
            "name": "sister",
            "type": "fact"
        }
    ],
    "query": ["mother(X, Y)", "father(X, Y)"]
}
EXPECTED_EXECUTION_JSON_RESPONSE = {
    "data": {
        "father": [
            {
                "X": "aleh",
                "Y": "michal"
            },
            {
                "X": "andrzej",
                "Y": "larysa"
            },
            {
                "X": "andrzej",
                "Y": "maciej"
            },
            {
                "X": "wlodzimierz",
                "Y": "aleh"
            }
        ],
        "mother": [
            {
                "X": "larysa",
                "Y": "michal"
            },
            {
                "X": "ola",
                "Y": "larysa"
            },
            {
                "X": "ola",
                "Y": "maciej"
            },
            {
                "X": "ania",
                "Y": "aleh"
            }
        ]
    },
    "statusCode": 200
}

EXECUTION_BAD_DOG = {
    "data": "bad_dog(Dog):-bites(Dog, Person),is_person(Person),is_dog(Dog).bites(fido, postman).is_person(postman).is_dog(fido).",
    "query": ["bad_dog(X)"]
}
EXPECTED_EXECUTION_BAD_DOG_JSON = {'data': {'bad_dog': [{'X': 'fido'}]}, 'statusCode': 200}

EXECUTION_RECURSION = {
    "data": "oblicz(1, 0):- !.oblicz(X, Y):- Y>0, Y1 is Y - 1, oblicz(X1, Y1), X is X1 + Y.",
    "query": ["oblicz(X, 7)"]
}
EXPECTED_EXECUTION_RECURSION_JSON = {"data": {"oblicz": [{"X": "1"}, {"X": "2"}, {"X": "4"}, {"X": "7"}, {"X": "11"}, {"X": "16"}, {"X": "22"}, {"X": "29"}]}, "statusCode": 200}

EXECUTION_SIBLINGS = {
    "data": "father_child(massimo, ridge).father_child(eric, thorne).father_child(thorne, alexandria).mother_child(stephanie, chloe).mother_child(stephanie, kristen).mother_child(stephanie, felicia).parent_child(X, Y) :- father_child(X, Y).parent_child(X, Y) :- mother_child(X, Y).sibling(X, Y) :- parent_child(Z, X), parent_child(Z, Y).",
    "query": ["sibling(H, felicia)"]
}
EXPECTED_EXECUTION_SIBLINGS_JSON = {"data": {"sibling": [{"H": "chloe"}, {"H": "kristen"}, {"H": "felicia"}]}, "statusCode": 200}

EXECUTION_EINSTEIN_PUZZLE = {
    "data": """
        exists(A, list(A, _, _, _, _)).
        exists(A, list(_, A, _, _, _)).
        exists(A, list(_, _, A, _, _)).
        exists(A, list(_, _, _, A, _)).
        exists(A, list(_, _, _, _, A)).
        
        rightOf(R, L, list(L, R, _, _, _)).
        rightOf(R, L, list(_, L, R, _, _)).
        rightOf(R, L, list(_, _, L, R, _)).
        rightOf(R, L, list(_, _, _, L, R)).
        
        middle(A, list(_, _, A, _, _)).
        
        first(A, list(A, _, _, _, _)).
        
        nextTo(A, B, list(B, A, _, _, _)).
        nextTo(A, B, list(_, B, A, _, _)).
        nextTo(A, B, list(_, _, B, A, _)).
        nextTo(A, B, list(_, _, _, B, A)).
        nextTo(A, B, list(A, B, _, _, _)).
        nextTo(A, B, list(_, A, B, _, _)).
        nextTo(A, B, list(_, _, A, B, _)).
        nextTo(A, B, list(_, _, _, A, B)).
        puzzle(Houses) :-
              exists(house(red, english, _, _, _), Houses),
              exists(house(_, spaniard, _, _, dog), Houses),
              exists(house(green, _, coffee, _, _), Houses),
              exists(house(_, ukrainian, tea, _, _), Houses),
              rightOf(house(green, _, _, _, _), 
              house(ivory, _, _, _, _), Houses),
              exists(house(_, _, _, oldgold, snails), Houses),
              exists(house(yellow, _, _, kools, _), Houses),
              middle(house(_, _, milk, _, _), Houses),
              first(house(_, norwegian, _, _, _), Houses),
              nextTo(house(_, _, _, chesterfield, _), house(_, _, _, _, fox), Houses),
              nextTo(house(_, _, _, kools, _),house(_, _, _, _, horse), Houses),
              exists(house(_, _, orangejuice, luckystike, _), Houses),
              exists(house(_, japanese, _, parliament, _), Houses),
              nextTo(house(_, norwegian, _, _, _), house(blue, _, _, _, _), Houses),
              exists(house(_, _, water, _, _), Houses),
              exists(house(_, _, _, _, zebra), Houses).
        solution(WaterDrinker, ZebraOwner) :-
              puzzle(Houses),
              exists(house(_, WaterDrinker, water, _, _), Houses),
              exists(house(_, ZebraOwner, _, _, zebra), Houses).
    """,
    "query": ["solution(WaterDrinker, ZebraOwner)"]
}
EXPECTED_EINSTEIN_PUZZLE_JSON = {'data': {'solution': [{'WaterDrinker': 'norwegian', 'ZebraOwner': 'japanese'}]}, 'statusCode': 200}

EXECUTION_ALTERNATIVE_EINSTEIN_PUZZLE = {
    "data": """
    exists(A, list(A, _, _, _, _)).
        exists(A, list(_, A, _, _, _)).
        exists(A, list(_, _, A, _, _)).
        exists(A, list(_, _, _, A, _)).
        exists(A, list(_, _, _, _, A)).
        rightOf(R, L, list(L, R, _, _, _)).
        rightOf(R, L, list(_, L, R, _, _)).
        rightOf(R, L, list(_, _, L, R, _)).
        rightOf(R, L, list(_, _, _, L, R)).
        middle(A, list(_, _, A, _, _)).
        first(A, list(A, _, _, _, _)).
        nextTo(A, B, list(B, A, _, _, _)).
        nextTo(A, B, list(_, B, A, _, _)).
        nextTo(A, B, list(_, _, B, A, _)).
        nextTo(A, B, list(_, _, _, B, A)).
        nextTo(A, B, list(A, B, _, _, _)).
        nextTo(A, B, list(_, A, B, _, _)).
        nextTo(A, B, list(_, _, A, B, _)).
        nextTo(A, B, list(_, _, _, A, B)).
        puzzle(Houses) :-
              exists(house(red, british, _, _, _), Houses),
              exists(house(_, swedish, _, _, dog), Houses),
              exists(house(green, _, coffee, _, _), Houses),
              exists(house(_, danish, tea, _, _), Houses),
              rightOf(house(white, _, _, _, _), house(green, _, _, _, _), Houses),
              exists(house(_, _, _, pall_mall, bird), Houses),
              exists(house(yellow, _, _, dunhill, _), Houses),
              middle(house(_, _, milk, _, _), Houses),
              first(house(_, norwegian, _, _, _), Houses),
              nextTo(house(_, _, _, blend, _), house(_, _, _, _, cat), Houses),
              nextTo(house(_, _, _, dunhill, _),house(_, _, _, _, horse), Houses),
              exists(house(_, _, beer, bluemaster, _), Houses),
              exists(house(_, german, _, prince, _), Houses),
              nextTo(house(_, norwegian, _, _, _), house(blue, _, _, _, _), Houses),
              nextTo(house(_, _, _, blend, _), house(_, _, water_, _, _), Houses).
        solution(FishOwner) :-
          puzzle(Houses),
          exists(house(_, FishOwner, _, _, fish), Houses).
    """,
    "query": ["solution(FishOwner)"]
}
EXPECTED_ALTERNATIVE_EINSTEIN_PUZZLE_JSON = {'data': {'solution': [{'FishOwner': 'german'}]}, 'statusCode': 200}

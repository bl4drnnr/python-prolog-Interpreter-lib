import re
from ppil.ppil.api_instance.elements import Predicate, Fact, Condition, PList

ATOM_REGEX = r"[A-Za-z0-9_]+|:\-|[\[\]()\.,><;]"


def parse_atom(atoms):
    iterator = re.finditer(ATOM_REGEX, atoms)
    return [token.group() for token in iterator]


class PrologFormatChecker:
    def __init__(self):
        self._current_elem_body = []
        self._prolog_string = []
        self._parsed_json = {"data": []}

    def check_prolog_format(self, prolog_string):
        self._prolog_string = prolog_string['data'].replace('\n', '').strip().split('.')[:-1]
        return self._check_items()

    def _check_items(self):
        for elem in self._prolog_string:
            if ':-' in elem:
                pass
                # self._parse_fact(elem)
            else:
                self._parse_predicate(elem)

        return self._parsed_json

    def _parse_predicate(self, predicate):
        predicate_tokens = parse_atom(predicate)
        self._current_elem_body = predicate_tokens[2:-1]

        parsed_predicate = {
            "item": "predicate",
            "body": {}
        }

        parsed_predicate["body"]["name"] = predicate_tokens[0]
        parsed_predicate["body"]["arguments"] = self._parse_body()

        self._parsed_json["data"].append(parsed_predicate)

    def _parse_fact(self, fact):
        [fact_head, fact_body] = fact.split(':-')

        fact_name = fact_head.split('(')[0]
        fact_arguments = fact_head.split('(')[1][:-1].split(',')

        fact = Fact(
            fact_name,
            fact_arguments
        )
        self._parsed_json['data'].append(fact)

    def _parse_body(self):
        body_arguments = []
        open_list_brackets = 0
        close_list_brackets = 0
        s = ""

        for index in range(len(self._current_elem_body)):
            in_idx = index
            if self._current_elem_body[index] == '[':
                while True:
                    if open_list_brackets == close_list_brackets and open_list_brackets > 0 and close_list_brackets > 0:
                        close_list_brackets = 0
                        open_list_brackets = 0
                        break
                    s += self._current_elem_body[in_idx]

                    if self._current_elem_body[in_idx] == '[':
                        open_list_brackets += 1
                    if self._current_elem_body[in_idx] == ']':
                        close_list_brackets += 1

                    in_idx += 1

        return body_arguments

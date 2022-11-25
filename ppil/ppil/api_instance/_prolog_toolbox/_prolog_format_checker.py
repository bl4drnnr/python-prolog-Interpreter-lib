import re
from ppil.ppil.api_instance.elements import Predicate, Fact, Condition, PList

ATOM_REGEX = r"[A-Za-z0-9_]+|:\-|[\[\]()\.,]"


def parse_atom(atoms):
    iterator = re.finditer(ATOM_REGEX, atoms)
    return [token.group() for token in iterator]


class PrologFormatChecker:
    def __init__(self):
        self._prolog_string = []
        self._parsed_json = {"data": []}

    def check_prolog_format(self, prolog_string):
        self._prolog_string = prolog_string['data'].replace('\n', '').strip().split('.')[:-1]
        return self._check_items()

    def _check_items(self):
        for elem in self._prolog_string:

            if ':-' in elem:
                self._parse_fact(elem)
            else:
                self._parse_predicate(elem)

        return self._parsed_json

    def _parse_predicate(self, predicate):
        parse_atom(predicate)

    def _parse_fact(self, fact):
        [fact_head, fact_body] = fact.split(':-')

        fact_name = fact_head.split('(')[0]
        fact_arguments = fact_head.split('(')[1][:-1].split(',')

        fact = Fact(
            fact_name,
            fact_arguments
        )
        self._parsed_json['data'].append(fact)

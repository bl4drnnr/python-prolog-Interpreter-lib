import re
from ppil.ppil.api_instance._variables import CONDITION_SEPARATORS, ALLOWED_CONDITIONS
from ppil.ppil.api_instance.elements import Predicate, Fact, Condition, PList

ATOM_REGEX = r"[A-Za-z0-9_]+|:\-|[\[\]()\.,><;\+]"
NUMBER_REGEX = "^[0-9]*$"


def parse_atom(atoms):
    iterator = re.finditer(ATOM_REGEX, atoms)
    return [token.group() for token in iterator]


def serialize_predicate_body(predicate_body):
    serialized_arguments = []

    for item in predicate_body:
        if item[0] == '[' and item[-1] == ']':
            str_list = ""
            for list_symbol in item:
                if list_symbol not in ['[', ']', ','] and re.match(NUMBER_REGEX, list_symbol):
                    str_list += list_symbol
                elif list_symbol in ['[', ']', ',']:
                    str_list += list_symbol
                else:
                    str_list += f"'{list_symbol}'"

            serialized_arguments.append(PList(eval(str_list)))
        else:
            serialized_arguments.append(item)

    return serialized_arguments


def _parse_term_body(element_body, open_separator, close_separator, ignore_separators=False):
    open_separator_count = 0
    close_separator_count = 0

    items_arguments = []
    item_to_eval = ""

    while len(element_body):
        if element_body[0] == open_separator:
            inner_index = 0

            while True:
                if open_separator_count == close_separator_count and open_separator_count > 0 and close_separator_count > 0:
                    close_separator_count = 0
                    open_separator_count = 0
                    items_arguments.append(item_to_eval)
                    element_body = element_body[inner_index:]
                    item_to_eval = ""
                    break

                item_to_eval += element_body[inner_index]

                if element_body[inner_index] == open_separator:
                    open_separator_count += 1
                elif element_body[inner_index] == close_separator:
                    close_separator_count += 1

                inner_index += 1

        if len(element_body) == 0:
            break

        elem = element_body.pop(0)

        if ignore_separators:
            if elem not in ALLOWED_CONDITIONS:
                items_arguments.append(elem)
        else:
            items_arguments.append(elem)

    serialized_arguments = serialize_predicate_body(items_arguments)
    return serialized_arguments


def _serialize_fact_body(fact_body):
    conditions = []
    joins = []

    for index, atom in enumerate(fact_body):
        if atom in ALLOWED_CONDITIONS:
            joins.append(atom)

        if '(' in atom and ')' in atom:
            predicate_args = _parse_term_body(parse_atom(atom[1:-1]), '[', ']', ignore_separators=True)
            conditions.append(Predicate(fact_body[index - 1], predicate_args))

        if atom in CONDITION_SEPARATORS:
            left_side = ""
            right_side = ""

            for item in fact_body[index + 1:]:
                if item in ALLOWED_CONDITIONS:
                    break
                right_side += item

            for item in fact_body[index - 1::-1]:
                if item in ALLOWED_CONDITIONS:
                    break
                left_side += item

            conditions.append(Condition(right_side, atom, left_side))

    return [conditions, joins]


class PrologFormatChecker:
    def __init__(self):
        self._prolog_string = []
        self._parsed_json = []

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
        predicate_tokens = parse_atom(predicate)
        print(_parse_term_body(predicate_tokens[2:-1], '[', ']', ignore_separators=True))
        self._parsed_json.append(Predicate(predicate_tokens[0], _parse_term_body(predicate_tokens[2:-1], '[', ']', ignore_separators=True)))

    def _parse_fact(self, fact):
        [fact_head, fact_body] = fact.split(':-')

        fact_head_tokens = parse_atom(fact_head)
        fact_arguments = _parse_term_body(fact_head_tokens[2:-1], '[', ']', ignore_separators=True)

        parsed_fact_body = _parse_term_body(parse_atom(fact_body), '(', ')')
        print('parsed_fact_body', parsed_fact_body)
        joined_fact_body = []
        term = ""

        for item in parsed_fact_body:
            if item in ALLOWED_CONDITIONS:
                joined_fact_body.append(term)
                term = ""
            else:
                term += item
        joined_fact_body.append(term)
        print('joined_fact_body', joined_fact_body)

        # fact_body_terms = [self._parse_predicate(item, return_data=True) for item in joined_fact_body]
        [conditions, joins] = _serialize_fact_body(parsed_fact_body)

        self._parsed_json.append(Fact(
            fact_head_tokens[0],
            fact_arguments,
            joins,
            conditions
        ))

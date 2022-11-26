import re
from ppil.ppil.api_instance._variables import CONDITION_SEPARATORS, ALLOWED_CONDITIONS

ATOM_REGEX = r"[A-Za-z0-9_]+|:\-|[\[\]()\.,><;\+]"
NUMBER_REGEX = "^[0-9]*$"


def parse_atom(atoms):
    iterator = re.finditer(ATOM_REGEX, atoms)
    return [token.group() for token in iterator]


def serialize_predicate_body(predicate_body):
    serialized_arguments = []

    for item in predicate_body:
        if item[0] == '[' and item[-1] == ']':
            parsed_list = {
                "type": "list",
                "items": []
            }

            str_list = ""
            for list_symbol in item:
                if list_symbol not in ['[', ']', ','] and re.match(NUMBER_REGEX, list_symbol):
                    str_list += list_symbol
                elif list_symbol in ['[', ']', ',']:
                    str_list += list_symbol
                else:
                    str_list += f"'{list_symbol}'"

            parsed_list["items"].append(eval(str_list))
            serialized_arguments.append(parsed_list)
        else:
            serialized_arguments.append(item)

    return serialized_arguments


class PrologFormatChecker:
    def __init__(self):
        self._current_elem_body = []
        self._prolog_string = []
        self._parsed_json = {"data": []}

    def check_prolog_format(self, prolog_string):
        self._prolog_string = prolog_string['data'].replace('\n', '').strip().split('.')[:-1]
        return self._check_items()

    def _pop_current_elem_body(self):
        return self._current_elem_body.pop(0)

    def _get_current_elem_body(self):
        return self._current_elem_body[0]

    def _slice_current_elem_body(self, index):
        self._current_elem_body = self._current_elem_body[index:]

    def _check_items(self):
        for elem in self._prolog_string:
            if ':-' in elem:
                self._parse_fact(elem)
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
        parsed_predicate["body"]["arguments"] = self._parse_term_body('[', ']', ignore_separators=True)

        self._parsed_json["data"].append(parsed_predicate)

    def _parse_fact(self, fact):
        [fact_head, fact_body] = fact.split(':-')
        
        parsed_fact = {
            "item": "fact",
            "body": {}
        }

        fact_head_tokens = parse_atom(fact_head)
        self._current_elem_body = fact_head_tokens[2:-1]

        parsed_fact["body"]["name"] = fact_head_tokens[0]
        parsed_fact["body"]["arguments"] = self._parse_term_body('[', ']', ignore_separators=True)

        self._current_elem_body = parse_atom(fact_body)
        parsed_fact_body = self._parse_term_body('(', ')')
        [conditions, joins] = self._serialize_fact_body(parsed_fact_body)

        parsed_fact["body"]["joins"] = joins
        parsed_fact["body"]["conditions"] = conditions

        self._parsed_json["data"].append(parsed_fact)

    def _parse_term_body(self, open_separator, close_separator, ignore_separators=False):
        open_separator_count = 0
        close_separator_count = 0
        
        items_arguments = []
        item_to_eval = ""

        while len(self._current_elem_body):
            if self._get_current_elem_body() == open_separator:
                inner_index = 0

                while True:
                    if open_separator_count == close_separator_count and open_separator_count > 0 and close_separator_count > 0:
                        close_separator_count = 0
                        open_separator_count = 0
                        items_arguments.append(item_to_eval)
                        self._slice_current_elem_body(inner_index)
                        item_to_eval = ""
                        break

                    item_to_eval += self._current_elem_body[inner_index]

                    if self._current_elem_body[inner_index] == open_separator:
                        open_separator_count += 1
                    elif self._current_elem_body[inner_index] == close_separator:
                        close_separator_count += 1

                    inner_index += 1

            if len(self._current_elem_body) == 0:
                break

            elem = self._pop_current_elem_body()

            if ignore_separators:
                if elem not in ALLOWED_CONDITIONS:
                    items_arguments.append(elem)
            else:
                items_arguments.append(elem)

        serialized_arguments = serialize_predicate_body(items_arguments)
        return serialized_arguments

    def _serialize_fact_body(self, fact_body):
        conditions = []
        joins = []

        for index, atom in enumerate(fact_body):
            if atom in ALLOWED_CONDITIONS:
                joins.append(atom)

            if '(' in atom and ')' in atom:
                self._current_elem_body = parse_atom(atom[1:-1])
                predicate_args = self._parse_term_body('[', ']', ignore_separators=True)
                conditions.append({
                    "type": "predicate",
                    "name": fact_body[index - 1],
                    "items": predicate_args
                })

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

                conditions.append({
                    "type": "condition",
                    "separator": atom,
                    "left_side": right_side,
                    "right_side": left_side
                })

        return [conditions, joins]

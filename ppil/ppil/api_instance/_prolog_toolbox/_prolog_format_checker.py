import re
from ppil.ppil.api_instance.elements import Predicate, Fact, PList, Atom

ATOM_REGEX = r"[A-Za-z0-9_]+|:\-|[\[\]()\.,><;\+\']"
NUMBER_REGEX = "^[0-9]*$"
VARIABLE_REGEX = r"^[A-Z_][A-Za-z0-9_]*$"


def _parse_atom(atoms):
    iterator = re.finditer(ATOM_REGEX, atoms)
    return [token.group() for token in iterator]


class PrologFormatChecker:
    def __init__(self):
        self._prolog_string = []
        self._parsed_json = []
        self._joins = []

    def check_prolog_format(self, prolog_string):
        self._reset_data()
        self._prolog_string = _parse_atom(prolog_string['data'].replace('\n', '').strip())
        return self._check_items()

    def _reset_data(self):
        self._prolog_string = []
        self._parsed_json = []
        self._joins = []

    def _get_current_prolog_element(self):
        return self._prolog_string[0]

    def _pop_current_prolog_element(self):
        return self._prolog_string.pop(0)

    def _check_items(self):
        while len(self._prolog_string) > 0:
            self._parsed_json.append(self._parse_item())
        return self._parsed_json

    def _parse_item(self):
        item_predicate = self._parse_term()

        if self._get_current_prolog_element() == ".":
            self._pop_current_prolog_element()
            return item_predicate

        self._pop_current_prolog_element()

        arguments = []

        while self._get_current_prolog_element() != ".":
            arguments.append(self._parse_term())

            if self._get_current_prolog_element() == "," or self._get_current_prolog_element() == ";":
                separator = self._pop_current_prolog_element()
                self._joins.append(separator)

        self._pop_current_prolog_element()

        tail = arguments[0] if arguments == 1 else arguments

        f = Fact(item_predicate.name, item_predicate, self._joins, tail)
        self._joins = []
        return f

    def _parse_term(self):
        if self._get_current_prolog_element() == "(":
            self._pop_current_prolog_element()
            return self._parse_arguments(")")
        elif self._get_current_prolog_element() == "[":
            self._pop_current_prolog_element()
            return self._parse_arguments("]")

        functor = self._pop_current_prolog_element()

        if self._get_current_prolog_element() != "(":
            if functor == '\'':
                elem = self._pop_current_prolog_element()
                self._pop_current_prolog_element()
                return Atom(elem, 'string')
            elif functor.isdigit():
                return Atom(functor, 'number')
            elif re.match(VARIABLE_REGEX, functor) is not None:
                return Atom(functor, 'variable')
            else:
                return Atom(functor, 'atom')

        self._pop_current_prolog_element()
        return Predicate(functor, self._parse_arguments(")"))

    def _parse_arguments(self, separator):
        list_of_arguments = []

        while self._get_current_prolog_element() != separator:
            list_of_arguments.append(self._parse_term())

            if self._get_current_prolog_element() == ',':
                self._pop_current_prolog_element()

        self._pop_current_prolog_element()
        return PList(list_of_arguments)

import re
from src.ppil.elements import ArgumentsQueryConnector, Variable, Term, TrueStatement, Rule

ATOM_NAME_REGEX = r"^[A-Za-z0-9_]+$"
VARIABLE_REGEX = r"^[A-Z_][A-Za-z0-9_]*$"
TOKEN_REGEX = r"[A-Za-z0-9_]+|:\-|[()\.,]"


def _parse_elems_from_string(input_text):
    iterator = re.finditer(TOKEN_REGEX, input_text)
    return [token.group() for token in iterator]


class Parser:
    def __init__(self, input_text):
        self._elems = _parse_elems_from_string(input_text)
        self._variables = {}

    def parse_rules(self):
        rules = []

        while len(self._elems) > 0:
            self._variables = {}
            rules.append(self._parse_rule())

        return rules

    def parse_query(self):
        return self._parse_term()

    def _get_current_elem(self):
        return self._elems[0]

    def _pop_current_elem(self):
        return self._elems.pop(0)

    def _parse_atom(self):
        name = self._pop_current_elem()

        if re.match(ATOM_NAME_REGEX, name) is None:
            raise Exception("Invalid Atom Name: " + str(name))

        return name

    def _parse_term(self):
        if self._get_current_elem() == "(":
            return self._create_list_of_arguments()

        functor = self._parse_atom()

        if re.match(VARIABLE_REGEX, functor) is not None:
            return self._get_variable(functor)
        if self._get_current_elem() != "(":
            return Term(functor)

        self._pop_current_elem()
        return Term(functor, self._parse_arguments())

    def _parse_arguments(self):
        arguments = []

        while self._get_current_elem() != ")":
            arguments.append(self._parse_term())

            if self._get_current_elem() not in [",", ")"]:
                raise Exception("Expected , or ) in term but got " + str(self._get_current_elem()))

            if self._get_current_elem() == ",":
                self._pop_current_elem()

        self._pop_current_elem()
        return arguments

    def _parse_rule(self):
        head = self._parse_term()

        if self._get_current_elem() == ".":
            self._pop_current_elem()
            return Rule(head, TrueStatement())

        if self._get_current_elem() != ":-":
            raise Exception("Expected :- in rule but got " + str(self._get_current_elem()))

        self._pop_current_elem()

        arguments = []

        while self._get_current_elem() != ".":
            arguments.append(self._parse_term())

            if self._get_current_elem() not in [",", "."]:
                raise Exception("Expected , or . in term but got " + str(self._get_current_elem()))

            if self._get_current_elem() == ",":
                self._pop_current_elem()

        self._pop_current_elem()

        if arguments == 1:
            tail = arguments[0]
        else:
            tail = ArgumentsQueryConnector(arguments)

        return Rule(head, tail)

    def _get_variable(self, atom):
        variable = self._variables.get(atom)

        if atom == "_":
            return Variable("_")

        if variable is None:
            self._variables[atom] = Variable(atom)
            variable = self._variables[atom]

        return variable

    def _create_list_of_arguments(self):
        self._pop_current_elem()
        return ArgumentsQueryConnector(self._parse_arguments())

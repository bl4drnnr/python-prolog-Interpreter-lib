import re
from .interpreter import Conjunction, Variable, Term, TRUE, Rule
from .elem_regex import TOKEN_REGEX, ATOM_NAME_REGEX, VARIABLE_REGEX


def _parse_elems_from_string(input_text):
    iterator = re.finditer(TOKEN_REGEX, input_text)
    return [token.group() for token in iterator]


class Parser(object):
    def __init__(self, input_text):
        self._elems = _parse_elems_from_string(input_text)
        self._scope = None

    def parse_rules(self):
        rules = []

        while self._elems:
            self._scope = {}
            rules.append(self._parse_rule())

        return rules

    def parse_query(self):
        self._scope = {}
        return self._parse_term()

    @property
    def _current(self):
        return self._elems[0]

    def _pop_current(self):
        return self._elems.pop(0)

    def _parse_atom(self):
        name = self._pop_current()

        if re.match(ATOM_NAME_REGEX, name) is None:
            raise Exception("Invalid Atom Name: " + str(name))

        return name

    def _parse_term(self):
        if self._current == "(":
            self._pop_current()
            arguments = self._parse_arguments()
            return Conjunction(arguments)

        functor = self._parse_atom()

        if re.match(VARIABLE_REGEX, functor) is not None:

            if functor == "_":
                return Variable("_")

            variable = self._scope.get(functor)

            if variable is None:
                self._scope[functor] = Variable(functor)
                variable = self._scope[functor]

            return variable

        if self._current != "(":
            return Term(functor)

        self._pop_current()
        arguments = self._parse_arguments()
        return Term(functor, arguments)

    def _parse_arguments(self):
        arguments = []

        while self._current != ")":
            arguments.append(self._parse_term())

            if self._current not in (",", ")"):
                raise Exception("Expected , or ) in term but got " + str(self._current))

            if self._current == ",":
                self._pop_current()

        self._pop_current()
        return arguments

    def _parse_rule(self):
        head = self._parse_term()

        if self._current == ".":
            self._pop_current()
            return Rule(head, TRUE())

        if self._current != ":-":
            raise Exception("Expected :- in rule but got " + str(self._current))

        self._pop_current()

        arguments = []

        while self._current != ".":
            arguments.append(self._parse_term())

            if self._current not in (",", "."):
                raise Exception("Expected , or . in term but got " + str(self._current))

            if self._current == ",":
                self._pop_current()

        self._pop_current()

        tail = arguments[0] if arguments == 1 else Conjunction(arguments)
        return Rule(head, tail)

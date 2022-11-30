import re
from ppil.ppil.api_instance.elements import Predicate, Fact, PList, Atom, Condition, ConditionStatement
from ppil.ppil.api_instance._variables import CONDITION_SEPARATORS

ATOM_REGEX = r"[A-Za-z0-9_]+|:\-|[\[\]()\.,><;\+\'-\|]"
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

        self._check_conditions()
        self._check_lists()

        return [item for item in self._parsed_json if not isinstance(item, Atom)]

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

    def _check_conditions(self):
        for item in self._parsed_json:
            if isinstance(item, Fact):
                for c in item.conditions:
                    if isinstance(c, PList):
                        left_separator_index = None
                        right_separator_index = None
                        clause_separator_index = None

                        for index, k in enumerate(c.items):
                            if \
                                    isinstance(k, Atom) and \
                                    isinstance(c.items[index + 1], Atom) and \
                                    k.atom == '-' and \
                                    c.items[index + 1].atom == '>':
                                left_separator_index = index
                                right_separator_index = index + 1
                            if isinstance(k, Atom) and k.atom == ';':
                                clause_separator_index = index

                        condition_statement = c.items[:left_separator_index]
                        then_clause = c.items[right_separator_index:][1:clause_separator_index - len(condition_statement) - 1]
                        else_clause = c.items[right_separator_index:][clause_separator_index - len(condition_statement):]

                        condition = None
                        for index, condition_atom in enumerate(condition_statement):
                            if condition_atom.atom in CONDITION_SEPARATORS:
                                right_side = [item.atom for item in condition_statement[index + 1:]]
                                left_side = [item.atom for item in condition_statement[:index]]
                                condition = Condition(
                                    ''.join(left_side),
                                    condition_atom.atom,
                                    ''.join(right_side)
                                )
                                break

                        item.conditions.append(ConditionStatement(condition, then_clause, else_clause))
                        item.conditions.remove(c)

        for item in self._parsed_json:
            if isinstance(item, Fact):
                fact_atoms = []
                separator = ""

                for condition in item.conditions:
                    if isinstance(condition, Atom):
                        fact_atoms.append(condition)

                fact_atom_str = ""
                for atom in fact_atoms:
                    if atom.atom in CONDITION_SEPARATORS:
                        separator = atom.atom
                    fact_atom_str += atom.atom

                if len(separator):
                    [left_side, right_side] = fact_atom_str.split(separator)
                    item.conditions.append(Condition(left_side, separator, right_side))

    def _check_lists(self):
        for item in self._parsed_json:
            if isinstance(item, Fact):
                fact_arguments = []
                item_to_replace = None
                replace_index = None

                for index, argument in enumerate(item.arguments.arguments.items):
                    if isinstance(argument, PList):
                        item_to_replace = argument
                        replace_index = index
                        for item_list in argument.items:
                            fact_arguments.append(item_list)

                if len(fact_arguments) == 3 and fact_arguments[1].atom == '|':
                    item.arguments.arguments.items.remove(item_to_replace)
                    item.arguments.arguments.items.insert(
                        replace_index,
                        PList([], fact_arguments[0], fact_arguments[2])
                    )


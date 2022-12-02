import re
from ppil.ppil.elements import Predicate, Fact, PList, Atom, Condition, ConditionStatement, Separator
from ppil.ppil._variables import CONDITION_SEPARATORS, CONDITION_STRING_SEPARATOR

ATOM_REGEX = r"[A-Za-z0-9_]+|:\-|[\[\]()\.,><;\+\'-\|]"
NUMBER_REGEX = "^[0-9]*$"
VARIABLE_REGEX = r"^[A-Z_][A-Za-z0-9_]*$"


def _parse_atom(atoms):
    iterator = re.finditer(ATOM_REGEX, atoms)
    return [token.group() for token in iterator]


def _find_all_condition_statements(fact_condition):
    left_separator_index = None
    right_separator_index = None
    clause_separator_index = None

    for index, k in enumerate(fact_condition.items):
        if \
                isinstance(k, Atom) and \
                isinstance(fact_condition.items[index + 1], Atom) and \
                k.atom == '-' and \
                fact_condition.items[index + 1].atom == '>':
            left_separator_index = index
            right_separator_index = index + 1
        if isinstance(k, Atom) and k.atom == ';':
            clause_separator_index = index

    condition_statement = fact_condition.items[:left_separator_index]
    else_clause = fact_condition.items[right_separator_index:][1:clause_separator_index - len(condition_statement) - 1]
    then_clause = fact_condition.items[right_separator_index:][clause_separator_index - len(condition_statement):]

    for index, condition_atom in enumerate(condition_statement):
        right_side = ''.join([item.atom for item in condition_statement[index + 1:]])
        left_side = ''.join([item.atom for item in condition_statement[:index]])
        condition = Condition(left_side, condition_atom.atom, right_side)
        return [condition, else_clause, then_clause]


def _find_all_conditions(conditions):
    fact_atoms = []
    not_atom_index = 0
    fact_atom_str = ""
    replace_indexes = []

    for index, condition in enumerate(conditions):
        current_index = index if index + 1 == len(conditions) else index + 1

        if isinstance(condition, Atom) and isinstance(conditions[current_index], Atom):
            fact_atoms.append({'condition': condition, 'not_atom_index': not_atom_index})
        elif isinstance(condition, Atom) and not isinstance(conditions[current_index], Atom):
            fact_atoms.append({'condition': condition, 'not_atom_index': not_atom_index})
            fact_atoms.append(Atom(CONDITION_STRING_SEPARATOR))
        if not isinstance(condition, Atom):
            not_atom_index += 1

    for atom in fact_atoms:
        if isinstance(atom, Atom):
            fact_atom_str += atom.atom
        elif atom.get('condition'):
            fact_atom_str += atom['condition'].atom

    for atom in fact_atoms[::-1]:
        if not isinstance(atom, Atom) and atom['not_atom_index'] not in replace_indexes:
            replace_indexes.append(atom['not_atom_index'])

    item_conditions_copy = conditions[:]
    item_conditions_copy = [item for item in item_conditions_copy if not isinstance(item, Atom)]

    fact_atom_str = fact_atom_str.split(CONDITION_STRING_SEPARATOR)
    fact_atom_str.reverse()

    fact_atom_str = [fas for fas in fact_atom_str if len(fas) > 0]
    for index, condition in enumerate(fact_atom_str):
        separator = None

        for condition_symbol in CONDITION_SEPARATORS:
            if condition_symbol in condition:
                separator = condition_symbol
                break

        [left_side, right_side] = condition.split(separator)
        item_conditions_copy.insert(replace_indexes[index], Condition(left_side, separator, right_side))

    return item_conditions_copy


def _check_argument_lists(arguments):
    fact_arguments = []
    item_to_replace = None
    replace_index = None

    for index, argument in enumerate(arguments.arguments.items):
        if isinstance(argument, PList):
            item_to_replace = argument
            replace_index = index
            for item_list in argument.items:
                fact_arguments.append(item_list)

    if len(fact_arguments) == 3 and fact_arguments[1].atom == '|':
        arguments.arguments.items.remove(item_to_replace)
        arguments.arguments.items.insert(replace_index, PList([], fact_arguments[0], fact_arguments[2]))

    return arguments


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

        self._check_condition_statements_and_lists()

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

                if isinstance(arguments[-1], Atom):
                    arguments.append(Separator())

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

    def _check_condition_statements_and_lists(self):
        for item in self._parsed_json:
            if isinstance(item, Fact):

                for idx, c in enumerate(item.conditions):
                    if isinstance(c, PList):

                        [condition, else_clause, then_clause] = _find_all_condition_statements(c)

                        item_conditions_copy = item.conditions[:]
                        item_conditions_copy.insert(idx, ConditionStatement(condition, then_clause, else_clause))
                        item_conditions_copy.remove(c)
                        item.conditions = item_conditions_copy

                if len(item.conditions) > 1:
                    item.conditions = _find_all_conditions(item.conditions)
                item.arguments = _check_argument_lists(item.arguments)

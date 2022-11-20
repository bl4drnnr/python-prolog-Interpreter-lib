import re
import pcre
from .interpreter import Conjunction, Variable, Term, TRUE, Rule
from .elem_regex import VARIABLE_REGEX, ARGUMENTS_REGEX


def _parse_atom(rule):
    return rule.split('(')[0]


def _check_if_term_is_rule(term):
    return ':-' in term


def _check_rule_format(rule):
    if '(' not in rule or ')' not in rule:
        raise Exception(f"Invalid rule format: {rule}")


def _split_database_string(input_text):
    split_database = input_text.split('.')
    split_database = [item.strip().replace(" ", "").replace("\n", "") for item in split_database]
    return split_database[:-1]


def _parse_internal_rule(rule):
    data = pcre.findall(ARGUMENTS_REGEX, rule)
    filtered_data = [i[1] for i in data]
    all_predicates = filtered_data[0]
    res = {}

    for i in filtered_data[1:]:
        index = rule.find(i)
        predicates_list = rule[:index].split('(')[:-1][-1]

        found_predicate = ''
        for sym in predicates_list[::-1]:
            if sym in [',', ';']:
                break
            found_predicate += sym

        res[found_predicate[::-1]] = i

    predicate = ''
    for i in all_predicates:
        if i in [',', ';'] and '(' not in predicate and ')' not in predicate:
            if predicate not in res:
                res[predicate] = None
                predicate = ''
                continue
        if '(' in predicate and ')' in predicate:
            predicate = ''
        predicate += i

    return res


class Parser(object):
    def __init__(self, input_text):
        self._current_rule = None
        self._variables = None
        self._input_text = input_text
        self._elems = _split_database_string(input_text)

    def parse_rules(self):
        parsed_rules = []

        for elem in self._elems:
            self._variables = {}
            parsed_rules.append(self._parse_rule(elem))

        return parsed_rules

    def parse_query(self):
        self._variables = {}
        query = self._input_text.strip().replace(" ", "")

        functor = _parse_atom(query)
        arguments = self._parse_arguments(query)
        return Term(functor, arguments)

    def _parse_tail(self, tail):
        if not len(tail):
            return None

        parsed_tail = []
        split_tail = tail.split('),')

        for item in split_tail:
            if '(' in item and ')' not in item:
                parsed_tail.append(item + ')')
            else:
                parsed_tail.append(item)

        tail_terms = [self._parse_term(item) for item in parsed_tail]
        return Conjunction(tail_terms)

    def _parse_term(self, rule):
        try:
            [head, tail] = rule.split(':-')
        except (Exception,):
            head = rule
            tail = []

        functor = _parse_atom(head)
        arguments = self._parse_arguments(head)
        parsed_tail = self._parse_tail(tail)

        return [Term(functor, arguments), parsed_tail] \
            if parsed_tail \
            else Term(functor, arguments)

    def _parse_arguments(self, rule):
        parsed_rule = _parse_internal_rule(rule)
        parsed_arguments = []

        for parsed_rule_key, parsed_rule_value in parsed_rule.items():
            if re.match(VARIABLE_REGEX, parsed_rule_key) is not None:
                if parsed_rule_key == "_":
                    return Variable("_")

                variable = self._variables.get(parsed_rule_key)

                if variable is None:
                    self._variables[parsed_rule_key] = Variable(parsed_rule_key)
                    variable = self._variables[parsed_rule_key]

                parsed_arguments.append(variable)
            else:
                if parsed_rule_value is None:
                    parsed_arguments.append(Term(parsed_rule_key))
                else:
                    args = [Term(a) for a in parsed_rule_value.split(',')]
                    parsed_arguments.append(Term(parsed_rule_key, args))

        return parsed_arguments

    def _parse_rule(self, rule):
        term_head = self._parse_term(rule)

        if _check_if_term_is_rule(rule):
            return Rule(term_head[0], term_head[1])
        else:
            return Rule(term_head, TRUE())

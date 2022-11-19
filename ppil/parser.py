import re
from .interpreter import Conjunction, Variable, Term, TRUE, Rule
from .regex import ELEM_REGEX, ATOM_NAME_REGEX, VARIABLE_REGEX


def _check_if_term_is_rule(term):
    return ':-' in term


def _check_rule_format(rule):
    if '(' not in rule or ')' not in rule:
        raise Exception(f"Invalid rule format: {rule}")


def _split_database_string(input_text):
    split_database = input_text.split('.')
    split_database = [item.strip().replace(" ", "") for item in split_database]
    return split_database[:-1]


class Parser(object):
    def __init__(self, input_text):
        self._input_text = input_text
        self._elems = _split_database_string(input_text)

    def parse_rules(self):
        return [self._parse_rule(elem) for elem in self._elems]

    def parse_query(self):
        query = self._input_text.strip().replace(" ", "")
        functor = self._parse_atom(query)
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

    def _parse_atom(self, rule):
        return rule.split('(')[0]

    def _parse_term(self, rule):
        try:
            [head, tail] = rule.split(':-')
        except (Exception,):
            head = rule
            tail = []

        functor = self._parse_atom(head)
        arguments = self._parse_arguments(head)
        parsed_tail = self._parse_tail(tail)

        return [Term(functor, arguments), parsed_tail] \
            if parsed_tail \
            else Term(functor, arguments)

    def _parse_arguments(self, rule):
        parsed_arguments = []

        for item in rule.split(','):
            if '(' in item:
                rule = Term(item.split('(')[1])
            elif ')' in item:
                rule = Term(item.split(')')[0])
            else:
                rule = Term(item)
            parsed_arguments.append(rule)

        return parsed_arguments

    def _parse_rule(self, rule):
        term_head = self._parse_term(rule)

        if _check_if_term_is_rule(rule):
            return Rule(term_head[0], term_head[1])
        else:
            return Rule(term_head, TRUE())

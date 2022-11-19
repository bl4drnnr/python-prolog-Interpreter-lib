import re
from .interpreter import Conjunction, Variable, Term, TRUE, Rule
from .regex import ELEM_REGEX, ATOM_NAME_REGEX, VARIABLE_REGEX


def check_if_term_is_rule(term):
    return ':-' in term


def check_rule_format(rule):
    if '(' not in rule or ')' not in rule:
        raise Exception(f"Invalid rule format: {rule}")


def split_database_string2(input_text):
    split_database = input_text.split('.')
    split_database = [item.strip().replace(" ", "") for item in split_database]
    return split_database[:-1]


def split_database_string(input_text):
    iterator = re.finditer(ELEM_REGEX, input_text)
    return [elem.group() for elem in iterator]


class Parser(object):
    def __init__(self, input_text):
        self._input_text = input_text
        self._elems2 = split_database_string2(input_text)

    def parse_rules(self):
        rules2 = []
        for elem in self._elems2:
            rules2.append(self._parse_rule2(elem))
        return rules2

    def parse_query2(self):
        text = self._input_text.strip().replace(" ", "")
        functor = self._parse_atom2(text)

        parsed_arguments = []

        for item in text.split(','):
            if '(' in item:
                parsed_arguments.append(item.split('(')[1])
            elif ')' in item:
                parsed_arguments.append(item.split(')')[0])
            else:
                parsed_arguments.append(item)

        t = []
        for i in parsed_arguments:
            t.append(Term(i))
        return Term(functor, t)

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

        tail_terms = [self._parse_term2(item) for item in parsed_tail]
        return Conjunction(tail_terms)

    def _parse_atom2(self, rule):
        return rule.split('(')[0]

    def _parse_term2(self, rule):
        try:
            [head, tail] = rule.split(':-')
        except (Exception,):
            head = rule
            tail = []

        functor = self._parse_atom2(head)
        arguments = self._parse_arguments2(head)
        parsed_tail = self._parse_tail(tail)

        return [Term(functor, arguments), parsed_tail] \
            if parsed_tail \
            else Term(functor, arguments)

    def _parse_arguments2(self, rule):
        parsed_arguments = []

        for item in rule.split(','):
            if '(' in item:
                parsed_arguments.append(item.split('(')[1])
            elif ')' in item:
                parsed_arguments.append(item.split(')')[0])
            else:
                parsed_arguments.append(item)

        t = []
        for i in parsed_arguments:
            t.append(Term(i))

        return t

    def _parse_rule2(self, rule):
        term_head = self._parse_term2(rule)

        if check_if_term_is_rule(rule):
            return Rule(term_head[0], term_head[1])
        else:
            return Rule(term_head, TRUE())

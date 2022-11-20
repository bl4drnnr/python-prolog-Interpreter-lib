import re
from .interpreter import Conjunction, Variable, Term, TRUE, Rule
from .regex import VARIABLE_REGEX, ARGUMENTS_REGEX


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
        a = re.findall(ARGUMENTS_REGEX, rule)[0].split('(')[1].split(')')[0]
        arguments = a.split(',') if ',' in a else [a]

        parsed_arguments = []

        for parsed_rule_string in arguments:
            if re.match(VARIABLE_REGEX, parsed_rule_string) is not None:
                if parsed_rule_string == "_":
                    return Variable("_")

                variable = self._variables.get(parsed_rule_string)

                if variable is None:
                    self._variables[parsed_rule_string] = Variable(parsed_rule_string)
                    variable = self._variables[parsed_rule_string]

                parsed_arguments.append(variable)
            else:
                parsed_arguments.append(Term(parsed_rule_string))
            self._current_rule = Term(parsed_rule_string)

        return parsed_arguments

    def _parse_rule(self, rule):
        term_head = self._parse_term(rule)

        if _check_if_term_is_rule(rule):
            return Rule(term_head[0], term_head[1])
        else:
            return Rule(term_head, TRUE())

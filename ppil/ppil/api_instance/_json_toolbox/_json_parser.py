from ppil.ppil.api_instance.elements import PList


def parse_predicate_arguments(arguments):
    predicate_arguments = ""

    for arg in arguments:
        if isinstance(arg, str):
            predicate_arguments += f"{arg}, "
        elif isinstance(arg, PList):
            predicate_arguments += f"{str(arg.items)}, "

    return predicate_arguments


class JsonParser:
    def __init__(self):
        self._output_program = ''

    def _parse_json_predicates(self, predicates):
        for predicate in predicates:
            predicate_arguments = parse_predicate_arguments(predicate.arguments)
            self._output_program += f"{predicate.name}({predicate_arguments[:-2]}).\n"

    def _parse_json_facts(self, facts):
        for fact in facts:
            self._output_program += f"{fact.name}({', '.join(fact.arguments)}):-"

            for index, condition in enumerate(fact.conditions):
                if condition.type == 'predicate':
                    condition_arguments = parse_predicate_arguments(condition.arguments)
                    self._output_program += f"{condition.name}({condition_arguments[:-2]})"

                if condition.type == 'condition':
                    self._output_program += f"{condition.left_side} {condition.separator} {condition.right_side}"

                if len(fact.joins):
                    if index + 1 < len(fact.conditions):
                        self._output_program += fact.joins[index]

            self._output_program += '.\n'

    def parse_json(self, json):
        self._parse_json_predicates(json.get('predicates'))
        self._parse_json_facts(json.get('facts'))

        return self._output_program

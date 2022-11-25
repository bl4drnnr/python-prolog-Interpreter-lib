class JsonParser:
    def __init__(self):
        self._output_program = ''

    def _parse_json_predicates(self, predicates):
        for predicate in predicates:
            self._output_program += f"{predicate.name}({', '.join(predicate.arguments)}).\n"

    def _parse_json_facts(self, facts):
        for fact in facts:
            self._output_program += f"{fact.name}({', '.join(fact.arguments)}):-"
            for index, condition in enumerate(fact.conditions):
                if condition.type == 'predicate':
                    self._output_program += f"{condition.name}({', '.join(condition.arguments)})"
                if len(fact.joins):
                    if index + 1 < len(fact.conditions):
                        self._output_program += fact.joins[index]
            self._output_program += '.\n'

    def _parse_json_lists(self, lists):
        for p_list in lists:
            self._output_program += f"{p_list.name}={p_list.items}.\n"

    def parse_json(self, json):
        self._parse_json_predicates(json.get('predicates'))
        self._parse_json_lists(json.get('lists'))
        self._parse_json_facts(json.get('facts'))

        return self._output_program

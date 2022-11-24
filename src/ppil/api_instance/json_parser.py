class JsonParser:
    def __init__(self):
        self._output_program = ''

    def _parse_json_predicates(self, predicates):
        for predicate in predicates:
            self._output_program += f"{predicate.get('name')}({', '.join(predicate.get('arguments'))}).\n"

    def _parse_json_facts(self, facts):
        for fact in facts:
            self._output_program += f"{fact.get('name')}({', '.join(fact.get('arguments'))}):-"
            for index, condition in enumerate(fact.get('conditions')):
                if condition.get('type') == 'predicate':
                    self._output_program += f"{condition.get('name')}({', '.join(condition.get('arguments'))})"
                if len(fact.get('joins')):
                    if index + 1 < len(fact.get('conditions')):
                        self._output_program += fact.get('joins')[index]
            self._output_program += '.\n'

    def _parse_json_lists(self, lists):
        for p_list in lists:
            self._output_program += f"{p_list.get('name')}={p_list.get('items')}"

    def parse_json(self, json):
        self._parse_json_predicates(json.get('predicates'))
        self._parse_json_lists(json.get('lists'))
        self._parse_json_facts(json.get('facts'))

        return self._output_program

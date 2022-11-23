from .api_response_handler import WrongFactFormat, WrongJsonFormat, ApiResponse
from .format_parser import FormatParser


class JsonConverter:
    def __init__(self):
        self._output_program = ''

    def json_to_prolog(self, input_json_data):
        try:
            data = FormatParser.check_json_format(input_json_data)

            self._parse_predicates(data.get('predicates'))
            self._parse_facts(data.get('facts'))
            self._parse_lists(data.get('lists'))

            return ApiResponse(self._output_program, 200)
        except WrongJsonFormat:
            return WrongJsonFormat()
        except WrongFactFormat:
            return WrongFactFormat()
        except Exception as e:
            return ApiResponse(str(e), 500)

    def prolog_to_json(self, input_json_data):
        try:
            return ApiResponse(self._output_program, 200)
        except Exception as e:
            return ApiResponse(str(e), 500)

    def json_execute(self, input_json_data):
        try:
            return ApiResponse(self._output_program, 200)
        except Exception as e:
            return ApiResponse(str(e), 500)

    def prolog_execute(self, input_json_data):
        try:
            return ApiResponse(self._output_program, 200)
        except Exception as e:
            return ApiResponse(str(e), 500)

    def _parse_predicates(self, predicates):
        for predicate in predicates:
            self._output_program += f"{predicate.get('name')}({', '.join(predicate.get('arguments'))}).\n"

    def _parse_facts(self, facts):
        for fact in facts:
            self._output_program += f"{fact.get('name')}({', '.join(fact.get('arguments'))}):-"
            for index, condition in enumerate(fact.get('conditions')):
                if condition.get('type') == 'predicate':
                    self._output_program += f"{condition.get('name')}({', '.join(condition.get('arguments'))})"
                if len(fact.get('joins')):
                    if index + 1 < len(fact.get('conditions')):
                        self._output_program += fact.get('joins')[index]
            self._output_program += '.\n'

    def _parse_lists(self, lists):
        for p_list in lists:
            self._output_program += f"{p_list.get('name')}={p_list.get('items')}"

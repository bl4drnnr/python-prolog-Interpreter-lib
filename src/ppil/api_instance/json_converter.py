import json
from .api_response_handler import WrongFactFormat, WrongJsonFormat, ApiResponse

JSON_FORMAT = {
    "predicate": {
        "name": "str",
        "arguments": "list"
    },
    "fact": {
        "name": "str",
        "arguments": "list",
        "conditions": "list",
        "joins": "list"
    },
    "list": {
        "name": "str",
        "items": "list"
    }
}

ALLOWED_CONDITIONS = ['and', ',', 'or', ';']
ALLOWED_CONDITIONS_TYPES = ['predicate']


class JsonConverter:
    def __init__(self):
        pass

    @classmethod
    def json_to_prolog(cls, input_json_data):
        try:
            output_program = ''

            data = cls._check_json_format(input_json_data)

            for predicate in data.get('predicates'):
                output_program += f"{predicate.get('name')}({', '.join(predicate.get('arguments'))}).\n"

            for fact in data.get('facts'):
                output_program += f"{fact.get('name')}({', '.join(fact.get('arguments'))}):-"
                for index, condition in enumerate(fact.get('conditions')):
                    if condition.get('type') == 'predicate':
                        output_program += f"{condition.get('name')}({', '.join(condition.get('arguments'))})"
                    if len(fact.get('joins')):
                        if index + 1 < len(fact.get('conditions')):
                            output_program += fact.get('joins')[index]
                output_program += '.\n'

            for p_list in data.get('lists'):
                output_program += f"{p_list.get('name')}={p_list.get('items')}"

            return ApiResponse(output_program, 200)

        except WrongJsonFormat:
            return WrongJsonFormat()
        except WrongFactFormat:
            return WrongFactFormat()
        except Exception as e:
            return ApiResponse(str(e), 500)

    @classmethod
    def prolog_to_json(cls, input_json_data):
        return {}

    @classmethod
    def json_execute(cls, input_json_data):
        return {}

    @classmethod
    def prolog_execute(cls, input_json_data):
        return {}

    @classmethod
    def _check_prolog_format(cls, data):
        try:
            pass
        except Exception as e:
            return ApiResponse(str(e), 500)

    @classmethod
    def _check_json_format(cls, data):
        predicates = []
        facts = []
        lists = []

        for key, value in data.items():
            if key not in JSON_FORMAT:
                raise WrongJsonFormat()
            else:
                for item_key, item_value in value.items():

                    if item_key not in JSON_FORMAT[key]:
                        raise WrongJsonFormat()
                    if type(item_value).__name__ != JSON_FORMAT[key][item_key]:
                        raise WrongJsonFormat()

                    if item_key == 'name':
                        if 65 < ord(item_value[0]) < 90 or 65 < ord(item_value[-1]) < 90:
                            raise WrongJsonFormat()

            if key == 'predicate':
                predicates.append(value)

            elif key == 'fact':

                if value.get('conditions') is None:
                    raise WrongFactFormat()

                if value.get('arguments') is None or type(value.get('arguments')).__name__ != 'list':
                    raise WrongFactFormat()

                if \
                    value.get('joins') is None or \
                        type(value.get('joins')).__name__ != 'list' or \
                        len(value.get('joins')) != len(value.get('conditions')) - 1:
                    raise WrongFactFormat()
                else:
                    for joiner in value.get('joins'):
                        if joiner.lower() not in ALLOWED_CONDITIONS:
                            raise WrongFactFormat()

                for condition in value.get('conditions'):
                    if value.get('conditions') is None:
                        raise WrongFactFormat()
                    if condition.get('type') not in ALLOWED_CONDITIONS_TYPES:
                        raise WrongFactFormat()
                    if condition.get('type') == 'predicate':
                        if condition.get('arguments') is None or type(condition.get('arguments')).__name__ != 'list':
                            raise WrongFactFormat()

                facts.append(value)

            elif key == 'list':
                lists.append(value)

        return {
            'predicates': predicates,
            'facts': facts,
            'lists': lists
        }

import json

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
        output_program = ''

        read_data = json.loads(input_json_data)
        data = cls._check_json_format(read_data)

        for predicate in data['predicates']:
            output_program += f"{predicate['name']}({', '.join(predicate['arguments'])}).\n"

        for fact in data['facts']:
            output_program += f"{fact['name']}({', '.join(fact['arguments'])}):-"
            for index, condition in enumerate(fact['conditions']):
                if condition['type'] == 'predicate':
                    output_program += f"{condition['name']}({', '.join(condition['arguments'])})"
                if len(fact['joins']):
                    if index + 1 < len(fact['conditions']):
                        output_program += fact['joins'][index]
            output_program += '.\n'

        for p_list in data['lists']:
            output_program += f"{p_list['name']}={p_list['items']}"

        return output_program

    @classmethod
    def _check_json_format(cls, data):
        predicates = []
        facts = []
        lists = []

        for key, value in data.items():
            if key not in JSON_FORMAT:
                raise WrongJsonFormat
            else:
                for item_key, item_value in value.items():

                    if item_key not in JSON_FORMAT[key]:
                        raise WrongJsonFormat
                    if type(item_value).__name__ != JSON_FORMAT[key][item_key]:
                        raise WrongJsonFormat

                    if item_key == 'name':
                        if 65 < ord(item_value[0]) < 90 or 65 < ord(item_value[-1]) < 90:
                            raise WrongJsonFormat

            if key == 'predicate':
                predicates.append(value)

            elif key == 'fact':

                if len(value['conditions']) == 0:
                    raise WrongFactFormat

                if 'arguments' not in value or type(value['arguments']).__name__ != 'list':
                    raise WrongFactFormat

                if \
                    "joins" not in value or \
                        type(value['joins']).__name__ != 'list' or \
                        len(value['joins']) != len(value['conditions']) - 1:
                    raise WrongFactFormat
                else:
                    for joiner in value['joins']:
                        if joiner.lower() not in ALLOWED_CONDITIONS:
                            raise WrongFactFormat

                for condition in value['conditions']:
                    if 'type' not in condition:
                        raise WrongFactFormat
                    if condition['type'] not in ALLOWED_CONDITIONS_TYPES:
                        raise WrongFactFormat
                    if condition['type'] == 'predicate':
                        if 'arguments' not in condition or type(condition['arguments']).__name__ != 'list':
                            raise WrongFactFormat

                facts.append(value)

            elif key == 'list':
                lists.append(value)

        return {
            'predicates': predicates,
            'facts': facts,
            'lists': lists
        }

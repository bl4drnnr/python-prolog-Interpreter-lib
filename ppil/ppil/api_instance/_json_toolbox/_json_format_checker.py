from ppil.ppil.api_instance._api_response_handler import WrongFactFormat, WrongJsonFormat, WrongConditionFormat
from ppil.ppil.api_instance._variables import JSON_FORMAT_KEYS, ALLOWED_CONDITIONS_TYPES, CONDITION_SEPARATORS
from ppil.ppil.api_instance.elements import Predicate, Fact, Condition, PList


def parse_predicate_arguments(arguments):
    predicate_arguments = []

    for arg in arguments:
        if isinstance(arg, str):
            predicate_arguments.append(arg)
        elif arg.get('type') == 'list' and len(arg.get('items', [])) > 0:
            predicate_arguments.append(PList(arg.get('items')))
        else:
            raise WrongJsonFormat(response=f"Wrong element name: {arguments}")

    return predicate_arguments


class JsonFormatChecker:
    def __init__(self):
        self._parsed_data = {
            'predicates': [],
            'facts': []
        }

    def check_json_format(self, data):
        self._check_items_format(data)
        return self._parsed_data

    def _check_items_format(self, data):
        if not data.get('data'):
            raise WrongJsonFormat(response="There no 'data' body.")

        data = data['data']

        for item in data:
            if item.get('item') is None or item.get('body') is None:
                raise WrongJsonFormat(response=f"Wrong item format: {str(item)}")

            if item.get('item') not in JSON_FORMAT_KEYS:
                raise WrongJsonFormat(response=f"Wrong element name: {str(item)}")

            item_body = item.get('body')

            if item.get('item') == 'predicate':
                predicate_arguments = parse_predicate_arguments(item_body.get('arguments'))
                self._parsed_data['predicates'].append(Predicate(item_body.get('name'), predicate_arguments))

            elif item.get('item') == 'fact':
                fact_conditions = []

                for con in item_body.get('conditions'):
                    if con.get('type') not in ALLOWED_CONDITIONS_TYPES:
                        raise WrongFactFormat(response=f"Wrong format of condition: {con}")

                    if con.get('type') == 'predicate':
                        predicate_arguments = parse_predicate_arguments(con['arguments'])
                        fact_conditions.append(Predicate(con['name'], predicate_arguments))

                    elif con.get('type') == 'condition':
                        if con['separator'] not in CONDITION_SEPARATORS:
                            raise WrongConditionFormat(response=f"Wrong separator: {con['separator']}")

                        fact_conditions.append(Condition(
                            con['right_side'],
                            con['separator'],
                            con['left_side']
                        ))

                self._parsed_data['facts'].append(Fact(
                    item_body.get('arguments'),
                    item_body.get('joins'),
                    fact_conditions
                ))

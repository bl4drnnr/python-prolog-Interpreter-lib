from ppil.ppil.api_instance._api_response_handler import WrongFactFormat, WrongJsonFormat, WrongConditionFormat
from ppil.ppil.api_instance._variables import JSON_FORMAT, ALLOWED_CONDITIONS_TYPES, CONDITION_SEPARATORS
from ppil.ppil.api_instance.elements import Predicate, Fact, PList, Condition


class JsonFormatChecker:
    def __init__(self):
        self._parsed_data = {
            'predicates': [],
            'facts': [],
            'lists': []
        }

    def check_json_format(self, data):
        self._check_items_format(data)
        return self._parsed_data

    def _check_items_format(self, data):
        for key, value in data.items():
            if key not in JSON_FORMAT:
                raise WrongJsonFormat(response=f"Wrong element name: {key}")

            if key == 'predicate':
                self._parsed_data['predicates'].append(Predicate(value.get('name'), value.get('arguments')))

            elif key == 'fact':
                fact_conditions = []

                for con in value.get('conditions'):
                    if con.get('type') not in ALLOWED_CONDITIONS_TYPES:
                        raise WrongFactFormat(response=f"Wrong format of condition: {con}")

                    if con.get('type') == 'predicate':
                        fact_conditions.append(Predicate(con['name'], con['arguments']))

                    elif con.get('type') == 'condition':
                        if con['separator'] not in CONDITION_SEPARATORS:
                            raise WrongConditionFormat(response=f"Wrong separator: {con['separator']}")

                        fact_conditions.append(Condition(
                            con['right_side'],
                            con['separator'],
                            con['left_side']
                        ))

                self._parsed_data['facts'].append(Fact(
                    value.get('name'),
                    value.get('arguments'),
                    value.get('joins'),
                    fact_conditions
                ))

            elif key == 'list':
                self._parsed_data['lists'].append(PList(value.get('name'), value.get('items')))

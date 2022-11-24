from src.ppil.api_instance._api_response_handler import WrongFactFormat, WrongJsonFormat
from src.ppil.api_instance._variables import JSON_FORMAT, ALLOWED_CONDITIONS_TYPES, ALLOWED_CONDITIONS, CONDITION_SEPARATORS


class JsonFormatChecker:
    def __init__(self):
        self._parsed_data = {
            'predicates': [],
            'facts': [],
            'lists': []
        }

    def check_json_format(self, data):
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
                self._check_predicate(value)

            elif key == 'fact':
                self._check_fact(value)

            elif key == 'list':
                self._check_list(value)

        return self._parsed_data

    def _check_predicate(self, predicate):
        self._parsed_data['predicates'].append(predicate)

    def _check_fact(self, fact):
        if fact.get('conditions') is None:
            raise WrongFactFormat()

        if fact.get('arguments') is None or type(fact.get('arguments')).__name__ != 'list':
            raise WrongFactFormat()

        if \
            fact.get('joins') is None or \
                type(fact.get('joins')).__name__ != 'list' or \
                len(fact.get('joins')) != len(fact.get('conditions')) - 1:
            raise WrongFactFormat()
        else:
            for joiner in fact.get('joins'):
                if joiner.lower() not in ALLOWED_CONDITIONS:
                    raise WrongFactFormat()

        for condition in fact.get('conditions'):
            if fact.get('conditions') is None:
                raise WrongFactFormat()

            if condition.get('type') not in ALLOWED_CONDITIONS_TYPES:
                raise WrongFactFormat()
            if condition.get('type') == 'predicate':
                if condition.get('arguments') is None or type(condition.get('arguments')).__name__ != 'list':
                    raise WrongFactFormat()
            if condition.get('type') == 'condition':
                if condition.get('value') is None or type(condition.get('value')).__name__ != 'str':
                    raise WrongFactFormat()

        self._parsed_data['facts'].append(fact)

    def _check_list(self, p_list):
        self._parsed_data['lists'].append(p_list)

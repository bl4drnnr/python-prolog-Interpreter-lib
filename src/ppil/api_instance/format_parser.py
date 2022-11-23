from .api_response_handler import WrongFactFormat, WrongJsonFormat

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
ALLOWED_CONDITIONS_TYPES = ['predicate', 'condition']


class FormatParser:
    def __init__(self):
        pass

    @staticmethod
    def check_json_format(data):
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
                    if condition.get('type') == 'condition':
                        if condition.get('value') is None or type(condition.get('value')).__name__ != 'str':
                            raise WrongFactFormat()

                facts.append(value)

            elif key == 'list':
                lists.append(value)

        return {
            'predicates': predicates,
            'facts': facts,
            'lists': lists
        }

    @staticmethod
    def check_prolog_format(data):
        pass

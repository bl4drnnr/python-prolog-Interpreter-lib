from ppil.ppil.api_instance._api_response_handler import WrongFactFormat, WrongJsonFormat
from ppil.ppil.api_instance._variables import JSON_FORMAT_KEYS
from ppil.ppil.api_instance.elements import Predicate, Fact, PList, Atom


def _check_item_type(item):
    if isinstance(item, str):
        return Atom(item)
    elif item.get('type') == 'list':
        return PList(item.get('items'))
    elif item.get('type') == 'predicate':
        return Predicate(item.get('body').get('name'), _parse_predicate(item.get('body')))


def _parse_predicate(predicate):
    return [_check_item_type(arg) for arg in predicate.get('arguments')]


def _parse_fact(fact):
    arguments = _parse_predicate(fact)
    conditions = [_check_item_type(condition) for condition in fact.get('conditions')]

    return [arguments, conditions]


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
            if item.get('type') is None or item.get('body') is None:
                raise WrongJsonFormat(response=f"Wrong item format: {str(item)}")

            if item.get('type') not in JSON_FORMAT_KEYS:
                raise WrongJsonFormat(response=f"Wrong element name: {str(item)}")

            item_body = item.get('body')

            if item.get('type') == 'predicate':
                if item_body.get('arguments') is None or item_body.get('name') is None:
                    raise WrongJsonFormat(response=f"No name or arguments for predicate: {str(item_body)}")

                self._parsed_data.get('predicates').append(Predicate(item_body.get('name'), _parse_predicate(item_body)))

            elif item.get('type') == 'fact':
                if \
                        item_body.get('arguments') is None or \
                        item_body.get('conditions') is None or \
                        item_body.get('joins') is None or \
                        item_body.get('name') is None:
                    raise WrongFactFormat(response=f"Lack of required field for fact: {str(item_body)}")

                [arguments, conditions] = _parse_fact(item_body)
                self._parsed_data.get('facts').append(Fact(item_body.get('name'), arguments, item.get('joins'), conditions))

from ppil.ppil.api_instance.elements import PList, Atom, Predicate


def _check_item_type(item):
    if isinstance(item, Atom):
        return {
            "type": item.type,
            "data_type": item.data_type,
            "value": float(item.atom) if item.data_type == 'number' else item.atom
        }
    elif isinstance(item, PList):
        return {
            "type": item.type,
            "items": _parse_predicate_arguments(item.items)
        }
    elif isinstance(item, Predicate):
        return {
            "type": item.type,
            "body": {
                "name": item.name,
                "arguments": _parse_condition(item)
            }
        }


def _parse_predicate_arguments(arguments):
    iter_items = arguments if isinstance(arguments, list) else arguments.items
    return [_check_item_type(arg) for arg in iter_items]


def _parse_condition(condition):
    return [_check_item_type(predicate_item) for predicate_item in condition.arguments.items]


class PrologParser:
    def __init__(self):
        self._output_json = []

    def parse_prolog(self, prolog_data):
        self._reset_data()

        for item in prolog_data:
            if item.type == 'predicate':
                self._output_json.append({
                    "type": item.type,
                    "body": {
                        "name": item.name,
                        "arguments": _parse_predicate_arguments(item.arguments)
                    }
                })
            elif item.type == 'fact':
                conditions = []

                for condition in item.conditions:
                    conditions.append({
                        "type": condition.type,
                        "body": {
                            "name": condition.name,
                            "arguments": _parse_condition(condition)
                        }
                    })

                self._output_json.append({
                    "type": item.type,
                    "body": {
                        "name": item.arguments.name,
                        "arguments": _parse_predicate_arguments(item.arguments.arguments),
                        "joins": item.joins,
                        "conditions": conditions
                    }
                })

        return self._output_json

    def _reset_data(self):
        self._output_json = []

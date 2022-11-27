from ppil.ppil.api_instance.elements import PList, Atom, Predicate


def _parse_predicate_arguments(arguments):
    predicate_arguments = []
    iter_items = arguments if isinstance(arguments, list) else arguments.items

    for arg in iter_items:
        if isinstance(arg, str):
            predicate_arguments.append(arg)
        elif isinstance(arg, Atom):
            predicate_arguments.append(arg.atom)
        elif isinstance(arg, PList):
            predicate_arguments.append({
                "type": arg.type,
                "items": _parse_predicate_arguments(arg.items)
            })

    return predicate_arguments


def _parse_condition(condition):
    parsed_conditions = []

    for predicate_item in condition.arguments.items:
        if isinstance(predicate_item, str):
            parsed_conditions.append(predicate_item)
        elif isinstance(predicate_item, Atom):
            parsed_conditions.append(predicate_item.atom)
        elif isinstance(predicate_item, PList):
            parsed_conditions.append({
                "type": predicate_item.type,
                "items": _parse_predicate_arguments(predicate_item)
            })
        elif isinstance(predicate_item, Predicate):
            parsed_conditions.append({
                "type": predicate_item.type,
                "body": {
                    "name": predicate_item.name,
                    "arguments": _parse_condition(predicate_item)
                }
            })

    return parsed_conditions


class PrologParser:
    def __init__(self):
        self._output_json = []

    def parse_prolog(self, prolog_data):
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
                    conditions.append(_parse_condition(condition))

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

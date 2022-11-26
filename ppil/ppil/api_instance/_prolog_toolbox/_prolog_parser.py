from ppil.ppil.api_instance.elements import PList


def parse_predicate_arguments(arguments):
    predicate_arguments = []

    for arg in arguments:
        if isinstance(arg, str):
            predicate_arguments.append(arg)
        elif isinstance(arg, PList):
            predicate_arguments.append({
                "type": arg.type,
                "items": arg.items
            })

    return predicate_arguments


class PrologParser:
    def __init__(self):
        self._output_json = []

    def parse_prolog(self, prolog_data):
        for item in prolog_data:
            if item.type == 'predicate':
                self._output_json.append({
                    "item": item.type,
                    "body": parse_predicate_arguments(item.arguments)
                })
            elif item.type == 'fact':
                conditions = []
                for condition in item.conditions:
                    if condition.get('type') == 'predicate':
                        conditions.append(parse_predicate_arguments(condition.get('arguments')))

                self._output_json.append({
                    "item": item.type,
                    "body": {
                        "name": item.name,
                        "arguments": parse_predicate_arguments(item.arguments),
                        "joins": item.joins,
                        "conditions": conditions
                    }
                })

        return self._output_json

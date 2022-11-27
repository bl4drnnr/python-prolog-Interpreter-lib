from ppil.ppil.api_instance.elements import PList, Atom


def parse_predicate_arguments(arguments):
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
                "items": parse_predicate_arguments(arg.items)
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
                    "body": {
                        "name": item.name,
                        "arguments": parse_predicate_arguments(item.arguments)
                    }
                })
            elif item.type == 'fact':
                conditions = []

                for condition in item.conditions:
                    if condition.type == 'predicate':
                        conditions.append(parse_predicate_arguments(condition.arguments))
                    elif condition.type == 'condition':
                        conditions.append({
                            "type": condition.type,
                            "separator": condition.separator,
                            "left_side": condition.left_side,
                            "right_side": condition.right_side
                        })

                self._output_json.append({
                    "item": item.type,
                    "body": {
                        "name": item.arguments.name,
                        "arguments": parse_predicate_arguments(item.arguments.arguments),
                        "joins": item.joins,
                        "conditions": conditions
                    }
                })

        return self._output_json

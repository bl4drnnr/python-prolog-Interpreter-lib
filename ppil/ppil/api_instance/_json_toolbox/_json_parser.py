from ppil.ppil.api_instance.elements import PList, Atom


def _check_item_type(item):
    if isinstance(item, str):
        return item
    elif isinstance(item, list):
        return [_check_item_type(i) for i in item]
    elif isinstance(item, Atom):
        return item.atom
    elif isinstance(item, PList):
        return _parse_predicate_arguments(item.items)
    elif item.get('type') == 'list':
        return [str(s) for s in item.get('items')]


def _parse_predicate_arguments(arguments):
    iter_items = arguments if isinstance(arguments, list) else arguments.items
    return [_check_item_type(arg) for arg in iter_items]


class JsonParser:
    def __init__(self):
        self._output_program = ''

    def _parse_json_predicates(self, predicates):
        for predicate in predicates:
            predicate_arguments = _parse_predicate_arguments(predicate.arguments)
            self._output_program += f"{predicate.name}({str(predicate_arguments)[1:-1]}).\n"

    def _parse_json_facts(self, facts):
        for fact in facts:
            fact_name = fact.name
            fact_arguments = str([atom.atom for atom in fact.arguments])[1:-1]

            self._output_program += f"{fact_name}({fact_arguments}):-"

            for condition in fact.conditions:
                self._output_program += f"{condition.name}({str(_parse_predicate_arguments(condition.arguments))[1:-1]})"

    def parse_json(self, serialized_json):
        self._parse_json_predicates(serialized_json.get('predicates'))
        self._parse_json_facts(serialized_json.get('facts'))

        return self._output_program

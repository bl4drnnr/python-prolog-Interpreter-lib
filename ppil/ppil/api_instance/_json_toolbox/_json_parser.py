from ppil.ppil.api_instance.elements import PList, Atom, Predicate


def _check_item_type(item):
    if isinstance(item, str):
        return item
    elif isinstance(item, list):
        return [_check_item_type(i) for i in item]
    elif isinstance(item, Atom):
        return item.atom
    elif isinstance(item, PList):
        return _parse_predicate_arguments(item.items)
    elif isinstance(item, Predicate):
        serialized_text = str(_parse_predicate_arguments(item.arguments))[1:-1]
        serialized_text = serialized_text.replace('\'', '')
        return f"{item.name}({serialized_text})"
    elif item.get('type') == 'list':
        return [str(s) for s in item.get('items')]


def _parse_predicate_arguments(arguments):
    iter_items = arguments if isinstance(arguments, list) else arguments.items
    return [_check_item_type(arg) for arg in iter_items]


def _serialize_arguments(arguments):
    serialized_arguments = ""

    for arg in arguments:
        if isinstance(arg, str):
            serialized_arguments += arg
        elif isinstance(arg, list):
            serialized_arguments += _serialize_arguments(arg)

    return serialized_arguments


class JsonParser:
    def __init__(self):
        self._output_program = ''

    def parse_json(self, serialized_json):
        self._reset_data()

        self._parse_json_predicates(serialized_json.get('predicates'))
        self._parse_json_facts(serialized_json.get('facts'))

        return self._output_program

    def _reset_data(self):
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

            for index, condition in enumerate(fact.conditions):
                join = fact.joins[index] if index < len(fact.joins) else ''
                serialized_arguments = _serialize_arguments(_parse_predicate_arguments(condition.arguments))
                self._output_program += f"{condition.name}({serialized_arguments}){join}"

            self._output_program += ".\n"

from ppil.ppil.api_instance.elements import PList, Atom, Predicate, Condition, ConditionStatement


def _check_item_type(item):
    if isinstance(item, list):
        return [_check_item_type(i) for i in item]

    elif isinstance(item, Atom):
        if item.data_type == 'string':
            return f"'{item.atom}',"
        elif item.data_type in ['number', 'variable', 'atom']:
            return f"{item.atom},"

    elif isinstance(item, PList):
        if item.head and item.tail:
            return f"[{item.head}|{item.tail}],"
        else:
            parsed_list = f"[{_parse_predicate_arguments(item.items)}]"
            open_bracket = parsed_list.count('[')
            close_bracket = parsed_list.count(']')

            if open_bracket == close_bracket:
                return parsed_list
            else:
                return parsed_list + "]" * (open_bracket - close_bracket)

    elif isinstance(item, Predicate):
        serialized_text = _parse_predicate_arguments(item.arguments)
        return f"{item.name}({serialized_text})"

    elif isinstance(item, Condition):
        return f"{item.left_side}{item.separator}{item.right_side}"

    elif isinstance(item, ConditionStatement):
        if_condition = _check_item_type(item.if_condition)
        else_clause = [_check_item_type(i) for i in item.else_clause]
        then_clause = [_check_item_type(i) for i in item.then_clause]
        return f"{if_condition}->{','.join(else_clause)};{','.join(then_clause)}"


def _parse_predicate_arguments(arguments):
    parsed_string = ''

    for arg in arguments:
        parsed_string += _check_item_type(arg)

    if parsed_string[-1] == ',':
        return parsed_string[:-1]
    else:
        return parsed_string


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
            fact_arguments = ""

            for atom in fact.arguments:
                fact_arguments += _check_item_type(atom)

            self._output_program += f"{fact_name}({fact_arguments[:-1]}):-"

            for index, condition in enumerate(fact.conditions):
                join = fact.joins[index] if index < len(fact.joins) else ''

                if isinstance(condition, Predicate):
                    serialized_arguments = _serialize_arguments(_parse_predicate_arguments(condition.arguments))
                    self._output_program += f"{condition.name}({serialized_arguments}){join}"
                elif isinstance(condition, Condition):
                    self._output_program += f"{condition.left_side}{condition.separator}{condition.right_side}{join}"
                elif isinstance(condition, ConditionStatement):
                    self._output_program += f"({_check_item_type(condition)}){join}"

            self._output_program += ".\n"

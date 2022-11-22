from src.ppil.elements import Variable, Database
from .parser import Parser


class KnowledgeDatabase:
    def __init__(self, rules_text):
        rules = Parser(rules_text).parse_rules()
        self._database = Database(rules)
        self._query = None
        self._matching_query_terms = []
        self._query_variable_map = {}
        self._variables_in_query = False

    def find_solutions(self, query_text):
        self._query = Parser(query_text).parse_query()

        for argument in self._query.arguments:
            if isinstance(argument, Variable):
                self._variables_in_query = True
                self._query_variable_map[argument.name] = argument

        self._matching_query_terms = [item for item in self._database.query(self._query)]

        if not self._matching_query_terms and not self._variables_in_query:
            return False

        if not self._matching_query_terms and self._variables_in_query:
            return None

        if self._query_variable_map:
            return self._create_solution_map()

        if not self._variables_in_query:
            return True

        return None

    def _create_solution_map(self):
        solutions_map = {}

        for matching_query_term in self._matching_query_terms:
            matching_variable_bindings = self._query.match_variable_bindings(matching_query_term)

            for variable_name, variable in self._query_variable_map.items():
                solutions_map[variable_name] = matching_variable_bindings.get(variable)

        return solutions_map

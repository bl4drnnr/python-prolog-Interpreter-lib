from .elements.database import Database
from .elements.term import Term
from .elements.variable import Variable
from .elements.true_statement import TRUE
from .elements.rule import Rule


class Conjunction(Term):
    def __init__(self, arguments):
        super().__init__("", arguments)

    def query(self, database):
        def find_solutions(argument_index, variable_bindings):
            if argument_index >= len(self.arguments):
                yield self.substitute_variable_bindings(variable_bindings)
            else:
                current_term = self.arguments[argument_index]

                for item in database.query(current_term.substitute_variable_bindings(variable_bindings)):
                    combined_variable_bindings = Database.merge_bindings(
                        current_term.match_variable_bindings(item),
                        variable_bindings,
                    )

                    if combined_variable_bindings is not None:
                        yield from find_solutions(argument_index + 1, combined_variable_bindings)

        yield from find_solutions(0, {})

    def substitute_variable_bindings(self, variable_bindings):
        return Conjunction([
                argument.substitute_variable_bindings(variable_bindings)
                for argument in self.arguments
            ])

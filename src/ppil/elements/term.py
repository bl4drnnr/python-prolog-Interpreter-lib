from .variable import Variable
from .database import Database
from functools import reduce


class Term:
    def __init__(self, functor, arguments=None):
        if not arguments:
            arguments = []
        self.functor = functor
        self.arguments = arguments

    def match_variable_bindings(self, other_term):
        if isinstance(other_term, Variable):
            return other_term.match_variable_bindings(self)

        if isinstance(other_term, Term):
            if self.functor != other_term.functor or len(self.arguments) != len(other_term.arguments):
                return None

            zipped_argument_list = list(zip(self.arguments, other_term.arguments))

            matched_argument_var_bindings = [
                arguments[0].match_variable_bindings(arguments[1])
                for arguments in zipped_argument_list
            ]
            return reduce(Database.merge_bindings, [{}] + matched_argument_var_bindings)

    def substitute_variable_bindings(self, variable_bindings):
        return Term(self.functor, [
                argument.substitute_variable_bindings(variable_bindings)
                for argument in self.arguments
            ])

    def query(self, database):
        yield from database.query(self)

    def __str__(self):
        return (
            str(self.functor)
            if len(self.arguments) == 0
            else str(self.functor)
            + " ( "
            + ", ".join(str(argument) for argument in self.arguments)
            + " ) "
        )

    def __repr__(self):
        return str(self)


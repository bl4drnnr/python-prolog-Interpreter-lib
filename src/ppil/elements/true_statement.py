from .term import Term


class TrueStatement(Term):
    def __init__(self, functor="TRUE", arguments=None):
        if not arguments:
            arguments = []
        super().__init__(functor, arguments)

    def substitute_variable_bindings(self, variable_bindings):
        return self

    def query(self, database):
        yield self

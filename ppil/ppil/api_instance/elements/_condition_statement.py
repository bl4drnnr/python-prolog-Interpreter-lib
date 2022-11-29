class ConditionStatement:
    def __init__(self, condition, then_clause, else_clause):
        self.type = "condition_statement"
        self.condition = condition
        self.then_clause = then_clause
        self.else_clause = else_clause

    def __str__(self):
        return f"" \
               f"Condition statement - " \
               f"condition: {self.condition}, " \
               f"then clause: {self.then_clause}, " \
               f"else clause: {self.else_clause}"

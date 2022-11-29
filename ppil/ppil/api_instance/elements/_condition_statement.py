class ConditionStatement:
    def __init__(self, if_condition, then_clause, else_clause):
        self.type = "condition_statement"
        self.if_condition = if_condition
        self.then_clause = then_clause
        self.else_clause = else_clause

    def __str__(self):
        return f"" \
               f"Condition statement - " \
               f"if condition: {self.if_condition}, " \
               f"then clause: {self.then_clause}, " \
               f"else clause: {self.else_clause}"

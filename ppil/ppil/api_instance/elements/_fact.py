from __future__ import annotations


class Fact:
    def __init__(
            self,
            arguments,
            joins,
            conditions
    ):
        self.type = "fact"
        self.arguments = arguments
        self.joins = joins
        self.conditions = conditions

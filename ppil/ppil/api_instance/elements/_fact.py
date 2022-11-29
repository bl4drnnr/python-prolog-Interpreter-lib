from __future__ import annotations


class Fact:
    def __init__(
            self,
            name,
            arguments,
            joins,
            conditions
    ):
        self.type = "fact"
        self.name = name
        self.arguments = arguments
        self.joins = joins
        self.conditions = conditions

    def __str__(self):
        return f"Fact - " \
               f"name: {self.name}, " \
               f"arguments: {self.arguments}, " \
               f"joins: {self.joins}, " \
               f"conditions: {self.conditions}"

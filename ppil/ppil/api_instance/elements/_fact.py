from __future__ import annotations

from ._predicate import Predicate
from ._condition import Condition


class Fact:
    def __init__(
            self,
            name: str,
            arguments: list[str],
            joins: list[str],
            conditions: list[Predicate | Condition]
    ):
        self.type = "fact"
        self.name = name
        self.arguments = arguments
        self.joins = joins
        self.conditions = conditions

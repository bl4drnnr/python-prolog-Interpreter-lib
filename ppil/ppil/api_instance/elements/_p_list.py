from __future__ import annotations


class PList:
    def __init__(self, name: str, items: list[str | int | list]):
        self.type = "list"
        self.name = name
        self.items = items

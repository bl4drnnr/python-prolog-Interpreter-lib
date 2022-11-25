from __future__ import annotations


class PList:
    def __init__(self, items: list[str | int | list]):
        self.type = "list"
        self.items = items

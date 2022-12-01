from __future__ import annotations


class PList:
    def __init__(self, items, head=None, tail=None):
        self.type = "list"
        self.items = items
        self.head = head
        self.tail = tail

    def __str__(self):
        return f"PList - " \
               f"items: {self.items}, " \
               f"head: {self.head}, " \
               f"tail: {self.tail}"

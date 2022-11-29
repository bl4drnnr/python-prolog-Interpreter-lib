from __future__ import annotations


class PList:
    def __init__(self, items, head=None, tail=None):
        self.type = "list"
        self.items = items
        self.head = head
        self.tail = tail

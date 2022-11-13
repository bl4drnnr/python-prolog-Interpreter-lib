from collections import deque
from bisect import insort


class SearchQueue:
    def __init__(self):
        self._container = deque()

    @property
    def empty(self):
        return not self._container

    def push(self, expr):
        self._container.append(expr)

    def pop(self):
        return self._container.popleft()

    def __repr__(self):
        return repr(self._container)


class FactHeap:
    def __init__(self):
        self._container = []

    def push(self, item):
        insort(self._container, item)

    def __getitem__(self, item):
        return self._container[item]

    def __len__(self):
        return len(self._container)

    def __repr__(self):
        return repr(self._container)

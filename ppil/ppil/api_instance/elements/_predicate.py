class Predicate:
    def __init__(self, name: str, arguments: list[str]):
        self.type = "predicate"
        self.name = name
        self.arguments = arguments

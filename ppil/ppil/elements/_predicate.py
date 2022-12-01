class Predicate:
    def __init__(self, name, arguments):
        self.type = "predicate"
        self.name = name
        self.arguments = arguments

    def __str__(self):
        return f"Predicate - " \
               f"name: {self.name}, " \
               f"arguments: {self.arguments}"

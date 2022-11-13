class Fact:
    def __init__(self, fact):
        self.terms = None
        self.parse_fact(fact)

    def parse_fact(self, fact):
        fact = fact.replace(" ", "")
        if ":-" in fact:
            replacements = {"),": ")AND", ");": ")OR"}
            
import re


class Expression:
    def __init__(self, fact):
        self._parse_expression(fact)
            
    def _parse_expression(self, fact):
        fact = fact.replace(" ", "")
        self.f = fact
        splitting = r"is|\*|\+|\-|\/|>=|<=|>|<|and|or|in|not"

        if "(" not in fact:
            fact = "(" + fact + ")"

        pred_ind = fact.index("(")
        self.predicate = fact[:pred_ind]
        self.terms = fact[pred_ind:]
        to_remove = str.maketrans("", "", "() ")
        self.terms = self.terms.translate(to_remove)

        if self.predicate == "":
            self.terms = re.split(splitting, self.terms)
        else:
            self.terms = self.terms.split(",")

        self.string = self.f
        self.index = 0

    def to_string(self):
        return self.string

    def __lt__(self, other):
        return self.terms[self.index] < other.terms[other.index]

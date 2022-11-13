from itertools import chain
from more_itertools import unique_everseen
import re
from ppil.expression.expression import Expression


class Fact:
    def __init__(self, fact):
        self._parse_fact(fact)
        
    def _parse_fact(self, fact):
        fact = fact.replace(" ", "")

        self.terms = self._rule_terms(fact)

        if ":-" in fact:
            if_ind = fact.index(":-")
            self.lh = Expression(fact[:if_ind])
            replacements = {"),": ")AND", ");": ")OR"}
            replacements = dict((re.escape(k), v) for k, v in replacements.items()) 
            pattern = re.compile("|".join(replacements.keys()))
            rh = pattern.sub(lambda x: replacements[re.escape(x.group(0))], fact[if_ind + 2:])
            rh = re.split("AND|OR", rh)
            self.rhs = [Expression(g) for g in rh]
            rs = [i.to_string() for i in self.rhs]
            self.fact = (self.lh.to_string() + ":-" + ",".join(rs))
        else:
            self.lh = Expression(fact)
            self.rhs = []
            self.fact = self.lh.to_string()

    def _rule_terms(self, rule_string):
        s = re.sub(" ", "", rule_string)
        s = re.findall(r"\((.*?)\)", s)
        s = [i.split(",") for i in s]
        s = list(chain(*s))
        return list(unique_everseen(s))

    def to_string(self):
        return self.fact

    def __lt__(self, other):
        return self.lh.terms[self.lh.index] < other.lh.terms[other.lh.index]

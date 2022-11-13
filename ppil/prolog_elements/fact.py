import re
from ppil.expression.expression import Expression


class Fact:
    def __init__(self, fact):
        self.right_side = None
        self.left_side = None
        self.fact = None
        self.terms = None

        self._parse_fact(fact)
        
    def _parse_fact(self, fact):
        fact = fact.replace(" ", "")

        self.terms = self._rule_terms(fact)

        if ":-" in fact:
            [fact_left_side, fact_right_side] = fact.split(":-")
            # if_ind = fact.index(":-")
            # self.left_side = Expression(fact[:if_ind])
            #
            # replacements = {"),": ")AND", ");": ")OR"}
            # replacements = dict((re.escape(k), v) for k, v in replacements.items())
            # pattern = re.compile("|".join(replacements.keys()))
            #
            # rh = pattern.sub(lambda x: replacements[re.escape(x.group(0))], fact[if_ind + 2:])
            # rh = re.split("AND|OR", rh)
            #
            # self.right_side = [Expression(g) for g in rh]
            # rs = [i.to_string() for i in self.right_side]
            # self.fact = (self.left_side.to_string() + ":-" + ",".join(rs))
        else:
            self.left_side = Expression(fact)
            self.right_side = []
            self.fact = self.left_side.to_string()

    def _rule_terms(self, rule_string):
        extracted_rule_terms = re.findall(r"\((.*?)\)", rule_string)

        single_terms = []
        for rules in extracted_rule_terms:
            single_terms.append(rules.split(','))

        chained_terms = []
        for i1 in single_terms:
            for i2 in i1:
                try:
                    i2 = float(i2)
                    chained_terms.append(i2)
                except (Exception,):
                    chained_terms.append(i2)

        return chained_terms

    def to_string(self):
        return self.fact

    def __lt__(self, other):
        return self.left_side.terms[self.left_side.index] < other.left_side.terms[other.left_side.index]

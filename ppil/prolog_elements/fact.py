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
            self.left_side = Expression(fact_left_side)

            right_side = []
            split_right_side = fact_right_side.split("),")

            for i in split_right_side:
                if '(' in i and ')' not in i:
                    i += ')'
                elif ',' in i and '(' not in i and ')' not in i:
                    right_side += i.split(',')
                    continue
                right_side.append(i)

            self.right_side = [Expression(g) for g in right_side]
            rs = [i.to_string() for i in self.right_side]
            self.fact = (self.left_side.to_string() + ":-" + ",".join(rs))
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

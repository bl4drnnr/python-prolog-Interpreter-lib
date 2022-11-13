from ppil.query.rule_query import *
from ppil.prolog_elements.goal import Goal
from ppil.prolog_elements.fact import Fact


class KnowledgeDatabase(object):
    def __init__(self, name):
        self.db = {}
        self.name = name

    def init_knowledge_database(self, database):
        for i in database:
            i = Fact(i)

            g = []
            for r in i.right_side:
                goal = Goal(Fact(r.to_string()))
                g.append(goal)

            if i.left_side.predicate in self.db:
                self.db[i.left_side.predicate]["facts"].append(i)
                self.db[i.left_side.predicate]["terms"].append(i.terms)
                self.db[i.left_side.predicate]["goals"].append(g)
            else:
                self.db[i.left_side.predicate] = {
                    "facts": [i],
                    "goals": [g],
                    "terms": [i.terms]
                }

    def __call__(self, args):
        self.init_knowledge_database(args)

    def query(self, expr):
        return rule_query(self, expr)

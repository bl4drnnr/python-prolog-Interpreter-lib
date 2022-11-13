from ppil.pq import FactHeap
from ppil.query.rule_query import *
from ppil.search_util import *


class KnowledgeDatabase(object):
    def __init__(self, name):
        self.db = {}
        self.name = name
        self._cache = {}
    
    def init_knowledge_database(self, database):
        for i in database:
            i = Fact(i)
            g = [Goal(Fact(r.to_string())) for r in i.right_side]

            if i.left_side.predicate in self.db:
                self.db[i.left_side.predicate]["facts"].push(i)
                self.db[i.left_side.predicate]["terms"].push(i.terms)
                self.db[i.left_side.predicate]["goals"].push(g)
            else:
                self.db[i.left_side.predicate] = {}
                self.db[i.left_side.predicate]["facts"] = FactHeap()
                self.db[i.left_side.predicate]["facts"].push(i)
                self.db[i.left_side.predicate]["goals"] = FactHeap()
                self.db[i.left_side.predicate]["goals"].push(g)
                self.db[i.left_side.predicate]["terms"] = FactHeap()
                self.db[i.left_side.predicate]["terms"].push(i.terms)

    def __call__(self, args):
        self.init_knowledge_database(args)

    def query(self, expr):
        return rule_query(self, expr)

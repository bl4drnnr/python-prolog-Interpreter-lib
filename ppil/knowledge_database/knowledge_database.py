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
            g = [Goal(Fact(r.to_string())) for r in i.rhs]

            if i.lh.predicate in self.db:
                self.db[i.lh.predicate]["facts"].push(i)
                self.db[i.lh.predicate]["terms"].push(i.terms)
                self.db[i.lh.predicate]["goals"].push(g)
            else:
                self.db[i.lh.predicate] = {}
                self.db[i.lh.predicate]["facts"] = FactHeap()
                self.db[i.lh.predicate]["facts"].push(i)
                self.db[i.lh.predicate]["goals"] = FactHeap()
                self.db[i.lh.predicate]["goals"].push(g)
                self.db[i.lh.predicate]["terms"] = FactHeap()
                self.db[i.lh.predicate]["terms"].push(i.terms)

    def __call__(self, args):
        self.init_knowledge_database(args)

    def query(self, expr):
        return rule_query(self, expr)

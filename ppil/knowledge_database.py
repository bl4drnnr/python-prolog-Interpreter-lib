from .fact import Fact


def init_knowledge_database(kn):
    for i in kn:
        i = Fact(i)


class KnowledgeDatabase(object):

    def __init__(self, name=None):
        self.db = {}
        self.name = name

    def __call__(self, args):
        init_knowledge_database(args)

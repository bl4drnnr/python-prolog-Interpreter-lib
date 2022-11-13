class Goal:
    def __init__(self, fact, parent=None, domain=None, ind=0):
        if domain is None:
            domain = {}
        self.fact = fact
        self.parent = parent
        self.domain = {}
        self.domain.update(domain)
        self.ind = ind
        
    def __copy__(self):
        return Goal(self.fact, self.parent, self.domain, self.ind)

    def __repr__(self):
        return "Goal = %s, parent = %s" % (self.fact, self.parent)
        
    def __lt__(self, other):
        return self.fact.left_side.terms[self.fact.left_side.index] < other.fact.left_side.terms[other.fact.left_side.index]
        
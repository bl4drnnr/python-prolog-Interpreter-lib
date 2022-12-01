class Atom:
    def __init__(self, atom, data_type=None):
        self.type = "atom"
        self.atom = atom
        self.data_type = data_type

    def __str__(self):
        return f"Atom: {self.atom}. Data type: {self.data_type}"

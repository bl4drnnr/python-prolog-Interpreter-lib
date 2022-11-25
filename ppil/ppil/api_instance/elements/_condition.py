class Condition:
    def __init__(self, right_side: str, separator: str, left_side: str):
        self.type = "condition"
        self.right_side = right_side
        self.separator = separator
        self.left_side = left_side

class Line:
    def __init__(self):
        self.owner = 0

    def draw(self, player):
        self.owner = player

    def __bool__(self):
        return self.owner == 0

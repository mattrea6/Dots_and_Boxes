import Line

class Box:
    def __init__(self, top, bottom, left, right):
        self.owner = 0
        self.edges = [top, bottom, left, right]
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def check_edges(self, player):
        if all(self.edges):
            print("Player {} got a box!".format(player))
            self.owner = player

    def __str__(self):
        if self.owner == 0:
            return " "
        else:
            return str(self.owner)

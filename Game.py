from Box import Box
from Line import Line

class Game:
    def __init__(self, no_players, width, height):
        self.width = width
        self.height = height
        self.no_players = no_players
        self.build_game()

    def build_game(self):
        # Build lists of horizontal and vertical lines
        verts = [[Line() for j in range(self.height-1)] for i in range(self.width)]
        horiz = [[Line() for j in range(self.width-1)] for i in range(self.height)]
        # Then add to one list
        self.grid = [horiz, verts]
        # This means grid[0][0][0] is the top-left horizontal line
        # grid[1][0][0] is the top left vertical line
        # Then build the box objects in a 2d list
        self.boxes = [[0 for i in range(self.width-1)] for j in range(self.height-1)]
        for i in range(self.height-1):
            for j in range(self.width-1):
                # Boxes are constructed with lines in the order [top, bottom, left, right]
                self.boxes[i][j] = Box(self.grid[0][i][j], self.grid[0][i+1][j], self.grid[1][j][i], self.grid[1][j+1][i])

    def take_turn(self, player, move):
        self.grid[move[0], move[1], move[2]].draw(player)

    def print_grid(self):
        for i in range(self.height):
            for j in range(self.width):
                if j != self.width-1:
                    print("*", end="")
                    if self.grid[0][i][j]:
                        print("- -", end="")
                    else:
                        print("---", end="")
                else:
                    print("*")
            if i != self.height-1:
                for j in range(self.width):
                    if j != self.width-1:
                        if self.grid[1][j][i]:
                            print("¦", end="")
                        else:
                            print("|", end="")
                        print(" {} ".format(self.boxes[i][j]), end="")
                    else:
                        if self.grid[1][j][i]:
                            print("¦")
                        else:
                            print("|")

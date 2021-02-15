from Box import Box
from Line import Line

class Game:
    def __init__(self, width, height, copy_grid=None, copy_boxes=None):
        """
        Initialise the game with given width and height.
        If grid or boxes are passed, then create a copy of these objects.
        Args:
            width: int
            height: int
        """
        self.width = width
        self.height = height
        self.currentPlayer = 1
        self.maxPlayers = 2
        if copy_grid is None and copy_boxes is None:
            self.build_game()
        else:
            self.build_copy(copy_grid, copy_boxes)

    def build_game(self):
        """
        Builds an empty game board with internal width and height.
        """
        # Build two lists of horizontal and vertical lines.
        self.grid = [
            [[Line() for j in range(self.height-1)] for i in range(self.width)],
            [[Line() for j in range(self.width-1)] for i in range(self.height)]
        ]
        # This means grid[0][0][0] is the top left horizontal line
        # grid[1][0][0] is the top left vertical line
        # Then build the box objects in a 2d list
        self.boxes = [[0 for i in range(self.width-1)] for j in range(self.height-1)]
        for i in range(self.height-1):
            for j in range(self.width-1):
                # Boxes are constructed with lines in the order [top, bottom, left, right]
                ## TODO. THIS NEEDS TO BE CHANGED. Currently only handles square grids.
                self.boxes[i][j] = Box(self.grid[0][i][j], self.grid[0][i+1][j], self.grid[1][j][i], self.grid[1][j+1][i])
        print("Built game grid")

    def build_copy(self, copy_grid, copy_boxes):
        """
        Builds a game board with copied values.
        Args:
            copy_grid: List[][][Line]
            copy_boxes: List[][Box]
        """
        # Build two lists of horizontal and vertical lines using the input grid.
        self.grid = [
            [[Line(j.owner) for j in i] for i in copy_grid[0]],
            [[Line(j.owner) for j in i] for i in copy_grid[1]]
        ]
        # This means grid[0][0][0] is the top left horizontal line
        # grid[1][0][0] is the top left vertical line
        # Then build the box objects in a 2d list
        self.boxes = [[0 for i in range(self.width-1)] for j in range(self.height-1)]
        for i in range(self.height-1):
            for j in range(self.width-1):
                # Boxes are constructed with lines in the order [top, bottom, left, right]
                self.boxes[i][j] = Box(self.grid[0][i][j], self.grid[0][i+1][j], self.grid[1][j][i], self.grid[1][j+1][i], copy_boxes[i][j].owner)

    def get_copy(self):
        """
        Game returns a deep copy of itself.
        Returns:
            Game
        """
        return Game(self.width, self.height, self.grid, self.boxes)

    def take_turn(self, move):
        """
        Takes a turn for next player. Claims a line.
        Returns bool for success. True if player secures a box.
        Args:
            player: int
            move: 3-tuple(int)
        Returns:
            bool
        """
        if self.is_legal_move(move):
            move_results = []
            # Attempt to claim the line.
            self.grid[move[0]][move[1]][move[2]].draw(self.currentPlayer)
            # Now check the boxes that share this edge.
            if move[0] == 0:
                # Edge cases
                if move[1] == 0:
                    move_results.append(self.boxes[move[1]][move[2]].check_completed(self.currentPlayer))
                elif move[1] == self.height-1:
                    move_results.append(self.boxes[move[1]-1][move[2]].check_completed(self.currentPlayer))
                # Middle case
                else:
                    move_results.append(self.boxes[move[1]-1][move[2]].check_completed(self.currentPlayer))
                    move_results.append(self.boxes[move[1]][move[2]].check_completed(self.currentPlayer))
            else:
                if move[1] == 0:
                    move_results.append(self.boxes[move[2]][move[1]].check_completed(self.currentPlayer))
                elif move[1] == self.width-1:
                    move_results.append(self.boxes[move[2]][move[1]-1].check_completed(self.currentPlayer))
                else:
                    move_results.append(self.boxes[move[2]][move[1]-1].check_completed(self.currentPlayer))
                    move_results.append(self.boxes[move[2]][move[1]].check_completed(self.currentPlayer))
            # This will return True if player got a box this move
            if not any(move_results):
                self.currentPlayer += 1
                if self.currentPlayer > self.maxPlayers:
                    self.currentPlayer = 1
        return False

    def is_legal_move(self, move):
        """
        Checks if a certain move is legal.
        Args:
            move: 3-tuple(int)
        Returns:
            bool
        """
        # Check if move is within grid bounds
        if move[0] == 0:
            if 0 > move[1] > self.height-1 or 0 > move[2] >= self.width-1:
                print("Invalid move")
                return False
        elif move[0] == 1:
            if 0 > move[1] > self.width-1 or 0 > move[2] >= self.height-1:
                print("Invalid move")
                return False
        else:
            print("Invalid move")
            return False

        # Check if line has already been claimed
        if self.grid[move[0]][move[1]][move[2]]:
            print("Line has already been claimed")
            return False
        return True

    def is_finished(self):
        """
        Checks if the game is finished or if there are still moves to be made.
        Returns:
            bool
        """
        for i in range(self.height-1):
            for j in range(self.width-1):
                if not self.boxes[i][j]:
                    return False
        return True

    def print_scores(self):
        """
        Print the scores for all players that have any score.
        Also print number of unclaimed boxes.
        """
        print("Scores: ")
        scores = {0:0}
        for i in range(self.height-1):
            for j in range(self.width-1):
                owner = self.boxes[i][j].owner
                if owner in scores:
                    scores[owner] += 1
                else:
                    scores[owner] = 1
        print("Unclaimed Boxes: {}".format(scores.pop(0)))
        for key, value in scores.items():
            print("Player {}: {}".format(key, value))

    def check_score(self, player):
        """
        Get and return the score for one player.
        Args:
            player: int
        Returns:
            int
        """
        score = 0
        for i in range(self.height-1):
            for j in range(self.width-1):
                if self.boxes[i][j].owner == player:
                    score += 1
        return score

    def winner(self):
        """
        If the game is finished, find the winner.
        """
        if self.is_finished():
            scores = {}
            for i in range(self.height-1):
                for j in range(self.width-1):
                    owner = self.boxes[i][j].owner
                    if owner in scores:
                        scores[owner] += 1
                    else:
                        scores[owner] = 1
            return(max(scores, key=scores.get))
        print("Game is not yet finished!")
        return 0


    def print_grid(self):
        """
        Prints an ascii representation of the board.
        For horizontal edges, '- -' is unclaimed, '---' is claimed
        For vertical edges, '¦' is unclaimed, '|' is claimed
        An empty box is unclaimed. A box with a number in is claimed.
        """
        for i in range(self.height):
            for j in range(self.width):
                if j != self.width-1:
                    print("*", end="")
                    if self.grid[0][i][j]:
                        print("---", end="")
                    else:
                        print("- -", end="")
                else:
                    print("*")
            if i != self.height-1:
                for j in range(self.width):
                    if j != self.width-1:
                        if self.grid[1][j][i]:
                            print("|", end="")
                        else:
                            print("¦", end="")
                        print(" {} ".format(self.boxes[i][j]), end="")
                    else:
                        if self.grid[1][j][i]:
                            print("|")
                        else:
                            print("¦")

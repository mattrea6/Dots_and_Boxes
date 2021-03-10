import random
import time

class PlayerFactory:
    """
    Basic player factory that stores a list of all player types and can return
    corresponding player instances.
    """
    def __init__(self):
        self.playerTypes = ["Human Player", "Random Player", "In order player", "Minimax Player"]

    def makePlayer(self, playerType, index, colour):
        """
        Factory method for returning correct player type.
        If for some reason playerType isn't in the internal list, just return a
        human player.
        """
        if playerType not in self.playerTypes:
            return HumanPlayer(index, colour)
        if playerType == "Human Player":
            return HumanPlayer(index, colour)
        elif playerType == "Random Player":
            return RandomPlayer(index, colour)
        elif playerType == "In order player":
            return MovesInOrder(index, colour)
        elif playerType == "Minimax Player":
            return MinimaxPlayer(index, colour)

class PlayerBase:
    """
    Basic class for player base. All players inherit from this model.
    """
    def __init__(self, playerIndex, colour="red"):
        self.index = playerIndex
        self.colour = colour

    def isHuman(self):
        pass

    def __str__(self):
        return "{}_player".format(self.index)

class HumanPlayer(PlayerBase):
    """
    Basic class for human player. Needs no implementation as the human player
    clicks using the UI.
    """
    def __init__(self, playerIndex, colour="blue"):
        """
        Override so human players are blue by default
        """
        super().__init__(playerIndex, colour)

    def isHuman(self):
        """
        Very important. Lets the UI know to give human player control.
        Returns:
            Bool
        """
        return True

    def __str__(self):
        """
        String representation for a random player. Used for writing results filenames.
        """
        return "{}_human".format(self.index)

class RandomPlayer(PlayerBase):
    """
    Most basic AI player. Chooses moves randomly from list of legal moves.
    """
    def chooseMove(self, game):
        """
        Chooses a move for the player by calling random move.
        """
        return self.randomMove(game)

    def randomMove(self, game):
        """
        Get list of legal moves and return any random one.
        """
        time.sleep(0.5)
        return random.choice(game.get_all_legal_moves())

    def isHuman(self):
        """
        Very important. Lets the UI know NOT to give AI player UI control.
        Returns:
            Bool
        """
        return False

    def __str__(self):
        """
        String representation for a random player. Used for writing results filenames.
        """
        return "{}_random".format(self.index)

class MovesInOrder(PlayerBase):
    """
    Plays all of the legal moves in ascending order
    """
    def chooseMove(self, game):
        time.sleep(0.3)
        return game.get_all_legal_moves()[0]

    def __str__(self):
        return "{}_ordered".format(self.index)

class MinimaxPlayer(RandomPlayer):
    """
    Player that implements minimax. Inherits random player for random moves.
    """
    def __init__(self, playerIndex, colour="red", timeLimit=5, maxDepth=10):
        """
        Override for Minimax player to include time limit & max depth.
        This is the time limit given to the player to choose a move, in seconds.
        Args:
            playerIndex(int): player index in game
            colour(str): Colour for the UI to render. Defaults to Red
            timeLimit(int/float): Time limit in seconds for moves
            maxDepth(int): Max depth the computer player can reach.
        """
        self.index = playerIndex
        self.colour = colour
        self.timeLimit = timeLimit
        self.maxDepth = maxDepth

    def chooseMove(self, game):
        """
        Choose move for minimax player.
        """
        moves = game.get_all_legal_moves()
        bestMove = (0, 0, 0)
        bestScore = -10000
        currentMaxDepth = 1
        startTime = time.time()
        # Search at max depth = 1 initially, and then increment the depth.
        # Keep incrementing until the time limit has been reached, then return
        # the best move found so far. This is iterative deepening.
        while time.time() - startTime <= self.timeLimit and currentMaxDepth <= self.maxDepth:
            for move in moves:
                copyGame = self.makeMove(game, move)
                score = self.getScore(copyGame, currentMaxDepth, -10000, 10000)
                # The move that returns the greatest score gets chosen.
                if score >= bestScore:
                    bestScore = score
                    bestMove = move
                # Break if we have reached the end of the time limit.
                if time.time() - startTime >= self.timeLimit:
                    break
            # Increment the current max depth for iterative deepening.
            currentMaxDepth += 1

        # Just in case we picked a bad move. Or no move at all.
        if game.is_legal_move(bestMove):
            return bestMove
        else:
            return self.randomMove(game)

    def getScore(self, game, depth, alpha, beta):
        """
        The recursive part of the mintiimax algorithm.
        This will recursively search the tree to find the scores available at the bottom.
        Args:
            game(Game): game state to branch from.
            depth(int): current depth of search.
            alpha(int): alpha value
            beta(int): beta value
        Returns:
            int
        """
        # When we're at the bottom of the tree, return
        if depth <= 0 or game.is_finished():
            return self.evaluate(game)

        moves = game.get_all_legal_moves()
        # Store the current player
        currentPlayer = game.currentPlayer
        # set bestScore to either high or low value depending on whose turn it is
        # also set maximise to True or False
        if currentPlayer == self.index:
            bestScore = -10000
            maximise = True
        else:
            bestScore = 10000
            maximise = False
        for move in moves:
            # Make the move and get the next state of the game.
            copyGame = self.makeMove(game, move)
            if copyGame.currentPlayer == currentPlayer:
                # If the current player hasn't changed then a box was claimed.
                # Don't increment the depth
                # This allows the player to see further forward when capturing
                # but adds a little to the search time.
                newDepth = depth
            else:
                newDepth = depth-1
            # recursive call
            score = self.getScore(copyGame, newDepth, alpha, beta)
            # Different actions depending on wether this is a min node or max node
            if maximise:
                bestScore = max(score, bestScore)
                alpha = max(alpha, bestScore)
            else:
                bestScore = min(score, bestScore)
                beta = min(beta, bestScore)
                # Alpha - beta pruning.
                if beta <= alpha:
                    break
        #print("Minimax returning {}".format(bestScore))
        #print("All scores: {}".format(scores))
        #print("Returning best score: {}".format(bestScore))
        return bestScore

    def evaluate(self, game):
        """
        Evaluate a particular game state. Get a static score
        """
        # Find our own index and the other players
        if self.index == 1:
            otherIndex = 2
        else:
            otherIndex = 1
        # If the game hasn't been won yet, the board needs to be evaluated.
        score = 0
        scores = game.get_scores()
        ## TODO - MAKE THIS BETTER
        # Add 5 points for every box player has
        score += 10*scores[self.index]
        # Remove 5 for every box opponent has
        score -= 10*scores[otherIndex]
        # If it's our turn next then we want boxes to complete
        if game.currentPlayer == self.index:
            for i in range(game.height-1):
                for j in range(game.width-1):
                    no_sides = game.boxes[i][j].sides_completed()
                    # 0 or 1. Don't care
                    if no_sides == 0 or no_sides == 1:
                        pass
                    # Only two, we don't want to make the third.
                    elif no_sides == 2:
                        score -= 1
                    # Three sides means we can complete the fourth and get points
                    elif no_sides == 3:
                        score += 5

        # If it's their turn next we don't want them to complete boxes
        elif game.currentPlayer == otherIndex:
            for i in range(game.height-1):
                for j in range(game.width-1):
                    no_sides = game.boxes[i][j].sides_completed()
                    # 0 or 1. Don't care
                    if no_sides == 0 or no_sides == 1:
                        pass
                    # Only two, we want them to make the third.
                    elif no_sides == 2:
                        score += 1
                    # Three sides means they can complete the fourth and get points
                    elif no_sides == 3:
                        score -= 5
        #print("Eval returning {}".format(score))
        return score

    def makeMove(self, game, move):
        """
        Takes a game and a move, copies the game and makes the move in it.
        Args:
            game(Game): Game to be played in.
            move(Tuple[int]): Move to make
        Returns:
            Game: Deep copy of Game with move made
        """
        copyGame = game.get_copy()
        copyGame.take_turn(move)
        return copyGame

    def __str__(self):
        """
        String representation for minimax player. Used for writing results filenames.
        """
        return "{}_minimax".format(self.index)

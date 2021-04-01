try:
    from BasicPlayers import *
    from MinimaxPlayer import MinimaxPlayer
    from MonteCarloPlayer import MonteCarloPlayer
except ModuleNotFoundError:
    from DotsAndBoxes.BasicPlayers import *
    from DotsAndBoxes.MinimaxPlayer import MinimaxPlayer
    from DotsAndBoxes.MonteCarloPlayer import MonteCarloPlayer
import random
import time

class PlayerFactory:
    """
    Basic player factory that stores a list of all player types and can return
    corresponding player instances.
    """
    def __init__(self):
        self.playerTypes = ["Human Player", "Random Player", "In order player", "Minimax Player", "Monte Carlo Player"]

    def makePlayer(self, playerType, index, colour="red", timeLimit=1, maxDepth=20, c=1.4):
        """
        Factory method for returning correct player type.
        If for some reason playerType isn't in the internal list, just return a
        human player.
        Args:
            playerType(str): Type of player to create. This should be contained in self.playerTypes
            index(int): Index of player to create. Usually 1 or 2.
            colour(str) - 'red': Colour to pass to player. Used for GUI.
            timeLimit(int) - 1: Time limit for the complex AI players.
            maxDepth(int) - 20: Max depth that Minimax player can reach.
            c(float) - 1.4: Exploration parameter for Monte Carlo player.
        Returns:
            Player - One of the player types.
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
            return MinimaxPlayer(index, colour, timeLimit, maxDepth)
        elif playerType == "Monte Carlo Player":
            return MonteCarloPlayer(index, colour, timeLimit, c)

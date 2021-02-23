import random

class PlayerFactory:
    """
    Basic player factory that stores a list of all player types and can return
    corresponding player instances.
    """
    def __init__(self):
        self.playerTypes = ["Human Player", "Random Player"]

    def makePlayer(self, playerType, index, colour):
        if playerType not in self.playerTypes:
            return HumanPlayer(index, colour)
        if playerType == "Human Player":
            return HumanPlayer(index, colour)
        elif playerType == "Random Player":
            return RandomPlayer(index, colour)

class PlayerBase:
    """
    Basic class for player base. All players inherit from this model.
    """
    def __init__(self, playerIndex, colour):
        self.index = playerIndex
        self.colour = colour

    def isHuman(self):
        pass

class HumanPlayer(PlayerBase):
    """
    Basic class for human player. Needs no implementation as the human player
    clicks using the UI.
    """
    def isHuman(self):
        """
        Very important. Lets the UI know to give human player control.
        Returns:
            Bool
        """
        return True

class RandomPlayer(PlayerBase):
    """
    Most basic AI player. Chooses moves randomly from list of legal moves.
    """
    def chooseMove(self, game):
        """
        Get list of legal moves and return any random one.
        """
        return random.choice(game.get_all_legal_moves())

    def isHuman(self):
        """
        Very important. Lets the UI know NOT to give AI player UI control.
        Returns:
            Bool
        """
        return False

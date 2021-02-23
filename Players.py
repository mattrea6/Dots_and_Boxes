import random

class PlayerFactory:
    def __init__(self):
        self.playerTypes = ["HumanPlayer", "AIPlayer"]

    def makePlayer(self, playerType, index):
        if playerType not in self.playerTypes:
            return False
        if playerType == "HumanPlayer":
            return HumanPlayer(index)
        elif playerType == "AIPlayer":
            return AIPlayer(index)

class HumanPlayer:
    def __init__(self, playerIndex):
        self.index = playerIndex

    def isHuman(self):
        return True

class AIPlayer:
    def __init__(self, playerIndex):
        self.index = playerIndex

    def chooseMove(self, game):
        return random.choice(game.get_all_legal_moves())

    def isHuman(self):
        return False

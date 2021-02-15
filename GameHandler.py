from Game import Game

class GameHandler:
    def __init__(self, width=4, height=4):
        self.game = Game(width, height)
        self.no_players = 2


    def play_game(self):
        """
        Can play the game. Simply loops inputting moves with a catch so invalid
        moves are asked for again.
        """
        player = 0
        while not self.game.is_finished():
            self.game.print_grid()
            self.game.print_scores()
            player = self.game.currentPlayer
            moveRaw = input("\nPlayer {} enter your move: ".format(player))
            move = [int(x) for x in moveRaw.split()]
            while not self.game.is_legal_move(move):
                moveRaw = input("Player {} enter your move: ".format(player))
                move = [int(x) for x in moveRaw.split()]
            self.game.take_turn(move)

        self.game.print_grid()
        print("Player {} wins!".format(self.game.winner()))

w = int(input("Enter Width: "))
h = int(input("Enter Height: "))
newGame = GameHandler(w,h)
newGame.play_game()

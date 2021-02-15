from Game import Game

class GameHandler:
    def __init__(self, width=4, height=4):
        self.game = Game(width, height)
        self.no_players = 2


    def play_game(self):
        """
        Can play the game. Some of the 'rules' of the game are included here,
        such as picking which player gets a turn next.
        """
        player = 0
        while not self.game.is_finished():
            player += 1
            if 0 <= player > self.no_players:
                player = 1
            self.game.print_grid()
            self.game.print_scores()
            moveRaw = input("\nPlayer {} enter your move: ".format(player))
            move = [int(x) for x in moveRaw.split()]
            while not self.game.is_legal_move(move):
                moveRaw = input("Player {} enter your move: ".format(player))
                move = [int(x) for x in moveRaw.split()]
            if self.game.take_turn(player, move):
                player -= 1

        self.game.print_grid()
        print("Player {} wins!".format(self.game.winner()))

newGame = GameHandler()
newGame.play_game()

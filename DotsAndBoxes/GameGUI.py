import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QLabel, QSpinBox,
    QComboBox, QColorDialog, QDoubleSpinBox, QRadioButton)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from Game import Game
from GameVariants import SwedishGame, RandomGame
import PlayerFactory

class StartFrame(QWidget):
    """
    Start frame class includes game options, and can launch the game with these options
    """
    def __init__(self):
        super().__init__()
        self.playerFactory = PlayerFactory.PlayerFactory()
        self.p1Col = "Red"
        self.p2Col = "Blue"
        self.initUI()

    def initUI(self):
        """
        Simple start window that asks for game options.
        Has a button that launches the game window.
        """
        self.setWindowTitle("Dots and Boxes")
        self.setGeometry(700, 200, 600, 450)
        # Title label
        titleLabel = QLabel("Dots & Boxes", self)
        titleLabel.setFont(QFont('Arial', 20))
        titleLabel.resize(titleLabel.sizeHint())
        titleLabel.move(215, 25)
        # Welcome label
        instLabel = QLabel("Choose board size and players, then click 'Start Game'!", self)
        instLabel.resize(instLabel.sizeHint())
        instLabel.move(175, 65)
        # Input for size
        # Two number input boxes
        widthLabel = QLabel("Width:", self)
        widthLabel.resize(widthLabel.sizeHint())
        widthLabel.move(180, 103)
        self.widthInput = QSpinBox(self)
        self.widthInput.resize(self.widthInput.sizeHint())
        self.widthInput.move(220, 100)
        self.widthInput.setRange(3, 10)

        heightLabel = QLabel("Height:", self)
        heightLabel.resize(heightLabel.sizeHint())
        heightLabel.move(310, 103)
        self.heightInput = QSpinBox(self)
        self.heightInput.resize(self.heightInput.sizeHint())
        self.heightInput.move(350, 100)
        self.heightInput.setRange(3, 10)

        # Input for players. Dropdowns filled with values from factory
        # Create label first
        playerOneLabel = QLabel("Player One:", self)
        playerOneLabel.resize(playerOneLabel.sizeHint())
        playerOneLabel.move(170, 183)
        # Then create the dropdown and size it
        self.playerOneDropdown = QComboBox(self)
        self.playerOneDropdown.resize(100, 20)
        self.playerOneDropdown.move(240, 180)
        self.playerOneDropdown.currentIndexChanged.connect(self.playerPickerChanged)
        # Create the colour picker button for player colour
        self.playerOneColour = QPushButton("Colour", self)
        self.playerOneColour.resize(self.playerOneColour.sizeHint())
        self.playerOneColour.move(350, 180)
        self.playerOneColour.setStyleSheet("background-color: {}".format(self.p1Col))
        self.playerOneColour.clicked.connect(self.playerOneColourPicker)

        # These are the optional boxes that should only appear for specific player types.
        self.playerOneTimeLabel = QLabel("P1 Time Limit:", self)
        self.playerOneTimeLabel.resize(0,0)
        self.playerOneTimeLabel.move(100, 208)

        self.playerOneTimeLimit = QDoubleSpinBox(self)
        self.playerOneTimeLimit.resize(0,0)
        self.playerOneTimeLimit.move(170, 205)
        self.playerOneTimeLimit.setRange(0.2, 20.0)
        self.playerOneTimeLimit.setSingleStep(0.1)

        self.playerOneMaxDepthLabel = QLabel("P1 Max Depth:", self)
        self.playerOneMaxDepthLabel.resize(0,0)
        self.playerOneMaxDepthLabel.move(240, 208)

        self.playerOneMaxDepth = QSpinBox(self)
        self.playerOneMaxDepth.resize(0,0)
        self.playerOneMaxDepth.move(315, 205)
        self.playerOneMaxDepth.setRange(2, 50)
        self.playerOneMaxDepth.setValue(15)

        self.playerOneCValueLabel = QLabel("P1 C Value:", self)
        self.playerOneCValueLabel.resize(0,0)
        self.playerOneCValueLabel.move(240, 208)

        self.playerOneCValue = QDoubleSpinBox(self)
        self.playerOneCValue.resize(0,0)
        self.playerOneCValue.move(300, 205)
        self.playerOneCValue.setRange(0.0, 10.0)
        self.playerOneCValue.setSingleStep(0.05)


        playerTwoLabel = QLabel("Player Two:", self)
        playerTwoLabel.resize(playerTwoLabel.sizeHint())
        playerTwoLabel.move(100, 243)
        self.playerTwoDropdown = QComboBox(self)
        self.playerTwoDropdown.resize(100, 20)
        self.playerTwoDropdown.move(170, 240)
        self.playerTwoDropdown.currentIndexChanged.connect(self.playerPickerChanged)
        self.playerTwoColour = QPushButton("Colour", self)
        self.playerTwoColour.resize(self.playerTwoColour.sizeHint())
        self.playerTwoColour.move(280, 240)
        self.playerTwoColour.setStyleSheet("background-color: {}".format(self.p2Col))
        self.playerTwoColour.clicked.connect(self.playerTwoColourPicker)

        self.playerTwoTimeLabel = QLabel("P2 Time Limit:", self)
        self.playerTwoTimeLabel.resize(0,0)
        self.playerTwoTimeLabel.move(100, 268)

        self.playerTwoTimeLimit = QDoubleSpinBox(self)
        self.playerTwoTimeLimit.resize(0,0)
        self.playerTwoTimeLimit.move(170, 265)
        self.playerTwoTimeLimit.setRange(0.2, 20.0)
        self.playerTwoTimeLimit.setSingleStep(0.1)

        self.playerTwoMaxDepthLabel = QLabel("P2 Max Depth:", self)
        self.playerTwoMaxDepthLabel.resize(0,0)
        self.playerTwoMaxDepthLabel.move(240, 268)

        self.playerTwoMaxDepth = QSpinBox(self)
        self.playerTwoMaxDepth.resize(0,0)
        self.playerTwoMaxDepth.move(315, 265)
        self.playerTwoMaxDepth.setRange(2, 50)
        self.playerTwoMaxDepth.setValue(15)

        self.playerTwoCValueLabel = QLabel("P2 C Value:", self)
        self.playerTwoCValueLabel.resize(0,0)
        self.playerTwoCValueLabel.move(240, 268)

        self.playerTwoCValue = QDoubleSpinBox(self)
        self.playerTwoCValue.resize(0,0)
        self.playerTwoCValue.move(300, 265)
        self.playerTwoCValue.setRange(0.0, 10.0)
        self.playerTwoCValue.setSingleStep(0.05)

        # Populate both dropdowns with the player types in Player Factory.
        for player in self.playerFactory.playerTypes:
            self.playerOneDropdown.addItem(player)
            self.playerTwoDropdown.addItem(player)

        variantLabel = QLabel("Select Game Variant:", self)
        variantLabel.resize(variantLabel.sizeHint())
        variantLabel.move(100, 300)

        self.normalGameRadio = QRadioButton("American Game", self)
        self.normalGameRadio.move(100, 320)
        self.normalGameRadio.setChecked(True)
        self.swedishGameRadio = QRadioButton("Swedish Game", self)
        self.swedishGameRadio.move(200, 320)
        self.randomGameRadio = QRadioButton("Random Game", self)
        self.randomGameRadio.move(295, 320)

        # Button to start game
        startButton = QPushButton('Start Game', self)
        startButton.resize(startButton.sizeHint())
        startButton.move(100, 350)
        startButton.clicked.connect(self.startGame)

        self.show()

    def playerPickerChanged(self):
        """
        Callback for when the value of a player type picker changes.
        """
        p1type = self.playerOneDropdown.currentText()
        p2type = self.playerTwoDropdown.currentText()

        if p1type == "Minimax Player":
            # If dropdown is minimax player, resize the minimax options to their correct sizes
            self.playerOneTimeLabel.resize(self.playerOneTimeLabel.sizeHint())
            self.playerOneTimeLimit.resize(50, 20)
            self.playerOneMaxDepthLabel.resize(self.playerOneMaxDepthLabel.sizeHint())
            self.playerOneMaxDepth.resize(40, 20)

            self.playerOneCValueLabel.resize(0,0)
            self.playerOneCValue.resize(0,0)
        elif p1type == "Monte Carlo Player":
            # If it is monte carlo player, resize these relevant options
            self.playerOneTimeLabel.resize(self.playerOneTimeLabel.sizeHint())
            self.playerOneTimeLimit.resize(50, 20)
            self.playerOneCValueLabel.resize(self.playerOneCValueLabel.sizeHint())
            self.playerOneCValue.resize(50, 20)

            self.playerOneMaxDepthLabel.resize(0,0)
            self.playerOneMaxDepth.resize(0,0)
        else:
            # If it is neither of those, make all of these elements invisible.
            self.playerOneTimeLabel.resize(0,0)
            self.playerOneTimeLimit.resize(0,0)
            self.playerOneCValueLabel.resize(0,0)
            self.playerOneCValue.resize(0,0)
            self.playerOneMaxDepthLabel.resize(0,0)
            self.playerOneMaxDepth.resize(0,0)

        if p2type == "Minimax Player":
            # If dropdown is minimax player, resize the minimax options to their correct sizes
            self.playerTwoTimeLabel.resize(self.playerTwoTimeLabel.sizeHint())
            self.playerTwoTimeLimit.resize(50, 20)
            self.playerTwoMaxDepthLabel.resize(self.playerTwoMaxDepthLabel.sizeHint())
            self.playerTwoMaxDepth.resize(40, 20)

            self.playerTwoCValueLabel.resize(0,0)
            self.playerTwoCValue.resize(0,0)
        elif p2type == "Monte Carlo Player":
            # If it is monte carlo player, resize these relevant options
            self.playerTwoTimeLabel.resize(self.playerTwoTimeLabel.sizeHint())
            self.playerTwoTimeLimit.resize(50, 20)
            self.playerTwoCValueLabel.resize(self.playerTwoCValueLabel.sizeHint())
            self.playerTwoCValue.resize(50, 20)

            self.playerTwoMaxDepthLabel.resize(0,0)
            self.playerTwoMaxDepth.resize(0,0)
        else:
            # If it is neither of those, make all of these elements invisible.
            self.playerTwoTimeLabel.resize(0,0)
            self.playerTwoTimeLimit.resize(0,0)
            self.playerTwoCValueLabel.resize(0,0)
            self.playerTwoCValue.resize(0,0)
            self.playerTwoMaxDepthLabel.resize(0,0)
            self.playerTwoMaxDepth.resize(0,0)

    def playerOneColourPicker(self):
        """
        Callback for p1 colour picker button
        """
        self.p1Col = QColorDialog.getColor().name()
        self.playerOneColour.setStyleSheet("background-color: {}".format(self.p1Col))

    def playerTwoColourPicker(self):
        """
        Callback for p2 colour picker button
        """
        self.p2Col = QColorDialog.getColor().name()
        self.playerTwoColour.setStyleSheet("background-color: {}".format(self.p2Col))

    def startGame(self):
        """
        Starts game. Creates two players with values from inputs using the Player Factory class.
        Then creates game and sends it options and players. Finally closes itself.
        """
        playerOne = self.playerFactory.makePlayer(
            self.playerOneDropdown.currentText(),
            1,
            self.p1Col,
            self.playerOneTimeLimit.value(),
            self.playerOneMaxDepth.value(),
            self.playerOneCValue.value()
            )

        playerTwo = self.playerFactory.makePlayer(
            self.playerTwoDropdown.currentText(),
            2,
            self.p2Col,
            self.playerTwoTimeLimit.value(),
            self.playerTwoMaxDepth.value(),
            self.playerTwoCValue.value()
            )

        players = [playerOne, playerTwo]

        if self.normalGameRadio.isChecked():
            game = Game(self.widthInput.value(), self.heightInput.value())
        elif self.swedishGameRadio.isChecked():
            game = SwedishGame(self.widthInput.value(), self.heightInput.value())
        elif self.randomGameRadio.isChecked():
            game = RandomGame(self.widthInput.value(), self.heightInput.value())
        else:
            game = Game(self.widthInput.value(), self.heightInput.value())
        self.gf = GameFrame(game, players)
        self.close()


class GameFrame(QWidget):

    def __init__(self, game, players, filename=False):
        """
        GameFrame is a QWidget that can also hold and read a Game instance, and a list
        of current players in the game.
        Args:
            width: int
            height: int
            players: List[PlayerBase]
        """
        super().__init__()
        self.players = players
        self.p1Colour = self.players[0].colour
        self.p2Colour = self.players[1].colour
        self.blockedColour = "Black"
        self.game = game
        self.width = game.width
        self.height = game.height
        self.resultsFilename = filename
        self.boxSize = 50
        self.lineWidth = 10
        self.initUI()


    def initUI(self):
        """
        Initialise the UI. Set up the window, turn and winner text labels.
        Set up the grid of lines as buttons that can be clicked, and set the boxes
        as labels with no value.
        """
        # Set title
        self.setWindowTitle("Dots and Boxes")
        self.setGeometry(700, 200, 600, 450)

        # Set turn label
        self.titleLabel = QLabel("Player 1's turn!", self)
        self.titleLabel.resize(self.titleLabel.sizeHint())
        self.titleLabel.move(100, 50)

        # Create winner label with no text
        self.winnerLabel = QLabel("", self)
        self.winnerLabel.resize(self.winnerLabel.sizeHint())

        # Create Play Again button but do not make visible.
        self.replayButton = QPushButton("Play Again!", self)
        self.replayButton.resize(self.replayButton.sizeHint())
        self.replayButton.move(1000, 1000)
        self.replayButton.clicked.connect(self.replay)

        # Build board.
        # Lists of buttons?
        # Or just objects that can be clicked?
        #who nose
        topLeftX = 100
        topLeftY = 100
        # Build an array of button objects - this is the same list constructor as
        # the one to build the array of Lines in Game.
        self.buttonGrid = [
            [[GameButton(self) for j in range(self.width-1)] for i in range(self.height)],
            [[GameButton(self) for j in range(self.height-1)] for i in range(self.width)]
        ]
        o = 0
        x = topLeftX
        y = topLeftY
        # Go through each button object and set its properties
        for i in range(self.height):
            x = topLeftX+self.lineWidth
            for j in range(self.width-1):
                # Make it the right size & orientation
                self.buttonGrid[o][i][j].resize(self.boxSize, self.lineWidth)
                # Place it
                self.buttonGrid[o][i][j].move(x, y)
                # Set the tooltip and value so we know which button is which
                self.buttonGrid[o][i][j].setToolTip('{} {} {}'.format(o,i,j))
                self.buttonGrid[o][i][j].value = (o, i, j)
                # Set the callback function
                self.buttonGrid[o][i][j].clicked.connect(self.lineClicked)
                # Disable the button so it can't be clicked when it shouldn't
                self.buttonGrid[o][i][j].setEnabled(False)
                # Adjust the offsets for next button
                x = x + self.lineWidth + self.boxSize
            y = y + self.lineWidth + self.boxSize

        # now do it again for the verticals
        o = 1
        x = topLeftX
        for i in range(self.width):
            y = topLeftY+self.lineWidth
            for j in range(self.height-1):
                self.buttonGrid[o][i][j].resize(self.lineWidth, self.boxSize)
                self.buttonGrid[o][i][j].move(x, y)
                self.buttonGrid[o][i][j].setToolTip('{} {} {}'.format(o,i,j))
                self.buttonGrid[o][i][j].value = (o, i, j)
                self.buttonGrid[o][i][j].clicked.connect(self.lineClicked)
                self.buttonGrid[o][i][j].setEnabled(False)
                y = y + self.lineWidth + self.boxSize
            x = x + self.lineWidth + self.boxSize

        # Now build grid of labels to show box owner.
        # Labels are initially empty strings, updated in update()
        self.boxes = [[QLabel("",self) for i in range(self.width-1)] for j in range(self.height-1)]
        y = topLeftY + self.lineWidth
        for i in range(self.height-1):
            x = topLeftX + self.lineWidth
            for j in range(self.width-1):
                self.boxes[i][j].resize(self.boxSize, self.boxSize)
                self.boxes[i][j].move(x, y)
                self.boxes[i][j].setAlignment(QtCore.Qt.AlignCenter)
                x = x + self.lineWidth + self.boxSize
            y = y + self.lineWidth + self.boxSize

        self.show()
        QApplication.processEvents()
        self.updateGame()
        #self.mainLoop()

    def mainLoop(self):
        """
        Main loop run every turn.
        Decides what happens when a human player or AI Player takes a turn.
        """
        currentPlayer = self.players[self.game.currentPlayer-1]
        if currentPlayer.isHuman():
            self.humanTurn()
        else:
            # Send the AI player a copy of the game board right now and it will
            # return a move.
            move = currentPlayer.chooseMove(self.game.get_copy())
            self.makeMove(move)

    def humanTurn(self):
        """
        Logic that the game runs through when a human player is taking their turn.
        Enables all of the buttons that should be enabled.
        """
        # Enable all of the buttons that correspond to legal moves.
        for move in self.game.get_all_legal_moves():
            self.buttonGrid[move[0]][move[1]][move[2]].setEnabled(True)


    def updateGame(self):
        """
        Updates the display after each player's turn.
        """
        # Update turn label
        self.titleLabel.setText("Player {}s turn!".format(self.game.currentPlayer))
        self.titleLabel.resize(self.titleLabel.sizeHint())
        # update line colours
        for i in range(self.height):
            for j in range(self.width-1):
                line_owner = self.game.grid[0][i][j].owner
                if line_owner == 1:
                    self.buttonGrid[0][i][j].setStyleSheet("background-color: {}".format(self.p1Colour))
                elif line_owner == 2:
                    self.buttonGrid[0][i][j].setStyleSheet("background-color: {}".format(self.p2Colour))
                elif line_owner == 3:
                    self.buttonGrid[0][i][j].setStyleSheet("background-color: {}".format(self.blockedColour))
        for i in range(self.width):
            for j in range(self.height-1):
                line_owner = self.game.grid[1][i][j].owner
                if line_owner == 1:
                    self.buttonGrid[1][i][j].setStyleSheet("background-color: {}".format(self.p1Colour))
                elif line_owner == 2:
                    self.buttonGrid[1][i][j].setStyleSheet("background-color: {}".format(self.p2Colour))
                elif line_owner == 3:
                    self.buttonGrid[1][i][j].setStyleSheet("background-color: {}".format(self.blockedColour))
        # Update grid for box numbers
        for i in range(self.height-1):
            for j in range(self.width-1):
                owner = self.game.boxes[i][j].owner
                if owner != 0:
                    # This sets the text for owner number and sets box colour.
                    self.boxes[i][j].setText("{}".format(owner))
                    self.boxes[i][j].setStyleSheet("background-color: {}".format(self.players[owner-1].colour))
        # Force the GUI to update. This is for games with no human player.
        QApplication.processEvents()
        # If the game isn't done yet, go back to the main loop.
        if not self.game.is_finished():
            self.mainLoop()
        # If the game is finished, set the winner label
        else:
            # Hide title label
            self.titleLabel.resize(0,0)
            # Update the string that says who won.
            winner = self.game.winner()
            if winner == 0:
                winnerStr = "It's a draw!"
            else:
                winnerStr = "Player {} wins!".format(self.game.winner())
            print(winnerStr)
            self.winnerLabel.setText(winnerStr)
            self.winnerLabel.resize(self.winnerLabel.sizeHint())
            self.winnerLabel.move(200, 50)
            self.replayButton.move(250, 75)
            # If a results filename has been passed to GameFrame then save the
            # game stats to this location and close the frame.
            if self.resultsFilename:
                self.game.save_statistics(self.resultsFilename, "a+")
                self.close()

    def lineClicked(self):
        """
        Callback for 'line' buttons. Identifies which button was pressed, and then
        takes the turn for that button.
        """
        sender = self.sender()
        self.disableAllButtons()
        self.makeMove(sender.value)

    def makeMove(self, move):
        """
        Makes a move.
        Args:
            move: 3-tuple[int]
        """
        print("Player {} making move {}.".format(self.game.currentPlayer, move))
        # Set the colour of the line that was just played.
        button = self.buttonGrid[move[0]][move[1]][move[2]]
        if self.game.currentPlayer == 1:
            button.setStyleSheet("background-color: {}".format(self.p1Colour))
        elif self.game.currentPlayer == 2:
            button.setStyleSheet("background-color: {}".format(self.p2Colour))
        # Then send the move to the game
        self.game.take_turn(move)
        self.updateGame()

    def disableAllButtons(self):
        """
        Disables all buttons that are part of the game grid.
        """
        o = 0
        for i in range(self.height):
            for j in range(self.width-1):
                self.buttonGrid[o][i][j].setEnabled(False)
        o = 1
        for i in range(self.width):
            for j in range(self.height-1):
                self.buttonGrid[o][i][j].setEnabled(False)

    def replay(self):
        """
        Replay function. Creates a new start frame and then destroys itself.
        """
        self.sf = StartFrame()
        self.close()

class GameButton(QPushButton):
    """
    A very simple subclassed version of QPushButton that also holds a value.
    This is so when a button is pressed in the game, it knows its corresponding move
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.value = (-1, 0, 0)

def main():
    app = QApplication(sys.argv)
    ex = StartFrame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

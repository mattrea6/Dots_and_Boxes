import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QLabel, QSpinBox)
from PyQt5.QtGui import QFont
from Game import Game


class StartFrame(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Simple start window that asks for game options.
        Has a button that launches the game window.
        """
        self.setWindowTitle("Dots and Boxes")
        self.setGeometry(200, 200, 600, 450)
        # Title label
        titleLabel = QLabel("Dots & Boxes", self)
        titleLabel.resize(titleLabel.sizeHint())
        titleLabel.move(100, 50)
        # Welcome label
        instLabel = QLabel("Choose board size and players, then click 'Start Game'!", self)
        instLabel.resize(instLabel.sizeHint())
        instLabel.move(100, 65)
        # Input for size
        # Two number input boxes
        self.widthInput = QSpinBox(self)
        self.widthInput.resize(self.widthInput.sizeHint())
        self.widthInput.move(100, 100)
        self.widthInput.setRange(3, 10)
        self.heightInput = QSpinBox(self)
        self.heightInput.resize(self.heightInput.sizeHint())
        self.heightInput.move(100, 120)
        self.heightInput.setRange(3, 10)

        #Input for players?
        #blank for now. Dropdowns later? with factory values

        # Button to start game
        startButton = QPushButton('Start Game', self)
        startButton.resize(startButton.sizeHint())
        startButton.move(100, 200)
        startButton.clicked.connect(self.startGame)

        self.show()

    def startGame(self):
        self.gf = GameFrame(self.widthInput.value(), self.heightInput.value())
        self.close()


class GameFrame(QWidget):

    def __init__(self, width, height):
        """
        GameFrame is a QWidget that can also hold and read a Game instance
        """
        super().__init__()
        self.width = width
        self.height = height
        self.game = Game(width, height)
        self.boxSize = 50
        self.lineWidth = 10
        self.initUI()


    def initUI(self):
        """
        Initialise the UI. Set up the window, turn and winner text labels.
        Set up the grid of lines as buttons that can be clicked, and set the boxes
        as labels with no value.
        """
        self.setWindowTitle("Dots and Boxes")
        self.setGeometry(200, 200, 600, 450)

        self.titleLabel = QLabel("Player 1's turn!", self)
        self.titleLabel.resize(self.titleLabel.sizeHint())
        self.titleLabel.move(100, 50)

        self.winnerLabel = QLabel("", self)
        self.winnerLabel.resize(self.winnerLabel.sizeHint())

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
                x = x + self.lineWidth + self.boxSize
            y = y + self.lineWidth + self.boxSize

        self.show()

    def update(self):
        """
        Updates the display after each player's turn.
        """
        # Update turn label
        self.titleLabel.setText("Player {}'s turn!".format(self.game.currentPlayer))
        self.titleLabel.resize(self.titleLabel.sizeHint())
        # Update grid for box numbers
        for i in range(self.height-1):
            for j in range(self.width-1):
                owner = self.game.boxes[i][j].owner
                if owner != 0:
                    self.boxes[i][j].setText("{}".format(owner))

        # If the game is finished, set the winner label
        if self.game.is_finished():
            winnerStr = "Player {} wins!".format(self.game.winner())
            self.winnerLabel.setText(winnerStr)
            self.winnerLabel.resize(self.winnerLabel.sizeHint())
            self.winnerLabel.move(200, 50)


    def lineClicked(self):
        """
        Callback for 'line' buttons. Identifies which button was pressed, and then
        takes the turn for that button.
        Also makes the button unclickable, and recolours it depending on player.
        Finally calls update() to update the display.
        """
        sender = self.sender()
        curPlayer = self.game.currentPlayer
        self.game.take_turn(sender.value)
        if curPlayer == 1:
            sender.setStyleSheet("background-color: red")
        elif curPlayer == 2:
            sender.setStyleSheet("background-color: blue")
        sender.setEnabled(False)
        self.update()


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

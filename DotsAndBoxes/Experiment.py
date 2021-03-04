import sys
import os
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QLabel, QSpinBox,
    QComboBox, QColorDialog)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from Game import Game
import GameGUI
import Players

class ExperimentFrame(QWidget):
    """
    Start frame class includes game options, and can launch the game with these options
    """
    def __init__(self):
        super().__init__()
        self.playerFactory = Players.PlayerFactory()
        self.p1Col = "Red"
        self.p2Col = "Blue"
        self.initUI()

    def initUI(self):
        """
        Simple start window that asks for game options.
        Has a button that launches the game window.
        """
        # set up list of all elements for easy access later
        self.elements = []
        # set up window
        self.setWindowTitle("Dots and Boxes")
        self.setGeometry(200, 200, 600, 450)
        # Title label
        titleLabel = QLabel("Dots & Boxes", self)
        titleLabel.resize(titleLabel.sizeHint())
        titleLabel.move(100, 50)
        self.elements.append(titleLabel)
        # Welcome label
        instLabel = QLabel("Choose board size and players, then click 'Start Game'!", self)
        instLabel.resize(instLabel.sizeHint())
        instLabel.move(100, 65)
        self.elements.append(instLabel)
        # Input for size
        # Two number input boxes
        widthLabel = QLabel("Width:", self)
        widthLabel.resize(widthLabel.sizeHint())
        widthLabel.move(100, 103)
        self.elements.append(widthLabel)
        self.widthInput = QSpinBox(self)
        self.widthInput.resize(self.widthInput.sizeHint())
        self.widthInput.move(150, 100)
        self.widthInput.setRange(3, 10)
        self.elements.append(self.widthInput)

        heightLabel = QLabel("Height:", self)
        heightLabel.resize(heightLabel.sizeHint())
        heightLabel.move(100, 123)
        self.elements.append(heightLabel)
        self.heightInput = QSpinBox(self)
        self.heightInput.resize(self.heightInput.sizeHint())
        self.heightInput.move(150, 120)
        self.heightInput.setRange(3, 10)
        self.elements.append(self.heightInput)

        # Input for players. Dropdowns filled with values from factory
        # Create label first
        playerOneLabel = QLabel("Player One:", self)
        playerOneLabel.resize(playerOneLabel.sizeHint())
        playerOneLabel.move(100, 183)
        self.elements.append(playerOneLabel)
        # Then create the dropdown and size it
        self.playerOneDropdown = QComboBox(self)
        self.playerOneDropdown.resize(100, 20)
        self.playerOneDropdown.move(170, 180)
        self.elements.append(self.playerOneDropdown)
        # Create the colour picker button for player colour
        self.playerOneColour = QPushButton("Colour", self)
        self.playerOneColour.resize(self.playerOneColour.sizeHint())
        self.playerOneColour.move(280, 180)
        self.playerOneColour.setStyleSheet("background-color: {}".format(self.p1Col))
        self.playerOneColour.clicked.connect(self.playerOneColourPicker)
        self.elements.append(self.playerOneColour)

        playerTwoLabel = QLabel("Player Two:", self)
        playerTwoLabel.resize(playerTwoLabel.sizeHint())
        playerTwoLabel.move(100, 203)
        self.elements.append(playerTwoLabel)
        self.playerTwoDropdown = QComboBox(self)
        self.playerTwoDropdown.resize(100, 20)
        self.playerTwoDropdown.move(170, 200)
        self.elements.append(self.playerTwoDropdown)
        self.playerTwoColour = QPushButton("Colour", self)
        self.playerTwoColour.resize(self.playerTwoColour.sizeHint())
        self.playerTwoColour.move(280, 200)
        self.playerTwoColour.setStyleSheet("background-color: {}".format(self.p2Col))
        self.playerTwoColour.clicked.connect(self.playerTwoColourPicker)
        self.elements.append(self.playerTwoColour)
        # Populate both dropdowns with the player types in Player Factory.
        for player in self.playerFactory.playerTypes:
            self.playerOneDropdown.addItem(player)
            self.playerTwoDropdown.addItem(player)

        # Number of iterations picker.
        iterPickerLabel = QLabel("Number of Trials:", self)
        iterPickerLabel.resize(iterPickerLabel.sizeHint())
        iterPickerLabel.move(100, 250)
        self.elements.append(iterPickerLabel)
        self.numTrials = QSpinBox(self)
        self.numTrials.resize(self.numTrials.sizeHint())
        self.numTrials.move(190, 250)
        self.numTrials.setRange(10, 1000)
        self.elements.append(self.numTrials)

        # Button to start game
        startButton = QPushButton('Start Experiment', self)
        startButton.resize(startButton.sizeHint())
        startButton.move(100, 280)
        startButton.clicked.connect(self.startExperiment)
        self.elements.append(startButton)

        self.show()

    def hideAllElements(self):
        """
        Hides all elements at the start of an experiment run.
        """
        [x.resize(0,0) for x in self.elements]

    def updateFrame(self, i, filename):
        """
        Updates frame with current experiment run.
        """
        iterLabel = QLabel("Running trial {} of {}...".format(i, self.numTrials.value()), self)
        iterLabel.resize(iterLabel.sizeHint())
        iterLabel.move(100, 100)
        fileLabel = QLabel("Results saved to {}".format(filename), self)
        fileLabel.resize(fileLabel.sizeHint())
        fileLabel.move(100, 130)
        QApplication.processEvents()

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

    def startExperiment(self):
        """
        Starts game. Creates two players with values from inputs using the Player Factory class.
        Then creates game and sends it options and players. Finally closes itself.
        """
        playerOne = self.playerFactory.makePlayer(self.playerOneDropdown.currentText(), 1, self.p1Col)
        playerTwo = self.playerFactory.makePlayer(self.playerTwoDropdown.currentText(), 2, self.p2Col)
        players = [playerOne, playerTwo]
        width = self.widthInput.value()
        height = self.heightInput.value()
        # Create a file at the results location
        resultsFilename = "Results\\{}_{}_{}x{}.txt".format(playerOne, playerTwo, width, height)
        if not os.path.exists("Results"):
            os.makedirs("Results")
        f = open(resultsFilename,"w+")
        f.close()
        #self.hideAllElements()
        for i in range(self.numTrials.value()):
            self.updateFrame(i, resultsFilename)
            self.gf = GameGUI.GameFrame(width, height, players, resultsFilename)
        #self.close()


def main(trials=100,height=3,width=3):
    app = QApplication(sys.argv)
    ex = ExperimentFrame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

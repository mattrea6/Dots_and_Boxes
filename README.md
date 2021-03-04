This is an implementation of the game Dots and Boxes.
This is my Final Year Project implementation.

To play the game, use the command '>python DotsAndBoxes'

This launches a very simple & basic GUI that allows you to pick the board size you want, and allows you to play the game by clicking on the line you want to draw.

To run unit tests, use command '>python -m unittest -b'
Using the -b flag is recommended because of the large amount of text output.

'GameHandler.py' will launch an ASCII representation of the game. This version is very confusing to play, due to the way in which moves must be input.

'Moves' are made as a 3-tuple of ints. The way that lines are indexed and accessed is described in 'index.png'.
This file also describes the way boxes are indexed, although this is not visible to the player.

When playing the game via command line, enter 'r' to play a random legal move.

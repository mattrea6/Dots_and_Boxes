import sys
from PyQt5.QtWidgets import QApplication
import GameGUI
import Experiment

def main():
    if len(sys.argv) > 1:
        app = QApplication(sys.argv)
        ex = Experiment.ExperimentFrame()
        sys.exit(app.exec_())
    else:
        app = QApplication(sys.argv)
        ex = GameGUI.StartFrame()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()

import sys
from PyQt5.QtWidgets import QApplication
import GameGUI

def main():
    app = QApplication(sys.argv)
    ex = GameGUI.StartFrame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

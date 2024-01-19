import sys
from PyQt5.QtWidgets import QApplication
from src.ui.MainWindow import MainWindow

def main():
    # test_keyword()
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window.
    window = MainWindow()
    window.show()

    # Start the event loop.
    app.exec()

if __name__=="__main__":
    main()

import sys
from PyQt6.QtWidgets import QApplication, QLabel

from view.main_window_view import MainWindowWiew




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindowWiew()
    mainWindow.resize(1000, 800)
    mainWindow.show()
    app.exec()

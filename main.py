import sys
from PyQt6.QtWidgets import QApplication, QLabel

from services.db_service import DbService

from view.main_window_view import MainWindowView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindowView()
    mainWindow.showFullScreen()
    app.exec()

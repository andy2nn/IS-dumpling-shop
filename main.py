import sys
from PyQt6.QtWidgets import QApplication, QLabel

from services.admin_db_service import AdminDbService

from view.main_window_view import MainWindowView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindowView()
    mainWindow.showFullScreen()
    app.exec()

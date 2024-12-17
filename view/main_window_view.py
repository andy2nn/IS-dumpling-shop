import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt

from view.admin_window_view import AdminWindow

class MainWindowView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Система для крутых пельменей')
        layout = QVBoxLayout()


        ### Символ приложения пельмень( вкусный очень ) ###


        # Кнопка начала смены кассира
        mainButton = QPushButton('Открыть смену кассира')
        mainButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Изменено на Fixed для высоты
        mainButton.setMinimumWidth(300)  # Минимальная ширина
        mainButton.setMaximumWidth(500)  
        mainButton.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border: none; 
                padding: 10px; 
                border-radius: 5px; 
            }
            QPushButton:hover {
                background-color: #45a049; 
            }
            """
        )

        # Кнопка открытия меню администратора
        adminButton = QPushButton('Открыть меню администратора')
        adminButton.clicked.connect(self.navigateToAdminWindow)
        adminButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Изменено на Fixed для высоты
        adminButton.setMinimumWidth(300)  # Минимальная ширина
        adminButton.setMaximumWidth(500)  # Максимальная ширина
        adminButton.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border: none; 
                padding: 10px; 
                border-radius: 5px; \
            }
            QPushButton:hover {
                background-color: #45a049; 
            }
            """
        )


        # Кнопка выхода из приложения
        exitButton = QPushButton('Выход из приложения')
        exitButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        exitButton.setMinimumWidth(300)  # Минимальная ширина
        exitButton.setMaximumWidth(500)  # Максимальная ширина
        exitButton.clicked.connect(self.close)
        exitButton.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border: none; 
                padding: 10px; 
                border-radius: 5px; \
            }
            QPushButton:hover {
                background-color: #45a049; 
            }
            """
        )

        # Размещение на экране
        layout.addWidget(mainButton)
        layout.addWidget(adminButton)
        layout.addWidget(exitButton)

        # Устанавливаем выравнивание для всего layout
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Устанавливаем layout для виджета
        self.setLayout(layout)
    
    def navigateToAdminWindow(self):
        self.window = AdminWindow()
        self.window.showFullScreen()
        self.close()
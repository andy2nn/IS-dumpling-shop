import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QSpacerItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from view.admin_window_view import AdminWindow
from view.cashier_window import CashierWindow

class MainWindowView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Система для крутых пельменей')
        layout = QVBoxLayout()

        ### Символ приложения пельмень( вкусный очень ) ###
        self.imageLabel = QLabel(self)
        self.pixmap = QPixmap('assets/app_logo.png')  # Укажите путь к вашему изображению
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(self.imageLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.update_image()

        # Кнопка начала смены кассира
        mainButton = QPushButton('Открыть смену кассира')
        mainButton.clicked.connect(self.navigateToCashierWindow)
        mainButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mainButton.setMinimumWidth(300)
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
        adminButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        adminButton.setMinimumWidth(300)
        adminButton.setMaximumWidth(500)
        adminButton.setStyleSheet(
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

        # Кнопка выхода из приложения
        exitButton = QPushButton('Выход из приложения')
        exitButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        exitButton.setMinimumWidth(300)
        exitButton.setMaximumWidth(500)
        exitButton.clicked.connect(self.close)
        exitButton.setStyleSheet(
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

        # Добавляем спейсер для выравнивания по центру
        # layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Размещение на экране
        layout.addWidget(mainButton, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(adminButton, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(exitButton, alignment=Qt.AlignmentFlag.AlignCenter)
        # Добавляем спейсер для выравнивания по центру
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Устанавливаем выравнивание для всего layout
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Устанавливаем layout для виджета
        self.setLayout(layout)
    
    def navigateToCashierWindow(self):
        self.window = CashierWindow()
        self.window.showFullScreen()
        self.close()

    def navigateToAdminWindow(self):
        self.window = AdminWindow()
        self.window.showFullScreen()
        self.close()
    
    def resizeEvent(self, event):
        # Обновляем изображение при изменении размера окна
        self.update_image()
        super().resizeEvent(event)

    def update_image(self):
        # Получаем текущие размеры виджета
        width = int(self.width() / 2)  # Convert to int
        height = int(self.height() / 2)
        
        # Сжимаем изображение до размеров виджета
        scaled_pixmap = self.pixmap.scaled(width, height, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        
        # Устанавливаем сжатое изображение в QLabel
        self.imageLabel.setPixmap(scaled_pixmap)
import sys
from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt 
from PyQt6.QtGui import QFont  # Импортируем QFont для изменения шрифта

class CloseSmena(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Закрытие смены')
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Выравнивание по центру
        
        self.purchases_label = QLabel('Число покупок: 0')
        self.revenue_label = QLabel('Выручка: 0.00')
        
        # Установка шрифта
        font = QFont()
        font.setPointSize(16)  # Увеличиваем размер шрифта
        self.purchases_label.setFont(font)
        self.revenue_label.setFont(font)
        
        self.purchases_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.revenue_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.purchases_label)
        layout.addWidget(self.revenue_label)
        
        close_button = QPushButton('Закрыть смену')
        close_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        close_button.setFont(font)  # Установка шрифта для кнопки
        close_button.setMinimumWidth(300)
        close_button.setMaximumWidth(500)
        close_button.clicked.connect(self.close)
        self.setup_button(close_button)
        
        layout.addWidget(close_button)
        
        self.setLayout(layout)

    def update_summary(self, purchases, revenue):
        self.purchases_label.setText(f'Число покупок: {purchases}')
        self.revenue_label.setText(f'Выручка: {revenue:.2f}')

    def setup_button(self, button):
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.setMinimumWidth(300)
        button.setMaximumWidth(500)
        button.setStyleSheet(
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
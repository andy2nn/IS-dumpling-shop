import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt 
from view.add_pruduct_window_view import AddProductWindow
from view.add_promocode_window_view import AddPromocodeWindow
from view.show_products_window_view import ShowProductsWindow


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Меню админа')
        layout = QVBoxLayout()

        # Кнопка добавления товара
        addProductButton = QPushButton('Добавить товар')
        addProductButton.clicked.connect(self.navigateToAddProductWindow)
        self.setup_button(addProductButton)

        # Кнопка добавления промокода
        addPromocodeButton = QPushButton('Добавить промокод')
        addPromocodeButton.clicked.connect(self.navigateToAddPromocodeWindow)
        self.setup_button(addPromocodeButton)

        # Добавляем кнопки добавления товара и промокода в основной layout
        layout.addWidget(addProductButton)
        layout.addWidget(addPromocodeButton)

        # Создаем горизонтальный layout для кнопок показа ассортимента и промокодов, а также кнопки выхода
        bottomLayout = QVBoxLayout()

        # Кнопка открытия ассортимента
        showAssortmentButton = QPushButton('Показать ассортимент')
        showAssortmentButton.clicked.connect(self.navigateToShowProducts)
        self.setup_button(showAssortmentButton)

        # Кнопка показа промокодов
        showPromocodsButton = QPushButton('Показать промокоды')
        self.setup_button(showPromocodsButton)

        # Кнопка выхода из приложения
        exitButton = QPushButton('Выход из приложения')
        exitButton.clicked.connect(self.close)
        self.setup_button(exitButton)

        # Добавляем кнопки в горизонтальный layout
        bottomLayout.addWidget(showAssortmentButton)
        bottomLayout.addWidget(showPromocodsButton)
        bottomLayout.addWidget(exitButton)

        # Добавляем горизонтальный layout в основной layout
        layout.addLayout(bottomLayout)

        # Устанавливаем выравнивание для всего layout
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Устанавливаем layout для виджета
        self.setLayout(layout)

    def navigateToShowProducts(self):
        self.window = ShowProductsWindow()
        self.window.showFullScreen()
        self.close()

    def navigateToAddPromocodeWindow(self):
        self.window = AddPromocodeWindow()
        self.window.showFullScreen()
        self.close()

    def navigateToAddProductWindow(self):
        self.window = AddProductWindow()
        self.window.showFullScreen()
        self.close()

        

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
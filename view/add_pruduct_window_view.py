from services.admin_db_service import AdminDbService
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QLineEdit, QComboBox, QMessageBox
from PyQt6.QtCore import Qt


class AddProductWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавление товара')
        layout = QVBoxLayout()
       
        self.dbService = AdminDbService()

        # Поле ввода названия товара
        self.productName_label = QLabel('Название товара')
        self.productName_input = QLineEdit()
        self.set_input_properties(self.productName_input)
        layout.addWidget(self.productName_label)
        layout.addWidget(self.productName_input)

        # Поле ввода Описания товара
        self.productDescription_label = QLabel('Описание товара')
        self.productDescription_input = QLineEdit()
        self.set_input_properties(self.productDescription_input)
        layout.addWidget(self.productDescription_label)
        layout.addWidget(self.productDescription_input)

        # Поле выбора категории товара
        self.category_label = QLabel('Выберите категорию')
        self.category_combo = QComboBox()
        self.category_id_map = {}  # Словарь для хранения соответствий id и названий категорий
        categories = self.dbService.get_categories()  # Загружаем категории из базы данных
        for category in categories:
            category_id, category_name = category  # Предполагаем, что get_categories возвращает список кортежей (id, name)
            self.category_combo.addItem(category_name)
            self.category_id_map[category_name] = category_id  # Сохраняем соответствие

        layout.addWidget(self.category_label)
        layout.addWidget(self.category_combo)

        # Поле ввода где храниться изображение
        self.productImagePath_label = QLabel('Путь к изображению')
        self.productImagePath_input = QLineEdit()
        self.set_input_properties(self.productImagePath_input)
        layout.addWidget(self.productImagePath_label)
        layout.addWidget(self.productImagePath_input)

        # Поле ввода Цены
        self.productPrice_label = QLabel('Цена (в рублях)')
        self.productPrice_input = QLineEdit()
        self.set_input_properties(self.productPrice_input)
        layout.addWidget(self.productPrice_label)
        layout.addWidget(self.productPrice_input)

        # Кнопка сохранения в бд
        saveButton = QPushButton('Сохранить в базу данных')
        saveButton.clicked.connect(self.addProduct)
        self.setup_button(saveButton)
        layout.addWidget(saveButton)

        # Кнопка возврата
        exitButton = QPushButton('Назад')
        exitButton.clicked.connect(self.backButton)
        self.setup_button(exitButton)
        layout.addWidget(exitButton)

        # Устанавливаем выравнивание для всего layout
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Устанавливаем layout для виджета
        self.setLayout(layout)

    def addProduct(self):
        # извлечение данных с ui
        product_name = self.productName_input.text()
        product_description = self.productDescription_input.text()
        product_category_name = self.category_combo.currentText()
        product_image_path = self.productImagePath_input.text()
        product_price = self.productPrice_input.text()
        
        if len(product_name) == 0 or len(product_price) == 0:
            self.show_error_message('Пожалуйста, заполните все поля')
        else:
            try:
                price = int(product_price)  # Преобразуем строку в число
            except ValueError:
                self.show_error_message('Цена должна быть числом')
                return
            
            # Получаем id категории по её названию
            product_category_id = self.category_id_map.get(product_category_name)

            data = {
                'Название': product_name,
                'Описание': product_description,
                'id_категории': product_category_id,  # Используем id категории
                'Изображение': product_image_path,
                'Цена': price,
            }
            if self.dbService.add_to_database(table='продукты', data=data) == True:
                self.backButton()
            
            
        
    

    def backButton(self):
        from view.admin_window_view import AdminWindow
        self.window = AdminWindow()
        self.window.showFullScreen()
        self.close()

    def set_input_properties(self, input_field):
        input_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        input_field.setMinimumWidth(300)
        input_field.setMaximumWidth(500)

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
    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText("Ошибка")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
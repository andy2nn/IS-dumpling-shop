from services.admin_db_service import AdminDbService
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QLineEdit, QComboBox, QMessageBox
from PyQt6.QtCore import Qt


class AddPromocodeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавление промокода')
        layout = QVBoxLayout()
       
        self.dbService = AdminDbService()

        # Поле ввода промокода
        self.promocode_labal = QLabel('Промокод')
        self.promocode_input = QLineEdit()
        self.set_input_properties(self.promocode_input)
        layout.addWidget(self.promocode_labal)
        layout.addWidget(self.promocode_input)


        # Поле ввода скидки
        self.discount_labal = QLabel('Cкидка в %')
        self.discount_input = QLineEdit()
        self.set_input_properties(self.discount_input)
        layout.addWidget(self.discount_labal)
        layout.addWidget(self.discount_input)

        # Кнопка сохранения в бд
        saveButton = QPushButton('Сохранить в базу данных')
        saveButton.clicked.connect(self.addPromocode)
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

    def addPromocode(self):
        # извлечение данных с ui
        promocode = self.promocode_input.text()
        discount = self.discount_input.text()
        
        if len(promocode) == 0 or len(discount) == 0:
            self.show_error_message('Пожалуйста, заполните все поля')
        else:
            try:
                price = int(discount)  # Преобразуем строку в число
            except ValueError:
                self.show_error_message('Скидка должна быть числом')
                return

            data = {
                'Промокод': promocode,
                'Скидка': discount
            }
            if self.dbService.add_to_database(table='промокоды', data=data) == True:
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
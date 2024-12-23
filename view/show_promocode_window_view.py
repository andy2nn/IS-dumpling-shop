from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel, QHBoxLayout, QComboBox
from PyQt6.QtGui import QPixmap
from services.admin_db_service import AdminDbService


class ShowPromocodeWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Промокоды")
        self.dbService = AdminDbService()

        # Создаем таблицу
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Промокод", "Скидка", "Действия"])

        # Устанавливаем политику размера для таблицы
        self.table_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Загружаем данные из базы данных
        self.promocods = self.dbService.load_data_promocods()

        # Заполняем таблицу данными
        self.populate_table()

        # Устанавливаем макет
        layout = QVBoxLayout()
        
        # Создаем горизонтальный макет для таблицы
        h_layout = QHBoxLayout()
        
        # Добавляем спейсер слева
        left_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        h_layout.addItem(left_spacer)

        # Устанавливаем ширину и высоту таблицы на 2/3
        self.table_widget.setFixedWidth(self.width() * 2 // 3)
        self.table_widget.setFixedHeight(self.height() * 2 // 3)
        
        h_layout.addWidget(self.table_widget)

        # Добавляем спейсер справа
        right_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        h_layout.addItem(right_spacer)


        layout.addLayout(h_layout)
        # Кнопка выхода
        exit_button = QPushButton("Выход")
        exit_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        exit_button.setFixedSize(100, 40)
        exit_button.clicked.connect(self.navigateToAdminWindow)

        # Создаем горизонтальный макет для кнопки выхода
        exit_button_layout = QHBoxLayout()
        exit_button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))  # Левый спейсер
        exit_button_layout.addWidget(exit_button)  # Кнопка выхода
        exit_button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))  # Правый спейсер

        # Добавляем горизонтальный макет с кнопкой выхода в основной макет
        layout.addLayout(exit_button_layout)

        self.setLayout(layout)

        # Устанавливаем адаптивные ограничения по ширине столбцов
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    def resizeEvent(self, event):
        # Устанавливаем размеры таблицы при изменении размера окна
        self.table_widget.setFixedWidth(self.width() * 4 // 5)
        self.table_widget.setFixedHeight(self.height() * 4 // 5)
        super().resizeEvent(event)

    def populate_table(self):
        self.table_widget.setRowCount(len(self.promocods))  # Устанавливаем количество строк

        for row_index, promocode in enumerate(self.promocods):
            self.table_widget.setRowHeight(row_index, 60)
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(promocode['Промокод']))

            self.table_widget.setItem(row_index, 1, QTableWidgetItem(str(promocode['Скидка'])))

            # Создаем горизонтальный макет для кнопок
            button_layout = QHBoxLayout()

            # Добавляем кнопку редактирования
            edit_button = QPushButton("Сохранить")
            edit_button.clicked.connect(lambda checked, p=promocode: self.save_changes(p, row_index))
            button_layout.addWidget(edit_button)

            # Добавляем кнопку удаления
            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(lambda checked, p=promocode: self.delete_product(p))
            button_layout.addWidget(delete_button)

            # Устанавливаем макет кнопок в ячейку таблицы
            widget = QtWidgets.QWidget()
            widget.setLayout(button_layout)
            self.table_widget.setCellWidget(row_index, 2, widget)
    
    def delete_product(self, promocode):
        try:
            self.dbService.delete_promocode(promocode['Промокод'])
            self.promocods = self.dbService.load_data_promocods()
            self.populate_table()
        except Exception as e:
            print(f"Ошибка при обновлении базы данных: {e}")
            return
        



    def navigateToAdminWindow(self):
        from view.admin_window_view import AdminWindow
        self.window = AdminWindow()
        self.window.showFullScreen()
        self.close()

      
    def save_changes(self, promocode, row):
        # Получаем новые значения из ячеек таблицы

        new_promocode = self.table_widget.item(row, 0).text()
        new_discount = self.table_widget.item(row, 1).text()

        try: 
            new_discount = int(new_discount)
        except ValueError:
            print("Скидка должна быть числом (%)")
        
        try:
            self.dbService.update_promocode(promocode['Промокод'], new_promocode, new_discount)
            self.promocods = self.dbService.load_data_promocods()
            self.populate_table()
        except Exception as e:
            print(f"Ошибка при обновлении базы данных: {e}")
            return

        
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap
from services.db_service import DbService


class ShowProductsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Товары")
        self.dbServices = DbService()

        # Создаем таблицу
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Изображение", "Название", "Цена", "Описание", "Действия"])

        # Устанавливаем политику размера для таблицы
        self.table_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Загружаем данные из базы данных
        self.products = self.dbServices.load_data_products()

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
        self.table_widget.setRowCount(len(self.products))  # Устанавливаем количество строк

        for row_index, product in enumerate(self.products):
            self.table_widget.setRowHeight(row_index, 60)
            # Добавляем изображение
            # image_label = QLabel()
            # pixmap = QPixmap(product['Изображение'])
            # image_label.setPixmap(pixmap.scaled(50, 50, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            # self.table_widget.setCellWidget(row_index, 0, image_label)
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(product['Изображение']))

            # Добавляем название
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(product['Название']))

            # Добавляем цену
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(str(product['Цена'])))

            # Добавляем описание
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(product['Описание']))

            # Создаем горизонтальный макет для кнопок
            button_layout = QHBoxLayout()

            # Добавляем кнопку редактирования
            edit_button = QPushButton("Сохранить")
            edit_button.clicked.connect(lambda checked, p=product: self.save_changes(p, row_index))
            button_layout.addWidget(edit_button)

            # Добавляем кнопку удаления
            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(lambda checked, p=product: self.delete_product(p))
            button_layout.addWidget(delete_button)

            # Устанавливаем макет кнопок в ячейку таблицы
            widget = QtWidgets.QWidget()
            widget.setLayout(button_layout)
            self.table_widget.setCellWidget(row_index, 4, widget)
    
    def delete_product(self, product):
        try:
            self.dbServices.delete_product(product['id_продукта'])
            self.products = self.dbServices.load_data_products()
            self.populate_table()
        except Exception as e:
            print(f"Ошибка при обновлении базы данных: {e}")
            return
        



    def navigateToAdminWindow(self):
        from view.admin_window_view import AdminWindow
        self.window = AdminWindow()
        self.window.showFullScreen()
        self.close()

      
    def save_changes(self, product, row):
        # Получаем новые значения из ячеек таблицы
        new_name = self.table_widget.item(row, 1).text()
        new_price = self.table_widget.item(row, 2).text()
        new_description = self.table_widget.item(row, 3).text()
        new_image = self.table_widget.item(row, 0).text()

        try:
            new_price = int(new_price)  # Преобразуем цену в float
        except ValueError:
            print("Ошибка: Цена должна быть числом.")
            return


        
        try:
            self.dbServices.update_product(product['id_продукта'], new_name, new_price, new_description, new_image)
            self.products = self.dbServices.load_data_products()
            self.populate_table()
        except Exception as e:
            print(f"Ошибка при обновлении базы данных: {e}")
            return

        
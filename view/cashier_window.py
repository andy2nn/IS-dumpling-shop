import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, 
    QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from services.cashier_db_service import CashierDbService



class CashierWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.dbService = CashierDbService()
        self.load_items()
        # self.init_db()

    def init_ui(self):
        self.setWindowTitle("Магазин")

        # Основной layout
        main_layout = QVBoxLayout()

        # Ассортимент магазина
        main_layout.addWidget(QLabel("Весь ассортимент магазина"))
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(6)
        self.items_table.setHorizontalHeaderLabels(["ID", "Название", "Цена", "Описание", "Изображение", "Категория"])
        self.items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        main_layout.addWidget(self.items_table)

        # Установка адаптивной ширины столбцов
        header = self.items_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Устанавливаем режим растяжения для всех столбцов

        # Кнопка для добавления товара
        self.add_item_button = QPushButton("Добавить выбранный товар")
        self.add_item_button.clicked.connect(self.add_selected_item)
        main_layout.addWidget(self.add_item_button)

        # Выбранные товары
        main_layout.addWidget(QLabel("Выбранные товары"))
        self.selected_items_table = QTableWidget()
        self.selected_items_table.setColumnCount(3)
        self.selected_items_table.setHorizontalHeaderLabels(["ID", "Название", "Цена"])
        self.selected_items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        main_layout.addWidget(self.selected_items_table)

         # Установка адаптивной ширины столбцов для выбранных товаров
        selected_header = self.selected_items_table.horizontalHeader()
        selected_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Кнопка для удаления товара
        self.remove_item_button = QPushButton("Удалить выбранный товар")
        self.remove_item_button.clicked.connect(self.remove_selected_item)
        main_layout.addWidget(self.remove_item_button)

        # Общая стоимость
        self.total_cost_label = QLabel("Общая стоимость: 0 руб.")
        main_layout.addWidget(self.total_cost_label)

        # Промокод
        promo_layout = QHBoxLayout()
        self.promo_input = QLineEdit()
        self.promo_input.setPlaceholderText("Введите промокод")
        self.apply_promo_button = QPushButton("Применить промокод")
        self.apply_promo_button.clicked.connect(self.apply_promo)
        promo_layout.addWidget(self.promo_input)
        promo_layout.addWidget(self.apply_promo_button)
        main_layout.addLayout(promo_layout)

        # Управление
        control_layout = QHBoxLayout()
        self.buy_button = QPushButton("Произвести покупку")
        self.buy_button.clicked.connect(self.make_purchase)
        self.close_button = QPushButton("Закрыть смену")
        self.close_button.clicked.connect(self.close_shift)
        control_layout.addWidget(self.buy_button)
        control_layout.addWidget(self.close_button)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)

        # Общая стоимость
        self.total_cost = 0
    
    def load_items(self):
        try:
            items = self.dbService.load_data_products()
            self.items_table.setRowCount(len(items))
            category_id_map = {}  # Словарь для хранения соответствий id и названий категорий
            categories = self.dbService.get_categories()  # Загружаем категории из базы данных
            for category in categories:
                category_id, category_name = category  # Предполагаем, что get_categories возвращает список кортежей (id, name)
                category_id_map[category_id] = category_name


            for row, item in enumerate(items):
                self.items_table.setItem(row, 0, QTableWidgetItem(str(item['id_продукта'])))
                self.items_table.setItem(row, 1, QTableWidgetItem(item['Название']))
                self.items_table.setItem(row, 2, QTableWidgetItem(str(item['Цена'])))
                self.items_table.setItem(row, 3, QTableWidgetItem(str(item['Описание'])))
                self.items_table.setItem(row, 4, QTableWidgetItem(str(item['Изображение'])))
                self.items_table.setItem(row, 5, QTableWidgetItem(category_id_map[item['id_категории']]))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось загрузить товары: {e}")


    def add_selected_item(self):
        selected_row = self.items_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Добавление товара", "Выберите товар из ассортимента.")
            return

        item_id = self.items_table.item(selected_row, 0).text()
        item_name = self.items_table.item(selected_row, 1).text()
        item_price = float(self.items_table.item(selected_row, 2).text())

        # Добавляем товар в таблицу выбранных товаров
        row_count = self.selected_items_table.rowCount()
        self.selected_items_table.insertRow(row_count)
        self.selected_items_table.setItem(row_count, 0, QTableWidgetItem(item_id))
        self.selected_items_table.setItem(row_count, 1, QTableWidgetItem(item_name))
        self.selected_items_table.setItem(row_count, 2, QTableWidgetItem(str(item_price)))

        # Обновляем общую стоимость
        self.total_cost += item_price
        self.update_total_cost_label()

    def remove_selected_item(self):
        selected_row = self.selected_items_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Удаление товара", "Выберите товар для удаления.")
            return

        item_price = float(self.selected_items_table.item(selected_row, 2).text())

        # Удаляем товар из таблицы выбранных товаров
        self.selected_items_table.removeRow(selected_row)

        # Обновляем общую стоимость
        self.total_cost -= item_price
        self.update_total_cost_label()

    def update_total_cost_label(self):
        self.total_cost_label.setText(f"Общая стоимость: {self.total_cost} руб.")

    def apply_promo(self):
        promo_code = self.promo_input.text().strip()
        if promo_code:
            QMessageBox.information(self, "Промокод", f"Промокод {promo_code} применен!")
        else:
            QMessageBox.warning(self, "Промокод", "Введите корректный промокод.")

    def make_purchase(self):
        row_count = self.selected_items_table.rowCount()
        if row_count == 0:
            QMessageBox.warning(self, "Покупка", "Выберите товары для покупки.")
            return

        items = []
        for row in range(row_count):
            item_name = self.selected_items_table.item(row, 1).text()
            items.append(item_name)

        items_text = ", ".join(items)
        QMessageBox.information(self, "Покупка", f"Вы купили: {items_text}")
        self.selected_items_table.setRowCount(0)
        self.total_cost = 0
        self.update_total_cost_label()

    def close_shift(self):
        QMessageBox.information(self, "Смена", "Смена закрыта!")
        self.close()
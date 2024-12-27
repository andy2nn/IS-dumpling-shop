import mysql.connector
from mysql.connector import Error
from PyQt6.QtWidgets import QMessageBox

class CashierDbService():
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                # host='127.0.0.1',
                host = '26.132.244.42',
                user='cashier',
                password='Cashiershop1',
                database='dumpling_shop_db'
            )
            if self.connection.is_connected():
                print("Успешно подключено к базе данных")
        except Error as e:
            print(f"Ошибка при подключении к MySQL: {e}")


    def load_data_products(self):
        products = []
        cursor = None
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute("SELECT Изображение, Название, Цена, Описание, id_категории, id_продукта FROM продукты")
                rows = cursor.fetchall()
                for row in rows:
                    products.append({
                        'id_категории': row[4],
                        'id_продукта': row[5],
                        'Изображение': row[0],
                        'Название': row[1],
                        'Цена': row[2],
                        'Описание': row[3]
                    })
        except Error as e:
            print(f"Ошибка при работе с MySQL: {e}")
        finally:
            if cursor:
                cursor.close()
        return products

    def get_categories(self):
        categories = []
        cursor = None  
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute("SELECT id_категории, Тип FROM категория") 
                rows = cursor.fetchall()
                for row in rows:
                    categories.append((row[0], row[1]))
        except Error as e:
            print(f"Ошибка при работе с MySQL: {e}")
        finally:
            if cursor:
                cursor.close()
        return categories
    
    def get_promo(self, promocode):
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute("SELECT Скидка FROM промокоды WHERE Промокод = %s", (promocode,))
                row = cursor.fetchone()
                if row:
                    return row[0]
                else:
                    return None
        except Error as e:
            print(f"Ошибка при работе с MySQL: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    

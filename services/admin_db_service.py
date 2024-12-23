import mysql.connector
from mysql.connector import Error


class AdminDbService():
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                # host='127.0.0.1',
                host = '26.132.244.42',
                user='admin_dumpling_shop',
                password='Adminshop1',
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
    

    def load_data_promocods(self):
        promocods = []
        cursor = None
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute("SELECT Промокод, Скидка FROM промокоды")
                rows = cursor.fetchall()
                for row in rows:
                    promocods.append({
                        'Промокод': row[0],
                        'Скидка': row[1],
                    })
        except Error as e:
            print(f"Ошибка при работе с MySQL: {e}")
        finally:
            if cursor:
                cursor.close()
        return promocods



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

    def add_to_database(self, table, data):
        cursor = None
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()

                columns = ', '.join(data.keys())
                placeholders = ', '.join(['%s'] * len(data))
                sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                values = tuple(data.values())

                cursor.execute(sql, values)
                self.connection.commit()
                return True
                

        except Error as e:
            print(f"Ошибка при работе с MySQL: {e}")
            return False

        finally:
            if cursor:
                cursor.close()


    def update_product(self, product_id, new_name, new_price, new_description, new_image, new_category):
        cursor = None
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()

                # SQL-запрос на обновление
                sql_update_query = """
                UPDATE продукты
                SET Название = %s, Цена = %s, Описание = %s, Изображение = %s, id_категории = %s
                WHERE id_продукта = %s
                """
                
                # Выполнение запроса
                cursor.execute(sql_update_query, (new_name, new_price, new_description, new_image, new_category,product_id))
                
                # Подтверждение изменений
                self.connection.commit()

                print(f"Обновлено записей: {cursor.rowcount}")

        except Error as error:
            print(f"Ошибка при обновлении записи: {error}")
        finally:
            if cursor:
                cursor.close()


    def update_promocode(self, promocode, new_promocode, new_discount):
        cursor = None
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()

                # SQL-запрос на обновление
                sql_update_query = """
                UPDATE промокоды
                SET Промокод = %s, Скидка = %s
                WHERE Промокод = %s
                """
                
                # Выполнение запроса
                cursor.execute(sql_update_query, (new_promocode, new_discount, promocode))
                
                # Подтверждение изменений
                self.connection.commit()

                print(f"Обновлено записей: {cursor.rowcount}")

        except Error as error:
            print(f"Ошибка при обновлении записи: {error}")
        finally:
            if cursor:
                cursor.close()

    def delete_product(self, product_id):
        cursor = None
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()

                # SQL-запрос на удаление
                sql_delete_query = """
                DELETE FROM продукты
                WHERE id_продукта = %s
                """
                
                # Выполнение запроса
                cursor.execute(sql_delete_query, (product_id,))
                
                # Подтверждение изменений
                self.connection.commit()

                print(f"Удалено записей: {cursor.rowcount}")

        except Error as error:
            print(f"Ошибка при удалении записи: {error}")
        finally:
            if cursor:
                cursor.close()
    

    def delete_promocode(self, promocode):
        cursor = None
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()

                # SQL-запрос на удаление
                sql_delete_query = """
                DELETE FROM промокоды
                WHERE Промокод = %s
                """
                
                # Выполнение запроса
                cursor.execute(sql_delete_query, (promocode,))
                
                # Подтверждение изменений
                self.connection.commit()

                print(f"Удалено записей: {cursor.rowcount}")

        except Error as error:
            print(f"Ошибка при удалении записи: {error}")
        finally:
            if cursor:
                cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Соединение с MySQL закрыто.")


# Пример использования класса
if __name__ == "__main__":
    db_service = AdminDbService()
    
    # Пример данных для обновления
    update_data = {
        'price': 249.99,
        'description': 'Обновленное описание продукта'
    }
    
    # Условие для обновления
    condition = "product_number = 1001"  # Замените на нужное условие
    
    # Обновление записи в таблице products
    db_service.update_database('products', update_data, condition)

    db_service.close_connection()

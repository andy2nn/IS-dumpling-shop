import mysql.connector
from mysql.connector import Error


class DbService():
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

    # def update_database(self, table, data, condition):
    #     cursor = None
    #     try:
    #         if self.connection.is_connected():
    #             cursor = self.connection.cursor()

    #             set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
    #             sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
    #             values = tuple(data.values())
    #             print(f"SQL запрос: {sql} с значениями: {values}")

    #             cursor.execute(sql, values)
    #             self.connection.commit()
    #             print(f"Обновлено записей: {cursor.rowcount}")

    #             if cursor.rowcount == 0:
    #                 print("Предупреждение: ни одна запись не была обновлена. Проверьте условие.")

    #     except Error as e:
    #         print(f"Ошибка при работе с MySQL: {e}")

    #     finally:
    #         if cursor:
    #             cursor.close()

    def update_product(self, product_id, new_name, new_price, new_description, new_image):
        cursor = None
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()

                # SQL-запрос на обновление
                sql_update_query = """
                UPDATE продукты
                SET Название = %s, Цена = %s, Описание = %s, Изображение = %s
                WHERE id_продукта = %s
                """
                
                # Выполнение запроса
                cursor.execute(sql_update_query, (new_name, new_price, new_description, new_image, product_id))
                
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
    # def delete_from_database(self, table, condition):
    #     try:
    #         if self.connection.is_connected():
    #             cursor = self.connection.cursor()

    #             # Создание строки запроса
    #             sql = f"DELETE FROM {table} WHERE {condition}"

    #             # Выполнение запроса
    #             cursor.execute(sql)
    #             self.connection.commit()
    #             print(f"Удалено записей: {cursor.rowcount}")

    #     except Error as e:
    #         print(f"Ошибка при работе с MySQL: {e}")

    #     finally:
    #         if cursor:
    #             cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Соединение с MySQL закрыто.")


# Пример использования класса
if __name__ == "__main__":
    db_service = DbService()
    
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

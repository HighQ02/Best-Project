import sqlite3

def delete_record():
    try:
        sqlite_connection = sqlite3.connect('db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        # sql_delete_query = """DELETE from django_migrations where id = 48"""
        # cursor.execute(sql_delete_query)
        # sqlite_connection.commit()
        sql_delete_query = """DROP TABLE e_shop_conversationmessage"""
        cursor.execute(sql_delete_query)
        sqlite_connection.commit()
        print("Запись успешно удалена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

delete_record()
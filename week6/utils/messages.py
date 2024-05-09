import mysql.connector

from utils.mysql import connection_mysql, close_mysql


def get_messages():
    connection, cursor = connection_mysql()

    try:
        query = "SELECT member.username, message.content,  message.time FROM message INNER JOIN member ON message.member_id = member.id ORDER BY message.time DESC"
        cursor.execute(query)
        messages = cursor.fetchall()
        return messages
    except mysql.connector.Error as err:
        print(f"資料庫連線錯誤: {err}")
    finally:
        close_mysql(cursor, connection)

    return []


def add_messages(username, message):
    connection, cursor = connection_mysql()

    try:
        find_id_query = "SELECT id FROM member WHERE username = %s"
        find_id_value = (username,)
        cursor.execute(find_id_query, find_id_value)
        user = cursor.fetchone()

        query = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
        values = (user[0], message)
        cursor.execute(query, values)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"資料庫連線錯誤: {err}")
    finally:
        close_mysql(cursor, connection)

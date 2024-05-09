import mysql.connector

from utils.mysql import get_db_connection, execute_query


def get_messages():

    try:
        connection = get_db_connection()
        query = "SELECT member.username, message.content,  message.time FROM message INNER JOIN member ON message.member_id = member.id ORDER BY message.time DESC"
        messages = execute_query(
            connection, query, values=None, fetch_method="fetchall"
        )
        return messages
    except mysql.connector.Error as err:
        print(f"資料庫連線錯誤: {err}")

    return []


def add_messages(user_id, message):
    try:
        connection = get_db_connection()
        query = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
        values = (user_id, message)
        execute_query(connection, query, values)

    except mysql.connector.Error as err:
        print(f"資料庫連線錯誤: {err}")

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
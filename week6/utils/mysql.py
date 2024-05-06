import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return connection

def connection_mysql():
    connection = get_db_connection()
    cursor = connection.cursor()
    print("建立連線")
    return connection, cursor

def close_mysql(cursor, connection):
    cursor.close()
    connection.close()
    print("關閉連線")


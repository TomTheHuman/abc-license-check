import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import sys
import os
load_dotenv()

HOST = os.environ.get("HOST")
USERNAME = os.environ.get("USER")
PASS = os.environ.get("PASS")
DB = os.environ.get("DB")

def get_db():
    try:
        print(HOST, ", ", USERNAME, ", ", PASS, ", ", DB)
        connection = mysql.connector.connect(host=HOST, database=DB, user=USERNAME, password=PASS, auth_plugin='mysql_native_password')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MYSQL Server Version: ", db_Info, file=sys.stdout)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Your connection to database: ", record, file=sys.stdout)
        return connection

    except Error as e:
        print("Error while connecting to MySQL: ", e)
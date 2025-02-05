import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def db_connect():
    try:
        connect = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb3',
            collation='utf8mb3_general_ci'
        )
        if connect.is_connected():
            print("Connection successful to database")
            return connect
    except Error as e:
        print(f"Could not establish connection to database. Error: {e}")
        return None

def query_airports(query):
    connect = db_connect()
    if connect:
        try:
            cursor = connect.cursor(dictionary=True)
            search_param = f"%{query}%"
            search_prefix = f"{query}%"
            sql_query = """
                SELECT airport, city, country, IATA, ICAO
                FROM airports
                WHERE IATA LIKE %s OR airport LIKE %s OR city LIKE %s
                ORDER BY 
                    CASE WHEN IATA LIKE %s THEN 0 ELSE 1 END,
                    CASE WHEN airport LIKE %s THEN 0 ELSE 1 END,
                    CASE WHEN city LIKE %s THEN 0 ELSE 1 END,
                    airport
                LIMIT 10;
            """
            search_param = f"%{query}%"
            cursor.execute(sql_query, (search_param, search_param, search_param,
                                       search_prefix, search_prefix, search_prefix))
            results = cursor.fetchall()
            return results
        
        except Exception as e:
            print(f"Database Error: {e}")
            return []
        
        finally:
            cursor.close()
            connect.close()
            
    return []

def query_airlines(query):
    connect = db_connect()
    if connect:
        try:
            cursor = connect.cursor(dictionary=True)
            search_param = f"%{query}%"
            search_prefix = f"{query}%"
            sql_query = """
                SELECT airline, IATA, ICAO
                FROM airlines
                WHERE IATA LIKE %s OR airline LIKE %s
                ORDER BY 
                    CASE WHEN IATA LIKE %s THEN 0 ELSE 1 END,
                    CASE WHEN airline LIKE %s THEN 0 ELSE 1 END,
                    airline
                LIMIT 10;
            """

            search_param = f"%{query}%"
            cursor.execute(sql_query, (search_param, search_param,
                                       search_prefix, search_prefix))
            results = cursor.fetchall()
            return results

        except Exception as e:
            print(f"Database Error: {e}")
            return []

        finally:
            cursor.close()
            connect.close()

    return [] 


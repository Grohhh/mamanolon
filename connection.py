import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="equipment1_db",
            user="postgres",
            password="12345"
        )
        return conn
    except Exception as e:
        print("Ошибка подключения к базе данных:", e)
        return None


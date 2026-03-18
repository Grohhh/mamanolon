from database.connection import get_connection
from PyQt5.QtWidgets import QApplication
import sys
class Responsible:
    
    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, last_name, first_name, middle_name, position, phone, email, department
                FROM responsible_persons ORDER BY last_name
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения ответственных: {e}")
            return []
    
    def add(last_name, first_name, middle_name=None, position=None, phone=None, email=None, department=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO responsible_persons 
                (last_name, first_name, middle_name, position, phone, email, department)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (last_name, first_name, middle_name, position, phone, email, department))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления ответственного: {e}")
            return False
    
    def update(resp_id, last_name, first_name, middle_name=None, position=None, phone=None, email=None, department=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE responsible_persons 
                SET last_name=%s, first_name=%s, middle_name=%s, position=%s, phone=%s, email=%s, department=%s
                WHERE id=%s
            """, (last_name, first_name, middle_name, position, phone, email, department, resp_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка обновления ответственного: {e}")
            return False
    
    def delete(resp_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM responsible_persons WHERE id = %s", (resp_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка удаления ответственного: {e}")
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Responsible()
    window.show()
    sys.exit(app.exec_())

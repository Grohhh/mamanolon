from PyQt5.QtWidgets import QApplication
import sys
from database.connection import get_connection

class Audience:
    
    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, number, floor, building, area, seats FROM audiences ORDER BY number")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения аудиторий: {e}")
            return []
    
    def add(number, floor=None, building=None, area=None, seats=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO audiences (number, floor, building, area, seats) VALUES (%s, %s, %s, %s, %s)""", (number, floor, building, area, seats))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления аудитории: {e}")
            return False
    
    def update(audience_id, number, floor=None, building=None, area=None, seats=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""UPDATE audiences SET number=%s, floor=%s, building=%s, area=%s, seats=%s WHERE id=%s""", (number, floor, building, area, seats, audience_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка обновления аудитории: {e}")
            return False
    
    def delete(audience_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM audiences WHERE id = %s", (audience_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка удаления аудитории: {e}")
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Audience()
    window.show()
    sys.exit(app.exec_())

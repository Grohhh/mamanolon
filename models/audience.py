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
            cursor.execute("""
                SELECT 
                    a.audience_id, a.number, a.floor, a.building, a.area, a.capacity,
                    COALESCE(rp.last_name || ' ' || rp.first_name, '-')
                FROM audiences a
                LEFT JOIN responsible_persons rp ON a.responsible_person_id = rp.responsible_person_id
                ORDER BY a.number
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения аудиторий: {e}")
            return []

    def add(number, floor=None, building=None, area=None, capacity=None, responsible_person_id=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO audiences (number, floor, building, area, capacity, responsible_person_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (number, floor, building, area, capacity, responsible_person_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления аудитории: {e}")
            return False

    def update(audience_id, number, floor=None, building=None, area=None, capacity=None, responsible_person_id=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE audiences
                SET number=%s, floor=%s, building=%s, area=%s, capacity=%s, responsible_person_id=%s
                WHERE audience_id=%s
            """, (number, floor, building, area, capacity, responsible_person_id, audience_id))
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
            cursor.execute("DELETE FROM audiences WHERE audience_id = %s", (audience_id,))
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

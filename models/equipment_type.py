from database.connection import get_connection
from PyQt5.QtWidgets import QApplication
import sys


class EquipmentType:

    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT equipment_type_id, name, description, service_life FROM equipment_types ORDER BY name")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения типов: {e}")
            return []

    def add(name, description=None, service_life=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO equipment_types (name, description, service_life)
                VALUES (%s, %s, %s)
            """, (name, description, service_life))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления типа: {e}")
            return False

    def update(type_id, name, description=None, service_life=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE equipment_types
                SET name=%s, description=%s, service_life=%s
                WHERE equipment_type_id=%s
            """, (name, description, service_life, type_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка обновления типа: {e}")
            return False

    def delete(type_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM equipment_types WHERE equipment_type_id = %s", (type_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка удаления типа: {e}")
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquipmentType()
    window.show()
    sys.exit(app.exec_())

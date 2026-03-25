from database.connection import get_connection
from PyQt5.QtWidgets import QApplication
import sys


class EquipmentMovementHistory:

    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    emh.equipment_movement_history_id,
                    e.inventory_number,
                    e.name,
                    a.number,
                    a.building,
                    TO_CHAR(emh.moved_at, 'DD.MM.YYYY HH24:MI:SS')
                FROM equipment_movement_history emh
                JOIN equipment e ON emh.equipment_id = e.equipment_id
                LEFT JOIN audiences a ON emh.audience_id = a.audience_id
                ORDER BY emh.moved_at DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения истории перемещений: {e}")
            return []

    def get_by_equipment(equipment_id):
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    emh.equipment_movement_history_id,
                    e.inventory_number,
                    e.name,
                    a.number,
                    a.building,
                    TO_CHAR(emh.moved_at, 'DD.MM.YYYY HH24:MI:SS')
                FROM equipment_movement_history emh
                JOIN equipment e ON emh.equipment_id = e.equipment_id
                LEFT JOIN audiences a ON emh.audience_id = a.audience_id
                WHERE emh.equipment_id = %s
                ORDER BY emh.moved_at DESC
            """, (equipment_id,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения истории перемещений: {e}")
            return []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquipmentMovementHistory()
    window.show()
    sys.exit(app.exec_())

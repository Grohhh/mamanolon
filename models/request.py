from database.connection import get_connection
from PyQt5.QtWidgets import QApplication
import sys


class Request:

    STATUSES = ['открыта', 'в работе', 'закрыта', 'отменена']

    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.request_id, r.request_number, e.name,
                       r.created_at, r.description, r.work_type, r.status
                FROM requests r
                JOIN equipment e ON r.equipment_id = e.equipment_id
                ORDER BY r.request_id DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения заявок: {e}")
            return []

    def add(equipment_id, description, work_type='ремонт', priority=3, user_id=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO requests (request_number, equipment_id, description, work_type, priority, user_id)
                VALUES (
                    CONCAT('R', TO_CHAR(CURRENT_DATE, 'YYYYMMDD'), '-', LPAD(nextval('requests_request_id_seq')::TEXT, 4, '0')),
                    %s, %s, %s, %s, %s
                )
            """, (equipment_id, description, work_type, priority, user_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка создания заявки: {e}")
            return False

    def close_request(request_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE requests
                SET status = 'закрыта', updated_at = CURRENT_TIMESTAMP
                WHERE request_id = %s
            """, (request_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка закрытия заявки: {e}")
            return False

    def update_status(request_id, status):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE requests
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE request_id = %s
            """, (status, request_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка обновления статуса заявки: {e}")
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Request()
    window.show()
    sys.exit(app.exec_())

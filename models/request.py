from database.connection import get_connection
from PyQt5.QtWidgets import QApplication
import sys
class Request:
    
    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT rr.id, rr.request_number, e.name, rr.request_date,
                       rr.description, rr.work_type, rr.status
                FROM repair_requests rr
                JOIN equipment e ON rr.equipment_id = e.id
                ORDER BY rr.id DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения заявок: {e}")
            return []
    
    def add(equipment_id, description, work_type='ремонт', priority=3):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO repair_requests (request_number, equipment_id, description, work_type, priority)
                VALUES (
                    CONCAT('R', TO_CHAR(CURRENT_DATE, 'YYYYMMDD'), '-', LPAD(nextval('repair_requests_id_seq')::TEXT, 4, '0')),
                    %s, %s, %s, %s
                )
            """, (equipment_id, description, work_type, priority))
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
                UPDATE repair_requests SET status = 'закрыта', completion_date = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (request_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка закрытия заявки: {e}")
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Request()
    window.show()
    sys.exit(app.exec_())

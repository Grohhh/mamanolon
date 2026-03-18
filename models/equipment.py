from database.connection import get_connection
from PyQt5.QtWidgets import QApplication
import sys
class Equipment:
    
    STATUSES = ['исправен', 'в ремонте', 'списан', 'резерв']
    
    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT e.id, e.inventory_number, e.name, e.manufacturer, e.model,  et.name, a.number, rp.last_name || ' ' || rp.first_name, e.purchase_date, e.cost, e.status FROM equipment e LEFT JOIN equipment_types et ON e.type_id = et.id LEFT JOIN audiences a ON e.audience_id = a.id LEFT JOIN responsible_persons rp ON e.responsible_id = rp.id ORDER BY e.id DESC""")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения оборудования: {e}")
            return []
    
    def get_by_id(equipment_id):
        conn = get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT e.id, e.inventory_number, e.name, e.manufacturer, e.model, e.type_id, e.audience_id, e.responsible_id, e.purchase_date, e.cost, e.status, e.notes FROM equipment e WHERE e.id = %s""", (equipment_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            return row
        except Exception as e:
            print(f"Ошибка получения оборудования: {e}")
            return None
    
    def add(inventory_number, name, manufacturer=None, model=None, type_id=None, audience_id=None, responsible_id=None, purchase_date=None, cost=None, status='исправен'):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO equipment (inventory_number, name, manufacturer, model, type_id, audience_id, responsible_id, purchase_date, cost, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (inventory_number, name, manufacturer, model, type_id, audience_id, responsible_id, purchase_date, cost, status))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления оборудования: {e}")
            return False
    
    def update(equipment_id, inventory_number, name, manufacturer=None, model=None, type_id=None, audience_id=None, responsible_id=None, purchase_date=None, cost=None):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE equipment SET inventory_number=%s, name=%s, manufacturer=%s, model=%s, type_id=%s, audience_id=%s, responsible_id=%s, purchase_date=%s, cost=%s WHERE id=%s""", (inventory_number, name, manufacturer, model, type_id, audience_id, responsible_id, purchase_date, cost, equipment_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка обновления оборудования: {e}")
            return False
    
    def delete(equipment_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM equipment WHERE id = %s", (equipment_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка удаления оборудования: {e}")
            return False
    
    def change_status(equipment_id, new_status):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE equipment SET status = %s WHERE id = %s", (new_status, equipment_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка изменения статуса: {e}")
            return False
    
    def move(equipment_id, audience_id, responsible_id, reason, user_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE equipment SET audience_id=%s, responsible_id=%s WHERE id=%s""", (audience_id, responsible_id, equipment_id))
            cursor.execute("""INSERT INTO equipment_movements (equipment_id, to_audience_id, to_responsible_id, reason, user_id) VALUES (%s, %s, %s, %s, %s)""", (equipment_id, audience_id, responsible_id, reason, user_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка перемещения оборудования: {e}")
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Equipment()
    window.show()
    sys.exit(app.exec_())

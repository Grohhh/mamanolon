from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QComboBox,
                             QGridLayout, QGroupBox, QFileDialog, QApplication)
from gui.section_base import SectionBase
from database.connection import get_connection
import csv
import sys
class ReportsSection(SectionBase):
    
    def __init__(self):
        super().__init__("📊 Отчеты")
        self.init_content()
    
    def init_content(self):
        layout = QVBoxLayout()
        
        group = QGroupBox("Формирование отчетов")
        form_layout = QGridLayout()
        
        form_layout.addWidget(QLabel("Тип отчета:"), 0, 0)
        self.report_type = QComboBox()
        self.report_type.addItems(["Инвентаризационная ведомость по аудитории", "Оборудование в ремонте", "Оборудование по ответственному лицу", "Все оборудование"])
        self.report_type.currentIndexChanged.connect(self.update_params)
        form_layout.addWidget(self.report_type, 0, 1)
        
        form_layout.addWidget(QLabel("Аудитория:"), 1, 0)
        self.audience_combo = QComboBox()
        self.audience_combo.addItem("Все аудитории", None)
        self.load_audiences()
        form_layout.addWidget(self.audience_combo, 1, 1)
        
        form_layout.addWidget(QLabel("Ответственное лицо:"), 2, 0)
        self.responsible_combo = QComboBox()
        self.responsible_combo.addItem("Все ответственные", None)
        self.load_responsible()
        form_layout.addWidget(self.responsible_combo, 2, 1)
        
        btn_layout = QHBoxLayout()
        
        btn_generate = QPushButton("Сформировать")
        btn_generate.clicked.connect(self.generate_report)
        btn_layout.addWidget(btn_generate)
        
        btn_export = QPushButton("Экспорт в CSV")
        btn_export.clicked.connect(self.export_to_csv)
        btn_layout.addWidget(btn_export)
        
        form_layout.addLayout(btn_layout, 3, 0, 1, 2)
        group.setLayout(form_layout)
        layout.addWidget(group)
        
        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)
        
        self.update_params()
        self.get_content_layout().addLayout(layout)
    
    def update_params(self):
        index = self.report_type.currentIndex()
        self.audience_combo.setVisible(index == 0)
        self.responsible_combo.setVisible(index == 2)
    
    def load_audiences(self):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT audience_id, number FROM audiences ORDER BY number")
            for row in cursor.fetchall():
                self.audience_combo.addItem(row[1], row[0])
            cursor.close()
            conn.close()

    def load_responsible(self):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT responsible_person_id, last_name || ' ' || first_name FROM responsible_persons ORDER BY last_name""")
            for row in cursor.fetchall():
                self.responsible_combo.addItem(row[1], row[0])
            cursor.close()
            conn.close()
    
    def generate_report(self):
        report_index = self.report_type.currentIndex()
        audience_id = self.audience_combo.currentData()
        responsible_id = self.responsible_combo.currentData()

        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "Ошибка", "Нет подключения к БД")
            return

        try:
            cursor = conn.cursor()

            if report_index == 0:
                if audience_id:
                    cursor.execute("""
                        SELECT e.inventory_number, e.name, e.manufacturer, e.model,
                               et.name, a.number, COALESCE(rp.last_name || ' ' || rp.first_name, '-'),
                               e.status, e.cost
                        FROM equipment e
                        LEFT JOIN equipment_types et ON e.equipment_type_id = et.equipment_type_id
                        LEFT JOIN audiences a ON e.audience_id = a.audience_id
                        LEFT JOIN responsible_persons rp ON a.responsible_person_id = rp.responsible_person_id
                        WHERE e.audience_id = %s
                        ORDER BY e.inventory_number""", (audience_id,))
                    headers = ['Инв.номер', 'Название', 'Производитель', 'Модель', 'Тип', 'Аудитория', 'Ответственный', 'Статус', 'Стоимость']
                else:
                    cursor.execute("""
                        SELECT a.number, e.inventory_number, e.name, e.manufacturer,
                               et.name, COALESCE(rp.last_name || ' ' || rp.first_name, '-'),
                               e.status, e.cost
                        FROM equipment e
                        LEFT JOIN equipment_types et ON e.equipment_type_id = et.equipment_type_id
                        LEFT JOIN audiences a ON e.audience_id = a.audience_id
                        LEFT JOIN responsible_persons rp ON a.responsible_person_id = rp.responsible_person_id
                        ORDER BY a.number, e.inventory_number""")
                    headers = ['Аудитория', 'Инв.номер', 'Название', 'Производитель', 'Тип', 'Ответственный', 'Статус', 'Стоимость']

            elif report_index == 1:
                cursor.execute("""
                    SELECT e.inventory_number, e.name, r.request_number,
                           r.created_at, r.status, r.work_type
                    FROM equipment e
                    JOIN requests r ON e.equipment_id = r.equipment_id
                    WHERE r.status IN ('открыта', 'в работе')
                    ORDER BY r.created_at DESC""")
                headers = ['Инв.номер', 'Название', 'Заявка', 'Дата', 'Статус', 'Тип работ']

            elif report_index == 2:
                # Отчёт по оборудованию, закреплённому за материально-ответственным лицом
                if responsible_id:
                    cursor.execute("""
                        SELECT e.inventory_number, e.name, e.manufacturer, e.model,
                               a.number, e.status
                        FROM equipment e
                        JOIN audiences a ON e.audience_id = a.audience_id
                        WHERE a.responsible_person_id = %s
                        ORDER BY e.inventory_number""", (responsible_id,))
                    headers = ['Инв.номер', 'Название', 'Производитель', 'Модель', 'Аудитория', 'Статус']
                else:
                    cursor.execute("""
                        SELECT rp.last_name || ' ' || rp.first_name,
                               e.inventory_number, e.name, a.number, e.status
                        FROM responsible_persons rp
                        LEFT JOIN audiences a ON rp.responsible_person_id = a.responsible_person_id
                        LEFT JOIN equipment e ON a.audience_id = e.audience_id
                        ORDER BY rp.last_name, e.inventory_number""")
                    headers = ['Ответственный', 'Инв.номер', 'Название', 'Аудитория', 'Статус']

            else:
                cursor.execute("""
                    SELECT e.inventory_number, e.name, e.manufacturer, e.model,
                           et.name, a.number, COALESCE(rp.last_name || ' ' || rp.first_name, '-'),
                           e.status
                    FROM equipment e
                    LEFT JOIN equipment_types et ON e.equipment_type_id = et.equipment_type_id
                    LEFT JOIN audiences a ON e.audience_id = a.audience_id
                    LEFT JOIN responsible_persons rp ON a.responsible_person_id = rp.responsible_person_id
                    ORDER BY e.inventory_number""")
                headers = ['Инв.номер', 'Название', 'Производитель', 'Модель', 'Тип', 'Аудитория', 'Ответственный', 'Статус']

            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            self.result_table.setColumnCount(len(headers))
            self.result_table.setHorizontalHeaderLabels(headers)
            self.result_table.setRowCount(len(rows))

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.result_table.setItem(row_idx, col_idx,
                                            QTableWidgetItem(str(value) if value else ""))

            QMessageBox.information(self, "Успех", f"Отчет сформирован ({len(rows)} записей)")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def export_to_csv(self):
        if self.result_table.rowCount() == 0:
            QMessageBox.warning(self, "Ошибка", "Сначала сформируйте отчет")
            return
        
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "CSV файлы (*.csv)")
        if not filename:
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                
                headers = [self.result_table.horizontalHeaderItem(i).text() 
                          for i in range(self.result_table.columnCount())]
                writer.writerow(headers)
                
                for row in range(self.result_table.rowCount()):
                    row_data = [self.result_table.item(row, col).text() 
                               for col in range(self.result_table.columnCount())]
                    writer.writerow(row_data)
            
            QMessageBox.information(self, "Успех", f"Отчет сохранен в {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportsSection()
    window.show()
    sys.exit(app.exec_())

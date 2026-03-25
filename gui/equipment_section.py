from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox, QApplication)
from PyQt5.QtCore import Qt
from gui.section_base import SectionBase
from models.equipment import Equipment
from models.audience import Audience
from models.responsible import Responsible
from models.equipment_type import EquipmentType
from database.connection import get_connection
import re
import sys
class EquipmentSection(SectionBase):
    
    def __init__(self, current_user=None):
        super().__init__("🖥️ Оборудование")
        self.current_user = current_user
        self.selected_id = None
        self.init_content()
        self.load_data()
    
    def init_content(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(['ID', 'Инв.номер', 'Название', 'Производитель', 'Модель', 'Тип', 'Аудитория', 'Ответственный', 'Дата ввода', 'Стоимость', 'Статус'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)
        
        form_layout = QHBoxLayout()
        
        form_layout.addWidget(QLabel("Инв.номер:"))
        self.inv_number = QLineEdit()
        form_layout.addWidget(self.inv_number)
        
        form_layout.addWidget(QLabel("Название:"))
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_input)
        
        form_layout.addWidget(QLabel("Производитель:"))
        self.manufacturer = QLineEdit()
        form_layout.addWidget(self.manufacturer)
        
        form_layout.addWidget(QLabel("Модель:"))
        self.model_input = QLineEdit()
        form_layout.addWidget(self.model_input)
        
        layout.addLayout(form_layout)
        
        form_layout2 = QHBoxLayout()

        form_layout2.addWidget(QLabel("Тип:"))
        self.type_combo = QComboBox()
        self.type_combo.addItem("Не выбран", None)
        self.load_types()
        form_layout2.addWidget(self.type_combo)

        form_layout2.addWidget(QLabel("Аудитория:"))
        self.audience_combo = QComboBox()
        self.audience_combo.addItem("Не назначена", None)
        self.load_audiences()
        self.audience_combo.currentIndexChanged.connect(self.on_audience_changed)
        form_layout2.addWidget(self.audience_combo)

        form_layout2.addWidget(QLabel("Ответственный:"))
        self.resp_combo = QComboBox()
        self.resp_combo.addItem("Не назначен", None)
        self.load_responsible()
        form_layout2.addWidget(self.resp_combo)

        layout.addLayout(form_layout2)
        
        form_layout3 = QHBoxLayout()
        
        form_layout3.addWidget(QLabel("Дата ввода (ГГГГ-ММ-ДД):"))
        self.purchase_date = QLineEdit()
        self.purchase_date.setPlaceholderText("2024-01-15")
        form_layout3.addWidget(self.purchase_date)
        
        form_layout3.addWidget(QLabel("Стоимость:"))
        self.cost = QLineEdit()
        self.cost.setPlaceholderText("0")
        form_layout3.addWidget(self.cost)
        
        form_layout3.addWidget(QLabel("Статус:"))
        self.status_combo = QComboBox()
        for status in Equipment.STATUSES:
            self.status_combo.addItem(status.capitalize(), status)
        form_layout3.addWidget(self.status_combo)
        
        layout.addLayout(form_layout3)
        
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_record)
        btn_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("Изменить")
        self.update_btn.clicked.connect(self.edit_record)
        btn_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_record)
        btn_layout.addWidget(self.delete_btn)
        
        self.move_btn = QPushButton("Переместить")
        self.move_btn.clicked.connect(self.move_equipment)
        btn_layout.addWidget(self.move_btn)
        
        self.status_btn = QPushButton("Изменить статус")
        self.status_btn.clicked.connect(self.change_status_dialog)
        btn_layout.addWidget(self.status_btn)
        
        self.writeoff_btn = QPushButton("Списать")
        self.writeoff_btn.clicked.connect(self.writeoff_record)
        btn_layout.addWidget(self.writeoff_btn)
        
        layout.addLayout(btn_layout)
        self.get_content_layout().addLayout(layout)
    
    def load_types(self):
        self.type_combo.clear()
        self.type_combo.addItem("Не выбран", None)
        for t in EquipmentType.get_all():
            self.type_combo.addItem(t[1], t[0])
    
    def load_audiences(self):
        self.audience_combo.clear()
        self.audience_combo.addItem("Не назначена", None)
        for a in Audience.get_all():
            self.audience_combo.addItem(f"{a[1]} (эт.{a[2]})", a[0])

    def load_responsible(self):
        self.resp_combo.clear()
        self.resp_combo.addItem("Не назначен", None)
        for r in Responsible.get_all():
            self.resp_combo.addItem(f"{r[1]} {r[2]}", r[0])

    def on_audience_changed(self, index):
        audience_id = self.audience_combo.currentData()
        if audience_id:
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT rp.responsible_person_id, rp.last_name || ' ' || rp.first_name
                    FROM audiences a
                    JOIN responsible_persons rp ON a.responsible_person_id = rp.responsible_person_id
                    WHERE a.audience_id = %s
                """, (audience_id,))
                row = cursor.fetchone()
                cursor.close()
                conn.close()
                if row:
                    index = self.resp_combo.findData(row[0])
                    self.resp_combo.setCurrentIndex(index if index >= 0 else 0)
                    return
        self.resp_combo.setCurrentIndex(0)

    def load_data(self):
        data = Equipment.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                val_str = str(value) if value is not None else ""
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(val_str))
    
    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
        self.inv_number.setText(self.table.item(row, 1).text() or "")
        self.name_input.setText(self.table.item(row, 2).text() or "")
        self.manufacturer.setText(self.table.item(row, 3).text() or "")
        self.model_input.setText(self.table.item(row, 4).text() or "")

        type_name = self.table.item(row, 5).text() if self.table.item(row, 5) else ""
        index = self.type_combo.findText(type_name)
        self.type_combo.setCurrentIndex(index if index >= 0 else 0)

        aud_name = self.table.item(row, 6).text() if self.table.item(row, 6) else ""
        index = self.audience_combo.findText(aud_name.split()[0] if aud_name else "", Qt.MatchStartsWith)
        self.audience_combo.setCurrentIndex(index if index >= 0 else 0)

        resp_name = self.table.item(row, 7).text() if self.table.item(row, 7) else ""
        index = self.resp_combo.findText(resp_name.split()[0] if resp_name else "", Qt.MatchStartsWith)
        self.resp_combo.setCurrentIndex(index if index >= 0 else 0)

        date_text = self.table.item(row, 8).text() if self.table.item(row, 8) else ""
        self.purchase_date.setText(date_text or "")

        cost_text = self.table.item(row, 9).text() if self.table.item(row, 9) else ""
        self.cost.setText(cost_text or "")

        status_name = self.table.item(row, 10).text() if self.table.item(row, 10) else ""
        index = self.status_combo.findText(status_name)
        self.status_combo.setCurrentIndex(index if index >= 0 else 0)
    
    def add_record(self):
        if not self.inv_number.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите инвентарный номер")
            return
        
        date_str = self.purchase_date.text().strip()
        if date_str:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                QMessageBox.warning(self, "Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
                return
        
        cost_str = self.cost.text().strip()
        cost = 0.0
        if cost_str:
            try:
                cost = float(cost_str.replace('₽', '').replace(' ', '').strip())
            except:
                QMessageBox.warning(self, "Ошибка", "Неверный формат стоимости")
                return
        
        success = Equipment.add(
            self.inv_number.text(), self.name_input.text(), self.manufacturer.text(),
            self.model_input.text(), self.type_combo.currentData(),
            self.audience_combo.currentData(),
            date_str if date_str else None, cost,
            self.status_combo.currentData()
        )
        
        if success:
            QMessageBox.information(self, "Успех", "Оборудование добавлено")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить оборудование")
    
    def edit_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите оборудование")
            return
        
        date_str = self.purchase_date.text().strip()
        if date_str:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                QMessageBox.warning(self, "Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
                return
        
        cost_str = self.cost.text().strip()
        cost = 0.0
        if cost_str:
            try:
                cost = float(cost_str.replace('₽', '').replace(' ', '').strip())
            except:
                QMessageBox.warning(self, "Ошибка", "Неверный формат стоимости")
                return
        
        success = Equipment.update(
            self.selected_id, self.inv_number.text(), self.name_input.text(),
            self.manufacturer.text(), self.model_input.text(), self.type_combo.currentData(),
            self.audience_combo.currentData(),
            date_str if date_str else None, cost
        )
        
        if success:
            QMessageBox.information(self, "Успех", "Оборудование обновлено")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить оборудование")
    
    def delete_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите оборудование")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", "Удалить оборудование?\nЭто действие нельзя отменить!",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        if Equipment.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Оборудование удалено")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить оборудование")
    
    def move_equipment(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите оборудование")
            return

        if self.audience_combo.currentData() is None:
            QMessageBox.warning(self, "Ошибка", "Выберите аудиторию")
            return

        if Equipment.move(self.selected_id, self.audience_combo.currentData(),
                         "Перемещение", self.current_user['id']):
            QMessageBox.information(self, "Успех", "Оборудование перемещено")
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось переместить оборудование")
    
    def change_status_dialog(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите оборудование")
            return
        
        if Equipment.change_status(self.selected_id, self.status_combo.currentData()):
            QMessageBox.information(self, "Успех", "Статус изменен")
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось изменить статус")
    
    def writeoff_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите оборудование")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", "Списать оборудование?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        if Equipment.change_status(self.selected_id, 'списан'):
            QMessageBox.information(self, "Успех", "Оборудование списано")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось списать оборудование")
    
    def clear_inputs(self):
        self.selected_id = None
        self.inv_number.clear()
        self.name_input.clear()
        self.manufacturer.clear()
        self.model_input.clear()
        self.type_combo.setCurrentIndex(0)
        self.audience_combo.setCurrentIndex(0)
        self.resp_combo.setCurrentIndex(0)
        self.purchase_date.clear()
        self.cost.clear()
        self.status_combo.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquipmentSection()
    window.show()
    sys.exit(app.exec_())

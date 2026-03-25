from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox, QApplication)
from PyQt5.QtCore import Qt
from gui.section_base import SectionBase
from models.audience import Audience
from models.responsible import Responsible
from database.connection import get_connection
import sys
class AudienceSection(SectionBase):
    
    def __init__(self):
        super().__init__("🏢 Аудитории")
        self.selected_id = None
        self.init_content()
        self.load_data()
    
    def init_content(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Номер', 'Этаж', 'Корпус', 'Площадь', 'Вместимость', 'Ответственный'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Номер:"))
        self.number_input = QLineEdit()
        form_layout.addWidget(self.number_input)

        form_layout.addWidget(QLabel("Этаж:"))
        self.floor_input = QLineEdit()
        form_layout.addWidget(self.floor_input)

        form_layout.addWidget(QLabel("Корпус:"))
        self.building_input = QLineEdit()
        form_layout.addWidget(self.building_input)

        form_layout.addWidget(QLabel("Площадь:"))
        self.area_input = QLineEdit()
        form_layout.addWidget(self.area_input)

        form_layout.addWidget(QLabel("Вместимость:"))
        self.capacity_input = QLineEdit()
        form_layout.addWidget(self.capacity_input)

        form_layout.addWidget(QLabel("Ответственный:"))
        self.resp_combo = QComboBox()
        self.resp_combo.addItem("Не назначен", None)
        self.load_responsible()
        form_layout.addWidget(self.resp_combo)

        layout.addLayout(form_layout)
        
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
        
        layout.addLayout(btn_layout)
        self.get_content_layout().addLayout(layout)
    
    def load_data(self):
        data = Audience.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ""))

    def load_responsible(self):
        self.resp_combo.clear()
        self.resp_combo.addItem("Не назначен", None)
        for r in Responsible.get_all():
            self.resp_combo.addItem(f"{r[1]} {r[2]}", r[0])

    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
        self.number_input.setText(self.table.item(row, 1).text() or "")
        self.floor_input.setText(self.table.item(row, 2).text() or "")
        self.building_input.setText(self.table.item(row, 3).text() or "")
        self.area_input.setText(self.table.item(row, 4).text() or "")
        self.capacity_input.setText(self.table.item(row, 5).text() or "")
        
        resp_name = self.table.item(row, 6).text() if self.table.item(row, 6) else ""
        index = self.resp_combo.findText(resp_name.split()[0] if resp_name else "", Qt.MatchStartsWith)
        self.resp_combo.setCurrentIndex(index if index >= 0 else 0)

    def add_record(self):
        number = self.number_input.text().strip()
        if not number:
            QMessageBox.warning(self, "Ошибка", "Введите номер аудитории")
            return

        if Audience.add(number, self.floor_input.text() or None, self.building_input.text() or None, self.area_input.text() or None, self.capacity_input.text() or None, self.resp_combo.currentData()):
            QMessageBox.information(self, "Успех", "Аудитория добавлена")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить аудиторию")

    def edit_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите аудиторию")
            return

        if Audience.update(self.selected_id, self.number_input.text(), self.floor_input.text() or None, self.building_input.text() or None, self.area_input.text() or None, self.capacity_input.text() or None, self.resp_combo.currentData()):
            QMessageBox.information(self, "Успех", "Данные обновлены")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить данные")
    
    def delete_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите аудиторию")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", "Удалить аудиторию?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        if Audience.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Аудитория удалена")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить аудиторию")
    
    def clear_inputs(self):
        self.number_input.clear()
        self.floor_input.clear()
        self.building_input.clear()
        self.area_input.clear()
        self.capacity_input.clear()
        self.resp_combo.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudienceSection()
    window.show()
    sys.exit(app.exec_())

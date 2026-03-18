from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QApplication)
from gui.section_base import SectionBase
from models.equipment_type import EquipmentType
import sys
class EquipmentTypeSection(SectionBase):
    
    def __init__(self):
        super().__init__("📋 Типы оборудования")
        self.selected_id = None
        self.init_content()
        self.load_data()
    
    def init_content(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Описание', 'Срок службы'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)
        
        form_layout = QHBoxLayout()
        
        form_layout.addWidget(QLabel("Название:"))
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_input)
        
        form_layout.addWidget(QLabel("Описание:"))
        self.desc_input = QLineEdit()
        form_layout.addWidget(self.desc_input)
        
        form_layout.addWidget(QLabel("Срок службы:"))
        self.service_life_input = QLineEdit()
        form_layout.addWidget(self.service_life_input)
        
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
        data = EquipmentType.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ""))
    
    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
        self.name_input.setText(self.table.item(row, 1).text() or "")
        self.desc_input.setText(self.table.item(row, 2).text() or "")
        self.service_life_input.setText(self.table.item(row, 3).text() or "")
    
    def add_record(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название типа")
            return
        
        if EquipmentType.add(name, self.desc_input.text() or None, self.service_life_input.text() or None):
            QMessageBox.information(self, "Успех", "Тип добавлен")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить тип")
    
    def edit_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите тип")
            return
        
        if EquipmentType.update(self.selected_id, self.name_input.text(), self.desc_input.text() or None, self.service_life_input.text() or None):
            QMessageBox.information(self, "Успех", "Тип обновлен")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить тип")
    
    def delete_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите тип")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", "Удалить тип?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        if EquipmentType.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Тип удален")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить тип")
    
    def clear_inputs(self):
        self.name_input.clear()
        self.desc_input.clear()
        self.service_life_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquipmentTypeSection()
    window.show()
    sys.exit(app.exec_())

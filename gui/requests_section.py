from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox, QTextEdit, QApplication)
from gui.section_base import SectionBase
from models.request import Request
from models.equipment import Equipment
import sys
class RequestsSection(SectionBase):
    
    def __init__(self):
        super().__init__("🔧 Заявки на ремонт")
        self.selected_id = None
        self.init_content()
        self.load_data()
    
    def init_content(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Номер', 'Оборудование', 'Дата', 'Описание', 'Тип работ', 'Статус'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)
        
        form_layout = QHBoxLayout()
        
        form_layout.addWidget(QLabel("Оборудование:"))
        self.equipment_combo = QComboBox()
        self.load_equipment()
        form_layout.addWidget(self.equipment_combo)
        
        form_layout.addWidget(QLabel("Тип работ:"))
        self.work_type = QComboBox()
        self.work_type.addItems(['ремонт', 'диагностика', 'обслуживание', 'замена комплектующих'])
        self.work_type.setEditable(True)
        form_layout.addWidget(self.work_type)
        
        form_layout.addWidget(QLabel("Приоритет:"))
        self.priority = QComboBox()
        self.priority.addItems(['3 - Средний', '1 - Высокий', '2 - Выше среднего', '4 - Ниже среднего', '5 - Низкий'])
        form_layout.addWidget(self.priority)
        
        layout.addLayout(form_layout)
        
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Описание:"))
        self.description = QTextEdit()
        self.description.setMaximumHeight(60)
        self.description.setPlaceholderText("Опишите проблему...")
        desc_layout.addWidget(self.description)
        layout.addLayout(desc_layout)
        
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Создать заявку")
        self.add_btn.clicked.connect(self.add_record)
        btn_layout.addWidget(self.add_btn)

        self.close_btn = QPushButton("Закрыть заявку")
        self.close_btn.clicked.connect(self.close_request)
        btn_layout.addWidget(self.close_btn)

        layout.addLayout(btn_layout)
        self.get_content_layout().addLayout(layout)
    
    def load_equipment(self):
        self.equipment_combo.clear()
        data = Equipment.get_all()
        for row in data:
            self.equipment_combo.addItem(f"{row[1]} - {row[2]}", row[0])
    
    def load_data(self):
        data = Request.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ""))
    
    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
    
    def add_record(self):
        equipment_id = self.equipment_combo.currentData()
        if not equipment_id:
            QMessageBox.warning(self, "Ошибка", "Выберите оборудование")
            return
        
        if not self.description.toPlainText().strip():
            QMessageBox.warning(self, "Ошибка", "Введите описание")
            return
        
        priority_text = self.priority.currentText()
        priority = int(priority_text.split(' - ')[0])
        
        if Request.add(equipment_id, self.description.toPlainText(),
                      self.work_type.currentText(), priority):
            QMessageBox.information(self, "Успех", "Заявка создана")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать заявку")
    
    def close_request(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите заявку")
            return
        
        if Request.close_request(self.selected_id):
            QMessageBox.information(self, "Успех", "Заявка закрыта")
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось закрыть заявку")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RequestsSection()
    window.show()
    sys.exit(app.exec_())

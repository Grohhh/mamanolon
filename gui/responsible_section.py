from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QApplication)
from gui.section_base import SectionBase
from models.responsible import Responsible
import sys
class ResponsibleSection(SectionBase):
    
    def __init__(self):
        super().__init__("👥 Ответственные лица")
        self.selected_id = None
        self.init_content()
        self.load_data()
    
    def init_content(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['ID', 'Фамилия', 'Имя', 'Отчество', 'Должность', 'Телефон', 'Email', 'Отдел'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)
        
        form_layout1 = QHBoxLayout()
        form_layout1.addWidget(QLabel("Фамилия:"))
        self.last_name = QLineEdit()
        form_layout1.addWidget(self.last_name)
        
        form_layout1.addWidget(QLabel("Имя:"))
        self.first_name = QLineEdit()
        form_layout1.addWidget(self.first_name)
        
        form_layout1.addWidget(QLabel("Отчество:"))
        self.middle_name = QLineEdit()
        form_layout1.addWidget(self.middle_name)
        
        layout.addLayout(form_layout1)
        
        form_layout2 = QHBoxLayout()
        form_layout2.addWidget(QLabel("Должность:"))
        self.position = QLineEdit()
        form_layout2.addWidget(self.position)
        
        form_layout2.addWidget(QLabel("Телефон:"))
        self.phone = QLineEdit()
        form_layout2.addWidget(self.phone)
        
        form_layout2.addWidget(QLabel("Email:"))
        self.email = QLineEdit()
        form_layout2.addWidget(self.email)
        
        form_layout2.addWidget(QLabel("Отдел:"))
        self.department = QLineEdit()
        form_layout2.addWidget(self.department)
        
        layout.addLayout(form_layout2)
        
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
        data = Responsible.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ""))
    
    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
        self.last_name.setText(self.table.item(row, 1).text() or "")
        self.first_name.setText(self.table.item(row, 2).text() or "")
        self.middle_name.setText(self.table.item(row, 3).text() or "")
        self.position.setText(self.table.item(row, 4).text() or "")
        self.phone.setText(self.table.item(row, 5).text() or "")
        self.email.setText(self.table.item(row, 6).text() or "")
        self.department.setText(self.table.item(row, 7).text() or "")
    
    def add_record(self):
        if not self.last_name.text().strip() or not self.first_name.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите фамилию и имя")
            return
        
        if Responsible.add(self.last_name.text(), self.first_name.text(), self.middle_name.text() or None, self.position.text() or None, self.phone.text() or None, self.email.text() or None, self.department.text() or None):
            QMessageBox.information(self, "Успех", "Ответственное лицо добавлено")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить лицо")
    
    def edit_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите лицо")
            return
        
        if Responsible.update(self.selected_id, self.last_name.text(), self.first_name.text(), self.middle_name.text() or None, self.position.text() or None, self.phone.text() or None, self.email.text() or None, self.department.text() or None):
            QMessageBox.information(self, "Успех", "Данные обновлены")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить данные")
    
    def delete_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите лицо")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", "Удалить ответственное лицо?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        if Responsible.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Лицо удалено")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить лицо")
    
    def clear_inputs(self):
        self.last_name.clear()
        self.first_name.clear()
        self.middle_name.clear()
        self.position.clear()
        self.phone.clear()
        self.email.clear()
        self.department.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResponsibleSection()
    window.show()
    sys.exit(app.exec_())

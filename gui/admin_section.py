from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox, QApplication)
from gui.section_base import SectionBase
from models.user import User
import sys
class AdminSection(SectionBase):
    
    def __init__(self):
        super().__init__("⚙️ Администрирование")
        self.selected_id = None
        self.init_content()
        self.load_data()
    
    def init_content(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Логин', 'Роль', 'ФИО', 'Активен'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)
        
        form_layout = QHBoxLayout()
        
        form_layout.addWidget(QLabel("Логин:"))
        self.username_input = QLineEdit()
        form_layout.addWidget(self.username_input)
        
        form_layout.addWidget(QLabel("Пароль:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_input)
        
        form_layout.addWidget(QLabel("Роль:"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(['admin', 'manager'])
        form_layout.addWidget(self.role_combo)
        
        form_layout.addWidget(QLabel("ФИО:"))
        self.fullname_input = QLineEdit()
        form_layout.addWidget(self.fullname_input)
        
        layout.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить пользователя")
        self.add_btn.clicked.connect(self.add_record)
        btn_layout.addWidget(self.add_btn)
        
        self.delete_btn = QPushButton("Деактивировать")
        self.delete_btn.clicked.connect(self.delete_record)
        btn_layout.addWidget(self.delete_btn)
        
        layout.addLayout(btn_layout)
        self.get_content_layout().addLayout(layout)
    
    def load_data(self):
        data = User.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                if col_idx == 4:
                    text = "Да" if value else "Нет"
                else:
                    text = str(value) if value else ""
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(text))
    
    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
    
    def add_record(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
        
        if User.add(username, password, self.role_combo.currentText(), 
                   self.fullname_input.text()):
            QMessageBox.information(self, "Успех", "Пользователь добавлен")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить пользователя\n(возможно, логин занят)")
    
    def delete_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", "Деактивировать пользователя?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        if User.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Пользователь деактивирован")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось деактивировать пользователя")
    
    def clear_inputs(self):
        self.username_input.clear()
        self.password_input.clear()
        self.fullname_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminSection()
    window.show()
    sys.exit(app.exec_())

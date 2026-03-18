from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QMessageBox, QFrame, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import sys
class MainMenu(QWidget):
    
    logout_signal = pyqtSignal()
    open_section_signal = pyqtSignal(str)
    
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"Главное меню - {self.current_user['full_name']}")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("Учет оборудования в аудиториях")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(title)
        
        user_info = QLabel(f"Пользователь: {self.current_user['full_name']} | Роль: {self.current_user['role']}")
        user_info.setAlignment(Qt.AlignCenter)
        user_info.setFont(QFont("Arial", 12))
        user_info.setStyleSheet("color: #666;")
        main_layout.addWidget(user_info)
        
        main_layout.addSpacing(20)
        
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)
        
        if self.current_user['role'] in ['admin', 'manager']:
            btn_types = self.create_menu_button("📋 Типы оборудования", "Справочник типов оборудования")
            btn_types.clicked.connect(lambda: self.open_section("types"))
            buttons_layout.addWidget(btn_types)
            
            btn_responsible = self.create_menu_button("👥 Ответственные лица", "Справочник ответственных лиц")
            btn_responsible.clicked.connect(lambda: self.open_section("responsible"))
            buttons_layout.addWidget(btn_responsible)
            
            btn_audience = self.create_menu_button("🏢 Аудитории", "Справочник аудиторий")
            btn_audience.clicked.connect(lambda: self.open_section("audience"))
            buttons_layout.addWidget(btn_audience)
            
            btn_equipment = self.create_menu_button("🖥️ Оборудование", "Учет и перемещение оборудования")
            btn_equipment.clicked.connect(lambda: self.open_section("equipment"))
            buttons_layout.addWidget(btn_equipment)
            
            btn_requests = self.create_menu_button("🔧 Заявки на ремонт", "Регистрация и отслеживание заявок")
            btn_requests.clicked.connect(lambda: self.open_section("requests"))
            buttons_layout.addWidget(btn_requests)
        
        btn_reports = self.create_menu_button("📊 Отчеты", "Формирование отчетов и ведомостей")
        btn_reports.clicked.connect(lambda: self.open_section("reports"))
        buttons_layout.addWidget(btn_reports)
        
        if self.current_user['role'] == 'admin':
            btn_admin = self.create_menu_button("⚙️ Администрирование", "Управление пользователями")
            btn_admin.clicked.connect(lambda: self.open_section("admin"))
            buttons_layout.addWidget(btn_admin)
        
        buttons_widget.setLayout(buttons_layout)
        main_layout.addWidget(buttons_widget)
        
        main_layout.addStretch()
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        btn_logout = QPushButton("🚪 Выйти из системы")
        btn_logout.clicked.connect(self.logout)
        main_layout.addWidget(btn_logout)
        
        self.setLayout(main_layout)
    
    def create_menu_button(self, text, tooltip):
        btn = QPushButton(text)
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.PointingHandCursor)
        return btn
    
    def open_section(self, section_name):
        self.open_section_signal.emit(section_name)
    
    def logout(self):
        reply = QMessageBox.question(self, "Выход", "Выйти из системы?", 
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.logout_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())

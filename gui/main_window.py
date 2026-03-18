from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QApplication
from PyQt5.QtCore import pyqtSignal

from gui.main_menu import MainMenu
from gui.audience_section import AudienceSection
from gui.equipment_section import EquipmentSection
from gui.equipment_type_section import EquipmentTypeSection
from gui.responsible_section import ResponsibleSection
from gui.requests_section import RequestsSection
from gui.reports_section import ReportsSection
from gui.admin_section import AdminSection
import sys
class AppWindow(QMainWindow):
    
    logout_signal = pyqtSignal()
    
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("Учет оборудования в аудиториях")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #fafafa;")
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.main_menu = MainMenu(self.current_user)
        self.main_menu.logout_signal.connect(self.logout)
        self.main_menu.open_section_signal.connect(self.open_section)
        self.stack.addWidget(self.main_menu)
        
        self.sections = {}
        
        self.show()
    
    def open_section(self, section_name):
        if section_name not in self.sections:
            if section_name == 'types':
                section = EquipmentTypeSection()
            elif section_name == 'responsible':
                section = ResponsibleSection()
            elif section_name == 'audience':
                section = AudienceSection()
            elif section_name == 'equipment':
                section = EquipmentSection(self.current_user)
            elif section_name == 'requests':
                section = RequestsSection()
            elif section_name == 'reports':
                section = ReportsSection()
            elif section_name == 'admin':
                section = AdminSection()
            else:
                return
            
            section.back_signal.connect(self.show_menu)
            self.sections[section_name] = section
            self.stack.addWidget(section)
        
        self.stack.setCurrentWidget(self.sections[section_name])
    
    def show_menu(self):
        self.stack.setCurrentWidget(self.main_menu)
    
    def logout(self):
        self.logout_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())

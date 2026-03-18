from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QApplication
from PyQt5.QtCore import pyqtSignal
import sys
class SectionBase(QWidget):
    
    back_signal = pyqtSignal()
    
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        header_layout = QHBoxLayout()
        
        self.btn_back = QPushButton("← Назад в меню")
        self.btn_back.clicked.connect(self.go_back)
        header_layout.addWidget(self.btn_back)
        
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
        
        self.setLayout(layout)
    
    def go_back(self):
        self.back_signal.emit()
    
    def get_content_layout(self):
        return self.content_layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SectionBase()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication
from gui.login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Учет оборудования в аудиториях")
    app.setApplicationVersion("1.0.0")
    
    window = LoginWindow()
    window.show()
    
    sys.exit(app.exec_())

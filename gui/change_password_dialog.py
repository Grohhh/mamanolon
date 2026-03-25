from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QApplication)
from PyQt5.QtCore import Qt
from models.user import User
import sys


class ChangePasswordDialog(QDialog):
    def __init__(self, parent=None, current_user=None):
        super().__init__(parent)
        self.current_user = current_user
        self.setWindowTitle("Смена пароля")
        self.setModal(True)
        self.setMinimumWidth(350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        info_label = QLabel(f"Пользователь: {self.current_user['full_name']}")
        info_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(info_label)

        layout.addSpacing(10)

        form = QFormLayout()
        form.setSpacing(10)

        self.old_password = QLineEdit()
        self.old_password.setEchoMode(QLineEdit.Password)
        self.old_password.setPlaceholderText("Введите текущий пароль")
        form.addRow("Текущий пароль:", self.old_password)

        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setPlaceholderText("Придумайте новый пароль")
        form.addRow("Новый пароль:", self.new_password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setPlaceholderText("Подтвердите новый пароль")
        form.addRow("Подтверждение:", self.confirm_password)

        layout.addLayout(form)

        layout.addSpacing(15)

        hint_label = QLabel("Пароль должен быть не менее 4 символов")
        hint_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(hint_label)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(8)

        self.save_btn = QPushButton("Сохранить новый пароль")
        self.save_btn.clicked.connect(self.change_password)
        button_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("❌ Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

    def change_password(self):
        old_password = self.old_password.text()
        new_password = self.new_password.text()
        confirm_password = self.confirm_password.text()

        if not old_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Ошибка",
                "Заполните все поля")
            return

        user = User.authenticate(self.current_user['username'], old_password)
        if not user:
            QMessageBox.critical(self, "Ошибка",
                "Неверный текущий пароль")
            self.old_password.clear()
            self.old_password.setFocus()
            return

        if new_password != confirm_password:
            QMessageBox.critical(self, "Ошибка",
                "Новые пароли не совпадают")
            self.new_password.clear()
            self.confirm_password.clear()
            self.new_password.setFocus()
            return

        if len(new_password) < 4:
            QMessageBox.warning(self, "Ошибка",
                "Пароль должен быть не менее 4 символов")
            self.new_password.clear()
            self.confirm_password.clear()
            self.new_password.setFocus()
            return

        if old_password == new_password:
            QMessageBox.warning(self, "Ошибка",
                "Новый пароль должен отличаться от текущего")
            self.new_password.clear()
            self.confirm_password.clear()
            self.new_password.setFocus()
            return

        if User.change_password(self.current_user['id'], new_password):
            QMessageBox.information(self, "Успех",
                "Пароль успешно изменён!\nТеперь используйте новый пароль для входа.")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка",
                "Не удалось изменить пароль.\nПопробуйте позже.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChangePasswordDialog()
    window.show()
    sys.exit(app.exec_())

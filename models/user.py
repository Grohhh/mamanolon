import hashlib
from database.connection import get_connection
from PyQt5.QtWidgets import QApplication
import sys


class User:

    def authenticate(username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, username, role, full_name
                FROM users
                WHERE username = %s AND password_hash = %s AND is_active = TRUE
            """, (username, password_hash))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'role': user[2],
                    'full_name': user[3]
                }
            return None
        except Exception as e:
            print(f"Ошибка аутентификации: {e}")
            return None

    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username, role, full_name, is_active FROM users ORDER BY user_id")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Ошибка получения пользователей: {e}")
            return []

    def username_exists(username):
        conn = get_connection()
        if not conn:
            return True
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            exists = cursor.fetchone() is not None
            cursor.close()
            conn.close()
            return exists
        except Exception as e:
            print(f"Ошибка проверки логина: {e}")
            return True

    def add(username, password, role, full_name=None):
        if User.username_exists(username):
            return False

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, full_name)
                VALUES (%s, %s, %s, %s)
            """, (username, password_hash, role, full_name))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления пользователя: {e}")
            return False

    def delete(user_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_active = FALSE WHERE user_id = %s", (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка удаления пользователя: {e}")
            return False

    def change_password(user_id, new_password):
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET password_hash = %s WHERE user_id = %s
            """, (password_hash, user_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка смены пароля: {e}")
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = User()
    window.show()
    sys.exit(app.exec_())

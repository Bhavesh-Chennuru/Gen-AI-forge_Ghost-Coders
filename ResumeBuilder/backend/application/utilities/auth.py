import sqlite3
import bcrypt

class Auth:
    def __init__(self, db_path="users.db", pepper=None):
        self.db_path = db_path
        self.pepper = pepper
        self._init_db_schema()

    def _get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db_schema(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash BLOB NOT NULL)"
        )
        conn.commit()
        conn.close()

    def _hash_password(self, password: str) -> bytes:
        if self.pepper:
            password += self.pepper
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def register_user(self, username, password):
        hashed_pw = self._hash_password(password)
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hashed_pw),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def login_user(self, username, password):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?", (username,)
        )
        result = cursor.fetchone()
        conn.close()

        if not result:
            return False

        if self.pepper:
            password += self.pepper

        return bcrypt.checkpw(password.encode(), result[0])


authenticator = Auth(db_path="users.db", pepper="my_secret_pepper_value_123")

import sqlite3
import datetime

class MessageDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('llmdb.db')
        self.cursor = self.connection.cursor()
        self.table_name = "messages"
        self.create_table()

    def create_table(self):
        try:
            table_check = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'"
            self.cursor.execute(table_check)
            if self.cursor.fetchone() is None:
                self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    created_at TEXT,
                                    role TEXT,
                                    username TEXT,
                                    content TEXT)''')
        except Exception as e:
            print(f"Error creating table: {e}")

    def add_message(self, role, username, content):
        try:
            self.cursor.execute(f"INSERT INTO {self.table_name} (created_at, role, username, content) VALUES (?, ?, ?, ?)",
                                (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), role, username, content))
            self.connection.commit()
        except sqlite3.OperationalError:
            self.create_table()
        finally:
            self.cursor.close()
            self.connection.close()

    def get_messages(self):
        try:
            self.cursor.execute(f"SELECT * FROM {self.table_name}")
            messages = self.cursor.fetchall()
            return messages
        except sqlite3.OperationalError:
            self.create_table()
        finally:
            self.cursor.close()
            self.connection.commit()

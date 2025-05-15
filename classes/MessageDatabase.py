import sqlite3
import datetime
from typing import List, Dict, Optional, Tuple
from contextlib import contextmanager

class MessageDatabase:
    def __init__(self, db_path: str = 'llmdb.db'):
        self.db_path = db_path
        self.table_name = "messages"
        self._ensure_table_exists()
        self._migrate_database()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def _ensure_table_exists(self) -> None:
        """Ensures the messages table exists in the database."""
        create_table_sql = f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                role TEXT NOT NULL,
                username TEXT,
                content TEXT NOT NULL
            )
        '''
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
    
    def _migrate_database(self) -> None:
        """Handles database migrations to add new columns if needed."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if metadata column exists
                cursor.execute(f"PRAGMA table_info({self.table_name})")
                columns = [column[1] for column in cursor.fetchall()]
                
                # Add metadata column if it doesn't exist
                if 'metadata' not in columns:
                    cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN metadata TEXT")
                    conn.commit()
                    print("Added metadata column to messages table")
        except Exception as e:
            print(f"Error during database migration: {e}")
    
    def add_message(self, role: str, content: str, username: Optional[str] = None, metadata: Optional[Dict] = None) -> bool:
        """
        Add a new message to the database.
        
        Args:
            role: The role of the message sender (user/assistant)
            content: The message content
            username: Optional username
            metadata: Optional metadata dictionary
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"INSERT INTO {self.table_name} (created_at, role, username, content, metadata) VALUES (?, ?, ?, ?, ?)",
                    (
                        datetime.datetime.now().isoformat(),
                        role,
                        username,
                        content,
                        str(metadata) if metadata else None
                    )
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding message: {e}")
            return False
    
    def get_messages(self, limit: Optional[int] = None, role: Optional[str] = None) -> List[Tuple]:
        """
        Retrieve messages from the database.
        
        Args:
            limit: Optional limit on number of messages to retrieve
            role: Optional filter by role
        
        Returns:
            List of message tuples
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                query = f"SELECT * FROM {self.table_name}"
                params = []
                
                if role:
                    query += " WHERE role = ?"
                    params.append(role)
                
                query += " ORDER BY created_at ASC"
                
                if limit:
                    query += " LIMIT ?"
                    params.append(limit)
                
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []
    
    def clear_messages(self) -> bool:
        """
        Clear all messages from the database.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {self.table_name}")
                conn.commit()
                return True
        except Exception as e:
            print(f"Error clearing messages: {e}")
            return False
    
    def get_message_count(self, role: Optional[str] = None) -> int:
        """
        Get the total number of messages.
        
        Args:
            role: Optional filter by role
        
        Returns:
            int: Number of messages
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                query = f"SELECT COUNT(*) FROM {self.table_name}"
                params = []
                
                if role:
                    query += " WHERE role = ?"
                    params.append(role)
                
                cursor.execute(query, params)
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting message count: {e}")
            return 0
    
    def delete_message(self, message_id: int) -> bool:
        """
        Delete a specific message by ID.
        
        Args:
            message_id: The ID of the message to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (message_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting message: {e}")
            return False

import sqlite3
import os


class CardDatabase:
    """SQLite database for card management"""

    def __init__(self, db_path="cards.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database and create tables if needed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create cards table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE NOT NULL,
                number TEXT UNIQUE NOT NULL,
                name TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def add_card(self, uid, number, name=None):
        """Add a new card to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO cards (uid, number, name) VALUES (?, ?, ?)",
                (uid, number, name)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_card(self, uid=None, number=None):
        """Check if card exists and is active"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if uid:
                cursor.execute(
                    "SELECT 1 FROM cards WHERE uid = ? AND status = 'active'",
                    (uid,)
                )
            elif number:
                cursor.execute(
                    "SELECT 1 FROM cards WHERE number = ? AND status = 'active'",
                    (number,)
                )
            else:
                return False

            result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception:
            return False

    def list_cards(self):
        """Get all active cards"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT uid, number, name FROM cards WHERE status = 'active'")
            cards = cursor.fetchall()
            conn.close()
            return cards
        except Exception:
            return []

    def deactivate_card(self, uid=None, number=None):
        """Deactivate a card"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if uid:
                cursor.execute("UPDATE cards SET status = 'inactive' WHERE uid = ?", (uid,))
            elif number:
                cursor.execute("UPDATE cards SET status = 'inactive' WHERE number = ?", (number,))

            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

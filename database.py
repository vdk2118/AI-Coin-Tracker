import sqlite3
from config import DATABASE_NAME


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Watchlist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watchlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        contract TEXT NOT NULL,
        nickname TEXT DEFAULT '',
        chain TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Setările utilizatorului
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        chat_id INTEGER PRIMARY KEY,
        chain TEXT DEFAULT 'ALL',
        min_liquidity INTEGER DEFAULT 50000,
        min_volume INTEGER DEFAULT 100000,
        alerts INTEGER DEFAULT 1
    )
    """)

    # Istoric analize
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        contract TEXT,
        token_name TEXT,
        ai_score INTEGER,
        analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# ===========================
# WATCHLIST
# ===========================

def add_token(chat_id, contract, nickname=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM watchlist WHERE chat_id=? AND contract=?",
        (chat_id, contract)
    )

    if cursor.fetchone():
        conn.close()
        return False

    cursor.execute(
        """
        INSERT INTO watchlist(chat_id, contract, nickname)
        VALUES (?, ?, ?)
        """,
        (chat_id, contract, nickname)
    )

    conn.commit()
    conn.close()
    return True


def get_tokens(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT contract, nickname
        FROM watchlist
        WHERE chat_id=?
        ORDER BY created_at DESC
        """,
        (chat_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_token(chat_id, contract):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM watchlist
        WHERE chat_id=? AND contract=?
        """,
        (chat_id, contract)
    )

    conn.commit()
    conn.close()


# ===========================
# SETTINGS
# ===========================

def create_settings(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO settings(chat_id)
        VALUES (?)
        """,
        (chat_id,)
    )

    conn.commit()
    conn.close()


def get_settings(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT chain, min_liquidity, min_volume, alerts
        FROM settings
        WHERE chat_id=?
        """,
        (chat_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return row


# ===========================
# HISTORY
# ===========================

def save_analysis(chat_id, contract, token_name, ai_score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO history(chat_id, contract, token_name, ai_score)
        VALUES (?, ?, ?, ?)
        """,
        (chat_id, contract, token_name, ai_score)
    )

    conn.commit()
    conn.close()


def get_history(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT token_name, ai_score, analyzed_at
        FROM history
        WHERE chat_id=?
        ORDER BY analyzed_at DESC
        LIMIT 10
        """,
        (chat_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
import sqlite3

def connect_db():
    conn = sqlite3.connect('rules.db')
    return conn

def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS rules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        rule_text TEXT,
                        ast_structure TEXT)''')
    conn.commit()
    conn.close()

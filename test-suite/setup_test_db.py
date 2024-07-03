import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('test_results.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS test_results
                 (file_name TEXT PRIMARY KEY,
                  last_run TIMESTAMP,
                  status TEXT,
                  force_run BOOLEAN)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()

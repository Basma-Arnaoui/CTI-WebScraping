import sqlite3

DATABASE = 'cve.db'  # Replace with your actual database path

def check_database_integrity():
    conn = sqlite3.connect(DATABASE)
    try:
        result = conn.execute('PRAGMA integrity_check;').fetchall()
        for row in result:
            print(row)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    check_database_integrity()

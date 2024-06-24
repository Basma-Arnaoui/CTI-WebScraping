import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'database.db')

class Article:
    def __init__(self, title, url, summary, date, source, image=None):
        self.title = title
        self.url = url
        self.summary = summary
        self.date = date
        self.source = source
        self.image = image

    @classmethod
    def fetch_from_db(cls, source=None, keywords=[]):
        conn = sqlite3.connect(DATABASE)
        query = 'SELECT title, url, summary, date, source, image FROM articles'
        params = []

        if source:
            query += ' WHERE source = ?'
            params.append(source)

        if keywords:
            keyword_query = ' OR '.join(['title GLOB ? OR summary GLOB ? OR url GLOB ?' for _ in keywords])
            if source:
                query += f' AND ({keyword_query})'
            else:
                query += f' WHERE {keyword_query}'
            for keyword in keywords:
                params.extend([f'*{keyword}*', f'*{keyword}*', f'*{keyword}*'])

        cursor = conn.execute(query, params)
        articles = [
            cls(title=row[0], url=row[1], summary=row[2], date=row[3], source=row[4], image=row[5])
            for row in cursor.fetchall()
        ]
        conn.close()
        return articles

    def save_to_db(self):
        conn = sqlite3.connect(DATABASE)
        conn.execute(
            'INSERT INTO articles (title, url, summary, date, source, image) VALUES (?, ?, ?, ?, ?, ?)',
            (self.title, self.url, self.summary, self.date, self.source, self.image)
        )
        conn.commit()
        conn.close()

def initialize_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT,
            summary TEXT,
            date TEXT,
            source TEXT,
            image TEXT
        )
    ''')
    conn.close()

def initialize_cve_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cve_id TEXT,
            vendor_project TEXT,
            product TEXT,
            vulnerability_name TEXT,
            date_added TEXT,
            short_description TEXT,
            required_action TEXT,
            due_date TEXT,
            known_ransomware_campaign_use TEXT,
            notes TEXT,
            score TEXT
        )
    ''')
    conn.close()
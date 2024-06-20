# app/models.py

import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'articles.db')

class Article:
    def __init__(self, title, url, summary, date, keywords, source, image=None):
        self.title = title
        self.url = url
        self.summary = summary
        self.date = date
        self.keywords = keywords
        self.source = source
        self.image = image

    @classmethod
    def fetch_from_db(cls, source=None, keywords=[]):
        conn = sqlite3.connect(DATABASE)
        query = 'SELECT title, url, summary, date, keywords, source, image FROM articles'
        params = []

        if source:
            query += ' WHERE source = ?'
            params.append(source)

        if keywords:
            if source:
                query += ' AND '
            else:
                query += ' WHERE '
            query += ' AND '.join(['(title LIKE ? OR summary LIKE ?)' for _ in keywords])
            params.extend([f'%{keyword}%', f'%{keyword}%'] for keyword in keywords)

        cursor = conn.execute(query, [item for sublist in params for item in sublist])
        articles = [
            cls(title=row[0], url=row[1], summary=row[2], date=row[3], keywords=row[4], source=row[5], image=row[6])
            for row in cursor.fetchall()
        ]
        conn.close()
        return articles

    def save_to_db(self):
        conn = sqlite3.connect(DATABASE)
        conn.execute(
            'INSERT INTO articles (title, url, summary, date, keywords, source, image) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (self.title, self.url, self.summary, self.date, self.keywords, self.source, self.image)
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
            keywords TEXT,
            source TEXT,
            image TEXT
        )
    ''')
    conn.close()

# app/models.py

import sqlite3
from contextlib import closing

class Article:
    def __init__(self, title, url, summary, date, keywords, source, image=None):
        self.title = title
        self.url = url
        self.summary = summary
        self.date = date
        self.keywords = keywords
        self.source = source
        self.image = image


    def save_to_db(self):
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('''
                    INSERT INTO articles (title, url, summary, date, keywords, source, image)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (self.title, self.url, self.summary, self.date, self.keywords, self.source, self.image))
        conn.commit()
        conn.close()
    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'summary': self.summary,
            'date': self.date,
            'keywords': self.keywords
        }

    @staticmethod
    def fetch_from_db(source=None):
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        if source:
            cursor.execute("SELECT title, url, summary, date, keywords, source, image FROM articles WHERE source=?",
                           (source,))
        else:
            cursor.execute("SELECT title, url, summary, date, keywords, source, image FROM articles")
        rows = cursor.fetchall()
        conn.close()
        articles = [Article(*row) for row in rows]
        return articles

def initialize_db():
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    cursor.execute('''
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
    conn.commit()
    conn.close()
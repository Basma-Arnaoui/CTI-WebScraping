import sqlite3
import os
from datetime import datetime


ARTICLES_DATABASE = os.path.join(os.path.dirname(__file__), '..', 'articles.db')
CVE_DATABASE = os.path.join(os.path.dirname(__file__), '..', 'cve.db')

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
        conn = sqlite3.connect(ARTICLES_DATABASE)
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
        conn = sqlite3.connect(ARTICLES_DATABASE)
        conn.execute(
            'INSERT INTO articles (title, url, summary, date, source, image) VALUES (?, ?, ?, ?, ?, ?)',
            (self.title, self.url, self.summary, self.date, self.source, self.image)
        )
        conn.commit()
        conn.close()

def initialize_db():
    conn = sqlite3.connect(ARTICLES_DATABASE)
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
    conn = sqlite3.connect(CVE_DATABASE)
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

def get_db_connection():
    conn = sqlite3.connect(ARTICLES_DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_cve_db_connection():
    conn = sqlite3.connect(CVE_DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
def insert_cve_data(cve_data):
    conn = sqlite3.connect(CVE_DATABASE)
    cursor = conn.cursor()
    for cve in cve_data:
        cursor.execute('''
            INSERT INTO cves (cve_id, vendor_project, product, vulnerability_name, date_added, short_description, required_action, due_date, known_ransomware_campaign_use, notes, score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            cve["CVE ID"], cve["Vendor Project"], cve["Product"], cve["Vulnerability Name"],
            cve["Date Added"], cve["Short Description"], cve["Required Action"], cve["Due Date"],
            cve["Known Ransomware Campaign Use"], cve["Notes"], "None"  # Store "None" as a string initially
        ))
    conn.commit()
    conn.close()


def get_sorted_cves(sort_order='date'):
    conn = get_cve_db_connection()
    current_year = datetime.now().year

    if sort_order == 'severity':
        query = f'SELECT * FROM cves WHERE cve_id LIKE "CVE-{current_year}-%" ORDER BY CAST(SUBSTR(score, 1, INSTR(score, " ")) AS FLOAT) DESC'
        cves = conn.execute(query).fetchall()
        return cves
    else:
        cves = conn.execute('SELECT * FROM cves').fetchall()
        conn.close()

        def sort_key(cve):
            parts = cve['cve_id'].split('-')
            year = int(parts[1])
            seq_num = int(parts[2])
            return (year, seq_num)

        sorted_cves = sorted(cves, key=sort_key, reverse=True)
        return sorted_cves



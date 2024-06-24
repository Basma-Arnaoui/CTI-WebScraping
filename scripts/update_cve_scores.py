import sqlite3
from cisa_scraper import get_cvss_score  # Assuming get_cvss_score is in the cisa_scraper module
import os
import sys
DATABASE = os.path.join(os.path.dirname(__file__), '..', 'cve.db')
from cisa_scraper import scrape_cisa_known_exploited_vulnerabilities
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import initialize_cve_db, insert_cve_data

def get_db_connection():
    initialize_cve_db()
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def update_cve_scores():
    conn = get_db_connection()
    cursor = conn.cursor()
    #data = scrape_cisa_known_exploited_vulnerabilities()
    #insert_cve_data(data)
    cursor.execute('SELECT cve_id FROM cves')
    cves = cursor.fetchall()
    i=599
    for cve in cves[600:1000]:
        cve_id = cve['cve_id']
        score = get_cvss_score(cve_id)
        cursor.execute('UPDATE cves SET score = ? WHERE cve_id = ?', (score, cve_id))
        print(f'Updated CVE {cve_id} with score {score}')
        i+=1
        print(i)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    update_cve_scores()

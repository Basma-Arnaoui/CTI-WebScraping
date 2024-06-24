from flask import Flask, render_template, request, redirect, url_for
from app.models import Article
import sqlite3
from scripts.cisa_scraper import scrape_cisa_known_exploited_vulnerabilities, get_cvss_score
from app.models import get_db_connection, get_cve_db_connection
app = Flask(__name__)


@app.route('/')
@app.route('/page/<int:page>')
def home(page=1):
    return redirect(url_for('filter_by_keywords', source='All', page=page))


@app.route('/filter', methods=['POST', 'GET'])
@app.route('/filter/page/<int:page>', methods=['POST', 'GET'])
def filter_by_keywords(page=1):
    if request.method == 'POST':
        keywords = request.form.get('keywords', '').split(',')
        source = request.form.get('source')
    else:
        keywords = request.args.get('keywords', '').split(',')
        source = request.args.get('source', 'All')

    articles = Article.fetch_from_db(source if source != 'All' else None, keywords)

    per_page = 5
    offset = (page - 1) * per_page
    conn = get_cve_db_connection()
    cves = conn.execute('SELECT * FROM cves ORDER BY id DESC LIMIT ? OFFSET ?', (per_page, offset)).fetchall()
    print("Fetched CVEs from DB:", cves)  # Debug statement

    updated_cves = []
    for cve in cves:
        cve_dict = dict(cve)
        cve_dict['nvd_link'] = f"https://nvd.nist.gov/vuln/detail/{cve_dict['cve_id']}"
        updated_cves.append(cve_dict)
    conn.close()
    print(updated_cves)
    total_cves = len(scrape_cisa_known_exploited_vulnerabilities())
    total_pages = (total_cves + per_page - 1) // per_page

    return render_template('home.html', articles=articles, current_filter=source, keywords=keywords, cves=updated_cves, page=page, total_pages=total_pages)
@app.route('/clear_filters', methods=['POST'])
def clear_filters():
    source = request.form.get('current_filter', 'All')
    return redirect(url_for('filter_by_keywords', source=source, keywords=''))


from .scheduler import start_scheduler

start_scheduler()
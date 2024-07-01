from flask import Flask, render_template, request, redirect, url_for
from app.models import Article
from app.models import get_sorted_cves, get_vendor_distribution
import json
from collections import Counter
from datetime import datetime

app = Flask(__name__)


@app.route('/')
@app.route('/page/<int:page>')
def home(page=1):
    return redirect(url_for('filter_by_keywords', source='All', page=page))


@app.route('/filter', methods=['POST', 'GET'])
def filter_by_keywords(page=1):
    if request.method == 'POST':
        keywords = request.form.get('keywords', '').split(',')
        source = request.form.get('source')
    else:
        keywords = request.args.get('keywords', '').split(',')
        source = request.args.get('source', 'All')

    page = int(request.args.get('page', 1))

    articles = Article.fetch_from_db(source if source != 'All' else None, keywords)

    per_page = 5
    offset = (page - 1) * per_page

    sort_order = request.args.get('sort', 'date')

    # Fetch all CVEs and sort them
    sorted_cves = get_sorted_cves(sort_order)

    # Paginate the sorted CVEs
    paginated_cves = sorted_cves[offset:offset + per_page]

    updated_cves = []
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'UNKNOWN': 0}
    vendor_counter = Counter()

    current_year = datetime.now().year

    for cve in paginated_cves:
        cve_dict = dict(cve)
        cve_dict['nvd_link'] = f"https://nvd.nist.gov/vuln/detail/{cve_dict['cve_id']}"
        updated_cves.append(cve_dict)

    graph = get_sorted_cves("severity")
    for cve in graph:
        cve_dict = dict(cve)
        # Count severities
        if 'CRITICAL' in cve_dict['score']:
            severity_counts['CRITICAL'] += 1
        elif 'HIGH' in cve_dict['score']:
            severity_counts['HIGH'] += 1
        elif 'MEDIUM' in cve_dict['score']:
            severity_counts['MEDIUM'] += 1
        elif 'LOW' in cve_dict['score']:
            severity_counts['LOW'] += 1
        else:
            severity_counts['UNKNOWN'] += 1

        # Count vendors for the current year
        date_added = cve_dict.get('date_added', '')
        if date_added.startswith(str(current_year)):
            vendor_counter[cve_dict['vendor_project']] += 1

    total_cves = len(sorted_cves)
    total_pages = (total_cves + per_page - 1) // per_page

    severity_counts_json = json.dumps(severity_counts)
    vendor_counts_json = json.dumps(vendor_counter)

    return render_template('home.html', articles=articles, current_filter=source, keywords=keywords, cves=updated_cves,
                           page=page, total_pages=total_pages, sort_order=sort_order,
                           severity_counts_json=severity_counts_json, vendor_counts_json=vendor_counts_json)



@app.route('/clear_filters', methods=['POST'])
def clear_filters():
    source = request.form.get('current_filter', 'All')
    return redirect(url_for('filter_by_keywords', source=source, keywords=''))


from .scheduler import start_scheduler

start_scheduler()
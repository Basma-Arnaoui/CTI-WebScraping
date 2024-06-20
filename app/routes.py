from flask import Flask, render_template, request, redirect, url_for
from app.models import Article

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('filter_by_keywords', source='All'))

@app.route('/filter', methods=['POST', 'GET'])
def filter_by_keywords():
    if request.method == 'POST':
        keywords = request.form.get('keywords', '').split(',')
        source = request.form.get('source')
    else:
        keywords = request.args.get('keywords', '').split(',')
        source = request.args.get('source', 'All')

    articles = Article.fetch_from_db(source if source != 'All' else None, keywords)
    return render_template('home.html', articles=articles, current_filter=source, keywords=keywords)

@app.route('/clear_filters', methods=['POST'])
def clear_filters():
    source = request.form.get('current_filter', 'All')
    return redirect(url_for('filter_by_keywords', source=source, keywords=''))

from .scheduler import start_scheduler

start_scheduler()

# app/routes.py

from flask import Flask, render_template, request
from app.models import Article
from app.run_scrapers import run_all_scrapers

app = Flask(__name__)


@app.route('/')
def home():
    articles = Article.fetch_from_db()
    return render_template('home.html', articles=articles)


@app.route('/filter', methods=['GET', 'POST'])
def filter_by_website():
    source = request.args.get('source')
    keywords = request.args.get('keywords', '').split(',')

    if request.method == 'POST':
        # Run all scrapers with the provided keywords
        run_all_scrapers(keywords)

    articles = Article.fetch_from_db(source, keywords)
    return render_template('home.html', articles=articles, current_filter=source, current_keywords=keywords)



from .scheduler import start_scheduler

start_scheduler()
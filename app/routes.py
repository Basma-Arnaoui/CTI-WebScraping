# app/routes.py

from flask import Flask, render_template, request
from app.models import Article

app = Flask(__name__)
@app.route('/')
def home():
    articles = Article.fetch_from_db()
    return render_template('home.html', articles=articles)

@app.route('/filter')
def filter_by_website():
    source = request.args.get('source')
    articles = Article.fetch_from_db(source)
    if source is None:
        source="All"
    return render_template('home.html', articles=articles, current_filter=source)


from .scheduler import start_scheduler

start_scheduler()
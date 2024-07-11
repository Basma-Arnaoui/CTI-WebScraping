# run.py

from app.routes import app
from scripts.articles_summary import update_summaries_db, delete_yesterdays_summaries
from app.run_scrapers import run_all_scrapers
from contextlib import closing
import sqlite3
from app.models import initialize_db
# Start the Flask app
if __name__ == "__main__":
    print("bdina")
    #with closing(sqlite3.connect('articles.db')) as conn:
    #    with conn:
    #        conn.execute('DELETE FROM articles')
    # Initialize the database
    #initialize_db()
    print("hna")
    #initialize_cve_db()
    #run_all_scrapers()

    #app.run()
    #refresh_articles()
    delete_yesterdays_summaries()

    #print("basma")
    update_summaries_db()
    app.run()
    #delete_yesterdays_summaries()

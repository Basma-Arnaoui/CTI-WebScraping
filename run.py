# run.py

from app.routes import app
from app.models import initialize_db, initialize_cve_db
from app.scheduler import clear_db
from app.run_scrapers import  run_all_scrapers
import sqlite3
from contextlib import closing


# Start the Flask app
if __name__ == "__main__":
    #with closing(sqlite3.connect('articles.db')) as conn:
     #   with conn:
      #      conn.execute('DELETE FROM articles')
    # Initialize the database
    #initialize_db()
    #initialize_cve_db()
    #run_all_scrapers()

    app.run()

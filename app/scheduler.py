# app/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
from contextlib import closing

def clear_db():
    with closing(sqlite3.connect('articles.db')) as conn:
        with conn:
            conn.execute('DELETE FROM articles')

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_db, 'cron', hour=8)
    scheduler.start()



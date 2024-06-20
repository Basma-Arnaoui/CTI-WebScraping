# run.py

from app.routes import app
from app.models import initialize_db
from app.run_scrapers import  run_all_scrapers

# Initialize the database
initialize_db()

# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True)

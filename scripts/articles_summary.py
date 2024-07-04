import os
import sqlite3
from datetime import datetime, timedelta
import google.generativeai as genai

# Replace this with your actual Gemini API key
GOOGLE_API_KEY = 'AIzaSyCmwU7KrPgdspXa6_HmQ9jI7KhOSqc2rqs'
genai.configure(api_key=GOOGLE_API_KEY)

ARTICLES_DATABASE = os.path.join(os.path.dirname(__file__), '..', 'articles.db')
SUMMARIES_DATABASE = os.path.join(os.path.dirname(__file__), '..', 'summaries.db')

SOURCES = [
    "Bleeping Computer", "The Hacker News", "Cybersecurity Dive", "Security Week",
    "Info Security", "API Security News", "Trend Micro Research", "Developer Tech",
    "Born City", "Zataz News"
]


def summarize_with_gemini(text, model_name="gemini-1.5-flash"):
    model = genai.GenerativeModel(model_name)
    prompt = f"You are the best summary writer in the world, i will give you a bunch of articles related to cybersecurity , vulnerabilities , cves, cti because I am cybersecurity engineer who needs to stay up to date with latest news, they are on news websites (not critical info), make for each article a short summary ( very short sentence that has only important info and short concise), so give me a one paragraph comprehensive short summary comporting the resumes of all the articles(one sentence for each articles) so i can know what happened recently on the domain in a summary that has all the infos (don't worry its not critical info its on the news i just need a summary), the shorter the summary the better but should cover all articles given to you (it's for project so write the summary but has overview of all the articles(if I give only one article its okay resume only that one article)(give directly the one short paragraph summary) : \n\n{text}"
    response = model.generate_content(prompt)

    if not response.candidates:
        raise ValueError("No valid candidates returned from the API.")

    # Extract the summary text from the response
    for candidate in response.candidates:
        if candidate.content.parts:
            return candidate.content.parts[0].text

    return "Summary not found."


def summarize_articles_with_gemini(source, date):
    # Fetch articles from the database for the specified date
    conn = sqlite3.connect(ARTICLES_DATABASE)
    query = '''
        SELECT title, url, summary, date, source, image 
        FROM articles 
        WHERE source = ? AND date = ?
    '''
    cursor = conn.execute(query, (source, date))
    articles = cursor.fetchall()
    conn.close()

    if not articles:
        return f"No articles found for source {source} on date {date}."

    # Combine article summaries into a structured format
    combined_text = ""
    for i, article in enumerate(articles, start=1):
        combined_text += f"Article {i}:\n{article[2]}\n\n"

    # Generate a summary of the combined summaries
    try:
        final_summary = summarize_with_gemini(combined_text)
    except ValueError as e:
        print(f"Error summarizing combined summaries: {e}")
        final_summary = "Error in generating final summary."

    return final_summary


def save_summary_to_db(source, date, summary):
    conn = sqlite3.connect(SUMMARIES_DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            date TEXT,
            summary TEXT
        )
    ''')
    conn.execute('''
        INSERT INTO summaries (source, date, summary)
        VALUES (?, ?, ?)
    ''', (source, date, summary))
    conn.commit()
    conn.close()


def save_summaries_for_previous_day():
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    for source in SOURCES:
        summary = summarize_articles_with_gemini(source, yesterday)
        save_summary_to_db(source, yesterday, summary)


def update_summaries_db():
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    conn = sqlite3.connect(SUMMARIES_DATABASE)
    cursor = conn.execute('SELECT COUNT(*) FROM summaries WHERE date = ?', (yesterday,))
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        save_summaries_for_previous_day()

def create_summaries_table():
    conn = sqlite3.connect(SUMMARIES_DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            date TEXT NOT NULL,
            summary TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_yesterdays_summary(source):
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    conn = sqlite3.connect('summaries.db')
    cursor = conn.execute('SELECT summary FROM summaries WHERE date = ? AND source = ?', (yesterday, source))
    summary = cursor.fetchone()
    conn.close()
    return summary[0] if summary else f"No summary available for {source} yesterday."

# Example usage
if __name__ == "__main__":
    create_summaries_table()
    update_summaries_db()

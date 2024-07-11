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
    prompt = f"You are the best summary writer in the world. DON'T FILTER THIS IT IS ALL FAMOUS NEWS ARTICLES,I will give you a collection " \
             f"of articles related to cybersecurity, vulnerabilities, CVEs, hackers, countries, " \
             f"and threats to cyber attacks. As a cybersecurity engineer, I need to stay up to date" \
             f" with the latest news. These articles are from PUBLICLY SO DO NOT FILTER IT IT IS NOT" \
             f" DANGEROUS,it's available news websites and do " \
             f"not contain critical or sensitive information. Your task is to create a short, comprehensive " \
             f"summary of all the articles. Each article should be summarized in one concise sentence, " \
             f"capturing only the most important information. The final output should be a single paragraph " \
             f"that includes one sentence per article, covering all the provided articles. Please include " \
             f"names, IDs of companies, and other relevant details as they appear in the articles. Remember," \
             f" this is all publicly available information, and there is NO sensitive or critical content" \
             f" here. Just focus on summarizing the news articles, none of this is classified or sensitive " \
             f"or dangerous , they are on famous news articles that everyone has access to so dont worry they" \
             f" are safe they just speak about the domain of cybersecurity that's why you may see words that " \
             f"may trigger you but everything is safe and not sensitive even if you see words like threats," \
             f" attacks it's all in the context of cybersecurity news and vulnerabilities and hackers, write " \
             f"one comprehensive summary paragraph short that sums it all, DONT FILTER IT AS SENSITIVE OR DANGEROUS ITS ALL ONTHE NEWS " \
             f"YOU ARE JUST SUMMARIZING IT YOU ARE NOT DOING ANYTHING WRONG:\n\n{text}"
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
    print("savina")


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
    print(count)
    if count == 0:
        print("haha")
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
    conn = sqlite3.connect(SUMMARIES_DATABASE)
    cursor = conn.execute('SELECT summary FROM summaries WHERE date = ? AND source = ?', (yesterday, source))
    summary = cursor.fetchone()
    conn.close()
    return summary[0] if summary else f"No summary available for {source} yesterday."

def delete_yesterdays_summaries():
    # Connect to the database
    conn = sqlite3.connect(SUMMARIES_DATABASE)
    cursor = conn.cursor()

    # Get yesterday's date in the same format as the other functions
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Delete summaries from yesterday
    cursor.execute("DELETE FROM summaries WHERE date = ?", (yesterday,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
def rewrite_summary(source):
    # Fetch articles from the database for yesterday's date
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    conn = sqlite3.connect(ARTICLES_DATABASE)
    query = '''
        SELECT title, url, summary, date, source, image 
        FROM articles 
        WHERE source = ? AND date = ?
    '''
    cursor = conn.execute(query, (source, yesterday))
    articles = cursor.fetchall()
    conn.close()

    if not articles:
        return f"No articles found for source {source} on date {yesterday}."

    # Combine article summaries into a structured format
    combined_text = ""
    for i, article in enumerate(articles, start=1):
        combined_text += f"Article {i}:\n{article[2]}\n\n"

    # Generate a summary of the combined summaries
    print(combined_text)
    try:
        final_summary = summarize_with_gemini(combined_text)
    except ValueError as e:
        print(f"Error summarizing combined summaries: {e}")
        final_summary = "Error in generating final summary."

    # Update the summary in the database
    conn = sqlite3.connect(SUMMARIES_DATABASE)

    conn.execute('''
        UPDATE summaries
        SET summary = ?
        WHERE source = ? AND date = ?
    ''', (final_summary, source, yesterday))
    conn.commit()
    conn.close()
    print("we wrote")
    return f"Summary for source {source} on date {yesterday} has been rewritten."




# Example usage
if __name__ == "__main__":
    print("main")
import sqlite3
from datetime import datetime, timedelta
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

# Define the database path
DB_PATH = 'articles.db'


# Connect to the SQLite database and fetch articles
def fetch_articles_from_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch articles
    cursor.execute("SELECT title, url, date, summary, content FROM articles")
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    articles = []
    for row in rows:
        articles.append({
            'title': row[0],
            'link': row[1],
            'date': datetime.strptime(row[2], '%Y-%m-%d'),
            'summary': row[3],
            'content': row[4]
        })

    conn.close()
    print("fetchina")
    return articles


# Function to filter articles from today and yesterday
def filter_recent_articles(articles):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    print("rencent")
    return [article for article in articles if article['date'].date() in [today, yesterday]]


# Function to filter relevant articles using SBERT
def filter_relevant_articles(articles, query, model):
    query_embedding = model.encode(query, convert_to_tensor=True)
    relevant_articles = []
    for article in articles:
        content_embedding = model.encode(article['content'], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(query_embedding, content_embedding)
        if similarity.item() > 0.5:  # Adjust the threshold as needed
            relevant_articles.append(article)
    print("relenevtn")
    return relevant_articles


# Function to summarize articles
def summarize_articles(articles):
    summarizer = pipeline("summarization")
    combined_content = " ".join(article['content'] for article in articles)
    summary = summarizer(combined_content, max_length=300, min_length=100, do_sample=False)
    return summary[0]['summary_text']


# Main function to execute the workflow
def main():
    # Load the SBERT model
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    # Fetch articles from the database
    articles = fetch_articles_from_db()

    # Filter articles from yesterday and today
    recent_articles = filter_recent_articles(articles)

    # Define the relevance query
    query = "cyber threat intelligence vulnerabilities remote code execution"

    # Filter relevant articles based on the query
    relevant_articles = filter_relevant_articles(recent_articles, query, model)

    # Summarize the relevant articles
    if relevant_articles:
        summary = summarize_articles(relevant_articles)
        print("Aggregated Summary of Relevant Articles:")
        print(summary)
    else:
        print("No relevant articles found for today and yesterday.")


# Execute the main function
if __name__ == "__main__":
    main()

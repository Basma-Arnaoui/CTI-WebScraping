import os
import sqlite3
import google.generativeai as genai

# Replace this with your actual Gemini API key
GOOGLE_API_KEY = 'AIzaSyCmwU7KrPgdspXa6_HmQ9jI7KhOSqc2rqs'
genai.configure(api_key=GOOGLE_API_KEY)

ARTICLES_DATABASE = os.path.join(os.path.dirname(__file__), '..', 'articles.db')


def summarize_with_gemini(text, model_name="gemini-1.5-flash"):
    model = genai.GenerativeModel(model_name)
    prompt = f"You are the best summary writer in the world, i will give you a bunch of articles related to cybersecurity and cti, make for each article a short summary ( very short sentence that has only important info and short concise), so give me a one paragraph comprehensive short summary comporting the resumes of all the info so i can know what happened recently on the domain in a summary that has all the infos:\n\n{text}"
    response = model.generate_content(prompt)

    if not response.candidates:
        raise ValueError("No valid candidates returned from the API.")

    # Extract the summary text from the response
    for candidate in response.candidates:
        if candidate.content.parts:
            return candidate.content.parts[0].text

    return "Summary not found."


def summarize_articles_with_gemini(source, start_date, end_date):
    # Fetch articles from the database
    conn = sqlite3.connect(ARTICLES_DATABASE)
    query = '''
        SELECT title, url, summary, date, source, image 
        FROM articles 
        WHERE source = ? AND date BETWEEN ? AND ?
    '''
    cursor = conn.execute(query, (source, start_date, end_date))
    articles = cursor.fetchall()
    conn.close()

    if not articles:
        return "No articles found for the given source and date range."

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


# Example usage
if __name__ == "__main__":
    source = 'Bleeping Computer'
    start_date = '2024-07-01'
    end_date = '2024-07-02'
    summary = summarize_articles_with_gemini(source, start_date, end_date)
    print(summary)

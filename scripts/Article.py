class Article:
    def __init__(self, title, url, summary, date, keywords):
        self.title = title
        self.url = url
        self.summary = summary
        self.date = date
        self.keywords = keywords

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'summary': self.summary,
            'date': self.date,
            'keywords': self.keywords
        }

from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

URL = "https://news.ycombinator.com/item?id=42919502"


def scrape_data():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    elements = soup.find_all(class_="ind", indent=0)

    comments = []
    for e in elements:
        comment = e.find_next(class_="comment")
        if comment:
            comments.append(comment.get_text())

    keywords = {
        "python": 0,
        "javascript": 0,
        "typescript": 0,
        "go": 0,
        "c#": 0,
        "java": 0,
        "rust": 0,
    }

    for comment in comments:
        words = {w.strip(".,/:;!@#()[]") for w in comment.lower().split()}
        for k in keywords:
            if k in words:
                keywords[k] += 1

    return keywords


@app.get("/scraping")
def get_scraping():
    return scrape_data()
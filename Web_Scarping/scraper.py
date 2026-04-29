import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


URL = "https://news.ycombinator.com/item?id=42919502"


def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print("Erreur:", e)
        return None


def extract_comments(html):
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.find_all(class_="ind", indent=0)

    comments = []
    for e in elements:
        comment = e.find_next(class_="comment")
        if comment:
            comments.append(comment.get_text())

    return comments


def analyze_keywords(comments):
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


def plot_results(data):
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

    plt.figure(figsize=(10, 6))
    bars = plt.bar(sorted_data.keys(), sorted_data.values())

    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(int(bar.get_height())),
            ha="center",
        )

    plt.title("Langages populaires")
    plt.savefig("results.png")
    plt.show()


def main():
    html = fetch_page(URL)
    if not html:
        return

    comments = extract_comments(html)
    print("Commentaires:", len(comments))

    data = analyze_keywords(comments)

    print("\nRésultats:")
    for k, v in data.items():
        print(k, ":", v)

    plot_results(data)


if __name__ == "__main__":
    main()
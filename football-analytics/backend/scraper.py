import requests
from bs4 import BeautifulSoup

def scrape_player_info(player_name):
    url = f"https://en.wikipedia.org/wiki/{player_name.replace(' ', '_')}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Player not found"}

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1").text
    paragraph = soup.find("p")
    summary = paragraph.text.strip() if paragraph else "No summary available."
    return {"name": title, "summary": summary}

import requests
from bs4 import BeautifulSoup


def get_text_content_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text_content = soup.get_text(separator="\n", strip=True)

        return text_content

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

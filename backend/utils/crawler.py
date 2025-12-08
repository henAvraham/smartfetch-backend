import requests
from bs4 import BeautifulSoup
from typing import Optional, Tuple


HEADERS = {
   
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


def fetch_page_text(url: str) -> tuple[Optional[str], str]:
    """
    Fetch an HTML page and extract a clean title and main text content.

    Returns:
        (title, content_text)
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[CRAWLER] request failed for {url}: {e}")
        return None, ""

    soup = BeautifulSoup(response.text, "lxml")

    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else None

    
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    main_container = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", attrs={"role": "main"})
        or soup.body
    )

    texts: list[str] = []

    if main_container:
        for element in main_container.find_all(
            ["p", "li", "h1", "h2", "h3", "h4", "div", "span"]
        ):
            text = element.get_text(separator=" ", strip=True)
            if text:
                texts.append(text)

    content = "\n".join(texts)

    
    if len(content) < 200 and soup.body:
        raw_text = soup.body.get_text(separator="\n", strip=True)
        content = raw_text
    return title, content








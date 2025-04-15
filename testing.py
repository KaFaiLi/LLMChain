from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from config import GOOGLE_SEARCH_HEADERS, MAX_SEARCH_RESULTS


UPDATED_GOOGLE_NEWS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://news.google.com/"
}

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def google_news_search(query: str) -> List[Dict[str, str]]:
    """Perform a Google News search and return a list of news results (title, link, snippet)."""
    url = f"https://news.google.com/search?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
    response = requests.get(url, headers=UPDATED_GOOGLE_NEWS_HEADERS, verify=False)
    if response.status_code != 200:
        return [{"error": f"Failed to fetch results: {response.status_code}"}]
    soup = BeautifulSoup(response.text, "html.parser")
    html_preview = response.text[:1000]
    print("--- Google News HTML Preview (first 1000 chars) ---\n", html_preview, "\n--- END HTML Preview ---\n")
    articles = soup.select('article')
    print(f"Found {len(articles)} <article> blocks.")
    for i, article in enumerate(articles[:3]):
        print(f"--- Article {i+1} HTML ---\n{article.prettify()}\n--- END Article {i+1} ---\n")
    results = []
    for i, article in enumerate(articles):
        title_elem = article.select_one('a.JtKRv')
        publisher_elem = article.select_one('.vr1PYe')
        author_elem = article.select_one('.bInasb span')
        if title_elem:
            link = title_elem['href']
            if link.startswith('./'):
                link = 'https://news.google.com' + link[1:]
            results.append({
                "title": title_elem.get_text(strip=True),
                "link": link,
                "publisher": publisher_elem.get_text(strip=True) if publisher_elem else "",
                "author": author_elem.get_text(strip=True) if author_elem else ""
            })
        if len(results) >= MAX_SEARCH_RESULTS:
            break
    return results

# Let's inspect some of the attributes associated with the tool.
print(multiply.name)
print(multiply.description)
print(multiply.args)

tools = [multiply, google_news_search]
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="openai/gpt-4o-mini-2024-07-18", 
                 base_url="https://openrouter.ai/api/v1",
                api_key='')
llm_with_tools = llm.bind_tools(tools)

query = "What are the latest news about OpenAI?"
result = llm_with_tools.invoke(query)
print(result)
print(result.tool_calls)
print(result.content)

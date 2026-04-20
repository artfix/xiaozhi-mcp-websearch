# websearch.py ​​- dynamic year processing version
from mcp.server.fastmcp import FastMCP
import sys
import logging
import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime, timedelta

logger = logging.getLogger('xiaozhi_search')

mcp = FastMCP("mcps")

def extract_and_validate_time(text: str) -> datetime:
    """Extract time from text and verify if it is the current year"""
    now = datetime.now()
    current_year = now.year

    # 1. Complete date of processing (June 15, 2024)
    if match := re.search(r'(\d{4})Year(\d{1,2})Month(\d{1,2})Day', text):
        year, month, day = map(int, match.groups())
        if year == current_year:
            return datetime(year, month, day)

    # 2. Handle date without year (June 15)
    elif match := re.search(r'(\d{1,2})month(\d{1,2})day', text):
        month, day = map(int, match.groups())
        return datetime(current_year, month, day)

    # 3. Process abbreviated dates (06-15)
    elif match := re.search(r'(\d{1,2})-(\d{1,2})', text):
        month, day = map(int, match.groups())
        return datetime(current_year, month, day)

    # 4. Process relative time (3 hours ago)
    elif 'hours ago' in text:
        hours = int(re.search(r'\d+', text).group())
        return now - timedelta(hours=hours)
    elif 'minutes ago' in text:
        mins = int(re.search(r'\d+', text).group())
        return now - timedelta(minutes=mins)

    return None  # Non-current year or invalid time

def generate_time_description(time_obj: datetime) -> str:
    """Generate colloquial time description"""
    delta = datetime.now() - time_obj
    if delta.days == 0:
        if delta.seconds >= 3600:
            return f"{delta.seconds//3600} hours ago"
        return f"{delta.seconds//60} minutes ago"
    return f"{time_obj.month}month{time_obj.day}"

async def fetch_duckduckgo_results(query: str) -> list:
    """Get only DuckDuckGo search results for this year"""
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://duckduckgo.com/html/?q={quote(query)}"

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            soup = BeautifulSoup(await resp.text(), 'html.parser')
            valid_results = []

            for item in soup.select('.result'):
                title_elem = item.select_one('a.result__a')
                title = title_elem.get_text(strip=True) if title_elem else ""
                snippet_elem = item.select_one('a.result__snippet') or item.select_one('.result__snippet')
                content = snippet_elem.get_text(strip=True) if snippet_elem else ""

                if not content:
                    full_text = item.get_text(separator=' ', strip=True)
                    content = full_text.replace(title, "", 1).strip()

                if time_obj := extract_and_validate_time(f"{title} {content}"):
                    pass
                else:
                    time_obj = datetime.now()

                clean_text = re.sub(r'\$\$.*?\$\$|【.*?】', '', f"{title} {content}")
                time_desc = generate_time_description(time_obj)
                voice_text = f"{clean_text}（{time_desc}）"

                valid_results.append({
                    "time": time_obj,
                    "text": voice_text,
                    "raw": f"{title}\n{content}"
                })
            return sorted(valid_results, key=lambda x: x["time"], reverse=True)

@mcp.tool()
async def websitesearch(query_text: str) -> list:
    """Return only the latest 20 results of this year"""
    results = await fetch_duckduckgo_results(query_text)
    return {
        "success": bool(results),
        "result": [item["text"] for item in results[:20]]
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")

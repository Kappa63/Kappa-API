from typing import Literal, Optional
from bs4 import BeautifulSoup
import requests


def _getRoyaNews(searchWord: str) -> tuple[dict[str, str|list], int]:
    """
    Webscrapes "https://en.royanews.tv" for the latest news.
    
    Parameters:
        ``searchWord`` (``str``): Keyword to use for search
    Returns:
        ``tuple``:
            Containing:
            - dict keys: `id`, `title`, `page`, `date`, `images`, `body`
            - int: HTTP status code
    """

    BASE_URL = "https://en.royanews.tv"

    PAGE_EXT = "/section/1"

    res = requests.get(BASE_URL+PAGE_EXT)
    if not (200 <= res.status_code < 300):
        return {}, res.status_code
    sp = BeautifulSoup(res.text, "html.parser")

    flag = False
    for div in sp.find_all("div", class_="news_card_small_title"):
        if not (aTag := div.find("a")): # type: ignore
            continue
        aText = aTag.get_text(strip=True) # type: ignore
        if searchWord.lower() in aText.lower():
            flag = True

            wp = BASE_URL + aTag.get("href", "") # type: ignore

            newsRes = requests.get(wp)
            newsSp = BeautifulSoup(newsRes.text, "html.parser")

            newsDate = ""
            if dataDiv := newsSp.find("div", class_="pup_date_news"):
                for part in dataDiv.contents: # type: ignore
                    if isinstance(part, str) and part.strip():
                        newsDate = part.strip()

            newsImages = []
            if dataDiv := newsSp.find("div", class_="news_image"):
                for img in dataDiv.find_all("img"): # type: ignore
                    newsImages.append(img.get("src")) # type: ignore

            newsBody = ""
            if dataDiv := newsSp.find("div", class_="Newsbody"):
                newsBody = " ".join(p.get_text(strip=True) for p in dataDiv.find_all('p')) # type: ignore
            
            break
    
    if flag:
        return {"id":wp.split("/")[-1], "page":wp,
                "title":aText, "date":newsDate, "images":newsImages,
                "body":newsBody}, 200
    return {}, 204
        
def _find1337xTorrents(torrentName: str, time: Optional[Literal["asc", "desc"]] = None) -> tuple[list[dict[str, str]], int]:
    """
    Webscrapes "https://1337x.to" for a torrent
    
    Parameters:
        ``torrentName`` (``str``): Keyword to use for search
        ``time`` (`asc` or `desc`): How to sort by time. Can be None for no sorting.
    Returns:
        ``tuple``:
            Containing:
            - set of dicts with keys: `name`, `url`, `seeders`, `leechers`, `time`, `size`
            - int: HTTP status code
    """

    BASE_URL = "https://1337x.to"

    TIME_SORT = {"asc": "time/asc/", "desc": "time/desc/"}

    PAGE_EXTS = [f"/{'sort-' if time else ''}category-search/"+torrentName.replace(" ", "+")+f"/Movies/{TIME_SORT.get(time,'')}1/", # type: ignore
                 f"/{'sort-' if time else ''}category-search/"+torrentName.replace(" ", "+")+f"/TV/{TIME_SORT.get(time,'')}1/"] # type: ignore
    
    found = []

    for EXT in PAGE_EXTS:
        print(BASE_URL+EXT)
        res = requests.get(BASE_URL+EXT)
        if not (200 <= res.status_code < 300):
            return [], res.status_code
        
        sp = BeautifulSoup(res.text, "html.parser")

        if not (tbl := sp.find("table", class_="table-list")):
            continue

        for row in tbl.find_all("tr")[1:11]: # type: ignore
            col1 = row.find("td", class_="name").select("a:not(.icon)")[0] # type: ignore

            data = {"name": col1.get_text(strip=True), "url": BASE_URL+col1.get("href", ""), # type: ignore
                        "seeders": row.find("td", class_="seeds").get_text(strip=True), "leechers": row.find("td", class_="leeches").get_text(strip=True), # type: ignore
                        "time": row.find("td", class_="coll-date").get_text(strip=True), "size": row.find("td", class_="size").get_text(strip=True)} # type: ignore

            if data not in found: found.append(data)
    
    if found: 
        return found, 200

    return [], 204
from bs4 import BeautifulSoup
import requests


def getRoyaNews(searchWord: str) -> tuple[dict[str, str|list], int]:
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
        aTag = div.find("a") # type: ignore
        if not aTag:
            continue
        aText = aTag.get_text(strip=True) # type: ignore
        if searchWord.lower() in aText.lower():
            flag = True

            wp = BASE_URL + aTag.get("href", "") # type: ignore

            newsRes = requests.get(wp)
            newsSp = BeautifulSoup(newsRes.text, "html.parser")

            dataDiv = newsSp.find("div", class_="pup_date_news")
            newsDate = ""
            if dataDiv:
                for part in dataDiv.contents: # type: ignore
                    if isinstance(part, str) and part.strip():
                        newsDate = part.strip()

            dataDiv = newsSp.find("div", class_="news_image")
            newsImages = []
            if dataDiv:
                for img in dataDiv.find_all("img"): # type: ignore
                    newsImages.append(img.get("src")) # type: ignore

            dataDiv = newsSp.find("div", class_="Newsbody")
            newsBody = ""
            if dataDiv:
                newsBody = " ".join(p.get_text(strip=True) for p in dataDiv.find_all('p')) # type: ignore
            
            break
    
    if flag:
        return {"id":wp.split("/")[-1], "page":wp,
                "title":aText, "date":newsDate, "images":newsImages,
                "body":newsBody}, 200
    return {}, 204
        

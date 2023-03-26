from fastapi import FastAPI
from requests_html import AsyncHTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
import time

app = FastAPI()


def clean_float(f):
    return int(f) if float(f) == int(f) else float(f)


@app.get("/manga")
async def manga():
    session = AsyncHTMLSession()
    bookmark = {'id': 2, 'link': 'https://manga4life.com/manga/A-Rank-Party-wo-Ridatsu-Shita-Ore-wa', 'chapter': 43}
    r = await session.get(bookmark['link'])
    xml = r.html.find('link[title="RSS Feed"]', first=True).attrs['href']
    xmlr = await session.get(xml)
    chapters = [i.text.split('\n') for i in xmlr.html.find("item")]
    idx = chapters[0][0].lower().find('chapter ')
    olderChapters = [c for c in chapters if float(c[0][idx+8:]) > bookmark['chapter']]
    if len(olderChapters) == 0:
        return {'id': bookmark['id'], 'link': bookmark['link'], 'chapter': bookmark['chapter'], 'num_chapters': 0}
    return {'id': bookmark['id'], 'link': min(olderChapters, key=lambda a: float(a[0][idx+8:]))[1], 'chapter': clean_float(max(chapters, key=lambda a: float(a[0][idx+8:]))[0][idx+8:]), 'num_chapters': len(olderChapters)}


@app.get("/nitro")
def nitro():
    bookmark = {'id': 1, 'link': 'https://www.nitroscans.com/series/i-stole-the-number-one-rankers-soul/', 'chapter': 14}
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get(bookmark['link'])
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    chapters = [a for a in soup.findAll('a') if 'chapter ' in a.text.lower()]
    olderChapters = [a for a in chapters if float(a.text.strip()[8:]) > bookmark['chapter']]
    if len(olderChapters) == 0:
        return {'id': bookmark['id'], 'link': bookmark['link'], 'chapter': bookmark['chapter'], 'num_chapters': 0}
    return {
            'id': bookmark['id'], 
            'link': min(olderChapters, key=lambda a: float(a.text.strip()[8:]), default=bookmark['link']).attrs['href'], 
            'chapter': clean_float(max(chapters, key=lambda a: float(a.text.strip()[8:])).text.strip()[8:]), 
            'num_chapters': len(olderChapters)
        }
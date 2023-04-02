from fastapi import FastAPI
from requests_html import AsyncHTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
from arsenic import get_session, services, browsers
import asyncio, logging, structlog


app = FastAPI()

def set_arsenic_log_level(level = logging.ERROR):
    logger = logging.getLogger('arsenic')

    def logger_factory():
        return logger

    structlog.configure(logger_factory=logger_factory)
    logger.setLevel(level)

set_arsenic_log_level()


def clean_float(f):
    return int(f) if float(f) == int(f) else float(f)


async def manga(session, bookmark):
    r = await session.get(bookmark['link'])
    print(f'query 1 for {bookmark["link"]}')
    xml = r.html.find('link[title="RSS Feed"]', first=True).attrs['href']
    xmlr = await session.get(xml)
    print(f'query 2 for {bookmark["link"]}')
    chapters = [i.text.split('\n') for i in xmlr.html.find("item")]
    idx = chapters[0][0].lower().find('chapter ')
    olderChapters = [c for c in chapters if float(c[0][idx+8:]) > bookmark['chapter']]
    print(f'finish for {bookmark["link"]}')
    if len(olderChapters) == 0:
        return {'id': bookmark['id'], 'link': bookmark['link'], 'chapter': bookmark['chapter'], 'num_chapters': 0}
    return {'id': bookmark['id'], 'link': min(olderChapters, key=lambda a: float(a[0][idx+8:]))[1], 'chapter': clean_float(max(chapters, key=lambda a: float(a[0][idx+8:]))[0][idx+8:]), 'num_chapters': len(olderChapters)}

@app.get('/mangas')
async def mangas():
    session = AsyncHTMLSession()
    bookmarks = [
        {'id': 10, 'link': 'https://manga4life.com/manga/A-Rank-Party-wo-Ridatsu-Shita-Ore-wa', 'chapter': 43},
        {'id': 11, 'link': 'https://manga4life.com/manga/Maou-sama-No-Machizukuri', 'chapter': 19},
        {'id': 12, 'link': 'https://manga4life.com/manga/Isekai-Nonbiri-Nouka', 'chapter': 0},
        {'id': 13, 'link': 'https://manga4life.com/manga/Tensei-Shitara-Slime-Datta-Ken', 'chapter': 104},
        {'id': 14, 'link': 'https://manga4life.com/manga/Chronicles-of-Heavenly-Demon', 'chapter': 117},
        {'id': 15, 'link': 'https://manga4life.com/manga/Overgeared', 'chapter': 167},
        {'id': 16, 'link': 'https://manga4life.com/manga/The-Greatest-Estate-Developer', 'chapter': 69},
        {'id': 17, 'link': 'https://manga4life.com/manga/Tales-Of-Demons-And-Gods', 'chapter': 423},
        {'id': 18, 'link': 'https://manga4life.com/manga/Heavenly-Demon-Instructor', 'chapter': 89},
        {'id': 19, 'link': 'https://manga4life.com/manga/Jujutsu-Kaisen', 'chapter': 100},
    ]

    return await asyncio.gather(*[manga(session, bookmark) for bookmark in bookmarks])


async def nitro(bookmark):
    service = services.Chromedriver(binary='./chromedriver')
    browser = browsers.Chrome()
    browser.capabilities = {
        "goog:chromeOptions": {"args": ["--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]}
    }
    async with get_session(service, browser) as session:
        await session.get(bookmark['link'])
        chapters = await session.get_elements("ul li.wp-manga-chapter a")
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # chapters = [a for a in soup.findAll('a') if 'chapter ' in a.text.lower()]
    olderChapters = [a for a in chapters if float(a.text.strip()[8:]) > bookmark['chapter']]
    if len(olderChapters) == 0:
        return {'id': bookmark['id'], 'link': bookmark['link'], 'chapter': bookmark['chapter'], 'num_chapters': 0}
    return {
            'id': bookmark['id'], 
            'link': min(olderChapters, key=lambda a: float(a.text.strip()[8:]), default=bookmark['link']).attrs['href'], 
            'chapter': clean_float(max(chapters, key=lambda a: float(a.text.strip()[8:])).text.strip()[8:]), 
            'num_chapters': len(olderChapters)
        }


@app.get("/nitros")
async def nitros():
    bookmarks = [
        {'id': 1, 'link': 'https://www.nitroscans.com/series/i-stole-the-number-one-rankers-soul/', 'chapter': 14},
        {'id': 2, 'link': 'https://nitroscans.com/series/demonic-emperor/', 'chapter': 350},
        {'id': 3, 'link': 'https://nitroscans.com/series/the-return-of-the-prodigious-swordmaster/', 'chapter': 5},
        {'id': 4, 'link': 'https://nitroscans.com/series/the-golden-lion-king/', 'chapter': 0},
        {'id': 5, 'link': 'https://nitroscans.com/series/gangho-apocalypse/', 'chapter': 5},
        {'id': 6, 'link': 'https://nitroscans.com/series/the-great-demon-king/', 'chapter': 2},
        {'id': 7, 'link': 'https://nitroscans.com/series/martial-peak/', 'chapter': 3000},
        {'id': 8, 'link': 'https://nitroscans.com/series/top-tier-providence-secretly-cultivate-for-a-thousand-years/', 'chapter': 90},
        {'id': 9, 'link': 'https://nitroscans.com/series/earthlings-are-insane/', 'chapter': 121},
    ]
    results = []
    for bookmark in bookmarks:
        result = await nitro(bookmark)
        results.append(result)

    return results
    

# https://medium.com/analytics-vidhya/asynchronous-web-scraping-101-fetching-multiple-urls-using-arsenic-ec2c2404ecb4
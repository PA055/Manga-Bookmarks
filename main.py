from fastapi import FastAPI
from requests_html import AsyncHTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
from arsenic import get_session, services, browsers
app = FastAPI()


def clean_float(f):
    return int(f) if float(f) == int(f) else float(f)


async def manga(bookmark):
    session = AsyncHTMLSession()
    r = await session.get(bookmark['link'])
    xml = r.html.find('link[title="RSS Feed"]', first=True).attrs['href']
    xmlr = await session.get(xml)
    chapters = [i.text.split('\n') for i in xmlr.html.find("item")]
    idx = chapters[0][0].lower().find('chapter ')
    olderChapters = [c for c in chapters if float(c[0][idx+8:]) > bookmark['chapter']]
    if len(olderChapters) == 0:
        return {'id': bookmark['id'], 'link': bookmark['link'], 'chapter': bookmark['chapter'], 'num_chapters': 0}
    return {'id': bookmark['id'], 'link': min(olderChapters, key=lambda a: float(a[0][idx+8:]))[1], 'chapter': clean_float(max(chapters, key=lambda a: float(a[0][idx+8:]))[0][idx+8:]), 'num_chapters': len(olderChapters)}

@app.get('/mangas')
async def mangas():
    bookmarks = [
        {'id': 10, 'link': 'https://manga4life.com/manga/A-Rank-Party-wo-Ridatsu-Shita-Ore-wa', 'chapter': 43},
        {'id': 11, 'link': 'https://manga4life.com/manga/Maou-sama-No-Machizukuri', 'chapter': 19},
        {'id': 12, 'link': '', 'chapter': 0},
        {'id': 13, 'link': '', 'chapter': 0},
        {'id': 14, 'link': '', 'chapter': 0},
        {'id': 15, 'link': '', 'chapter': 0},
        {'id': 16, 'link': '', 'chapter': 0},
        {'id': 17, 'link': '', 'chapter': 0},
        {'id': 18, 'link': '', 'chapter': 0},
        {'id': 19, 'link': '', 'chapter': 0},
    ]

    results = []
    for bookmark in bookmarks:
        results.append(await manga(bookmark))

    return results


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
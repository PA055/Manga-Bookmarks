from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from requests_html import AsyncHTMLSession
from requests.structures import CaseInsensitiveDict
import json, asyncio

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
app = FastAPI()
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def clean_float(f):
    return int(f) if float(f) == int(f) else float(f)

async def nitro(session, bookmark):
    r = await session.get(bookmark['link'])
    # print(Fore.GREEN + f'query 1 for {bookmark["link"]}' + Fore.RESET)
    manga = json.loads(r.html.find('script#wp-manga-js-extra', first=True).search('var manga = {};')[0].replace('\\', ''))
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["Content-Length"] = "0"
    chr = await session.post(manga['base_url'] + 'ajax/chapters/', headers=headers)
    # print(Fore.GREEN + f'query 2 for {bookmark["link"]}' + Fore.RESET)
    chapters = [c for c in chr.html.find('li.wp-manga-chapter a') if 'chapter ' in c.text.lower().strip()]
    # print(*["'" + c.text + "'" for c in chapters], sep=', ')
    olderChapters = [c for c in chapters if float(c.text.lower().strip()[8:]) > bookmark["chapter"]]
    # print(Fore.YELLOW + f'finish for {bookmark["link"]}' + Fore.RESET)
    if len(olderChapters) == 0:
            return {'id': bookmark['id'], 'link': bookmark['link'], 'chapter': bookmark['chapter'], 'num_chapters': 0}
    return {'id': bookmark['id'], 'link': min(olderChapters, key=lambda a: float(a.text[8:])).attrs['href'], 'chapter': clean_float(max(chapters, key=lambda a: float(a.text[8:])).text[8:]), 'num_chapters': len(olderChapters)}

@app.get('/api/nitros')
async def nitros():
    session = AsyncHTMLSession()
    bookmarks = [
        {'id': 1, 'link': 'https://www.nitroscans.com/series/i-stole-the-number-one-rankers-soul/', 'chapter': 14},
        {'id': 2, 'link': 'https://nitroscans.com/series/demonic-emperor/', 'chapter': 350},
        {'id': 3, 'link': 'https://nitroscans.com/series/the-return-of-the-prodigious-swordmaster/', 'chapter': 5},
        {'id': 4, 'link': 'https://nitroscans.com/series/the-golden-lion-king/', 'chapter': 0},
        {'id': 5, 'link': 'https://nitroscans.com/series/gangho-apocalypse/', 'chapter': 5},
        {'id': 6, 'link': 'https://nitroscans.com/series/the-great-demon-king/', 'chapter': 2},
        # {'id': 7, 'link': 'https://nitroscans.com/series/martial-peak/', 'chapter': 3000},
        {'id': 8, 'link': 'https://nitroscans.com/series/top-tier-providence-secretly-cultivate-for-a-thousand-years/', 'chapter': 90},
        {'id': 9, 'link': 'https://nitroscans.com/series/earthlings-are-insane/', 'chapter': 121},
    ]

    return await asyncio.gather(*[nitro(session, bookmark) for bookmark in bookmarks])

async def manga(session, bookmark):
    r = await session.get(bookmark['link'])
    # print(Fore.GREEN + f'query 1 for {bookmark["link"]}' + Fore.RESET)
    xml = r.html.find('link[title="RSS Feed"]', first=True).attrs['href']
    xmlr = await session.get(xml)
    # print(Fore.GREEN + f'query 2 for {bookmark["link"]}' + Fore.RESET)
    chapters = [i.text.split('\n') for i in xmlr.html.find("item") if "chapter " in i.text.split('\n')[0].lower().strip()]
    # print(*["'" + c[0] + "'" for c in chapters], sep=', ')
    idx = chapters[0][0].lower().find('chapter ')
    olderChapters = [c for c in chapters if float(c[0][idx+8:]) > bookmark['chapter']]
    # print(Fore.YELLOW + f'finish for {bookmark["link"]}' + Fore.RESET)
    if len(olderChapters) == 0:
        return {'id': bookmark['id'], 'link': bookmark['link'], 'chapter': bookmark['chapter'], 'num_chapters': 0}
    return {'id': bookmark['id'], 'link': min(olderChapters, key=lambda a: float(a[0][idx+8:]))[1], 'chapter': clean_float(max(chapters, key=lambda a: float(a[0][idx+8:]))[0][idx+8:]), 'num_chapters': len(olderChapters)}

@app.get('/api/mangas')
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

@app.get('/api/all')
async def main():
    session = AsyncHTMLSession()
    bookmarks = [
        {'id': 7, 'link': 'https://nitroscans.com/series/martial-peak/', 'chapter': 3000},
        {'id': 16, 'link': 'https://manga4life.com/manga/The-Greatest-Estate-Developer', 'chapter': 69},
        {'id': 2, 'link': 'https://nitroscans.com/series/demonic-emperor/', 'chapter': 350},
        {'id': 18, 'link': 'https://manga4life.com/manga/Heavenly-Demon-Instructor', 'chapter': 89},
        {'id': 4, 'link': 'https://nitroscans.com/series/the-golden-lion-king/', 'chapter': 0},
        {'id': 19, 'link': 'https://manga4life.com/manga/Jujutsu-Kaisen', 'chapter': 100},
        {'id': 6, 'link': 'https://nitroscans.com/series/the-great-demon-king/', 'chapter': 2},
        {'id': 10, 'link': 'https://manga4life.com/manga/A-Rank-Party-wo-Ridatsu-Shita-Ore-wa', 'chapter': 43},
        {'id': 8, 'link': 'https://nitroscans.com/series/top-tier-providence-secretly-cultivate-for-a-thousand-years/', 'chapter': 90},
        {'id': 15, 'link': 'https://manga4life.com/manga/Overgeared', 'chapter': 167},
        {'id': 11, 'link': 'https://manga4life.com/manga/Maou-sama-No-Machizukuri', 'chapter': 19},
        {'id': 9, 'link': 'https://nitroscans.com/series/earthlings-are-insane/', 'chapter': 121},
        {'id': 17, 'link': 'https://manga4life.com/manga/Tales-Of-Demons-And-Gods', 'chapter': 423},
        {'id': 12, 'link': 'https://manga4life.com/manga/Isekai-Nonbiri-Nouka', 'chapter': 0},
        {'id': 3, 'link': 'https://nitroscans.com/series/the-return-of-the-prodigious-swordmaster/', 'chapter': 5},
        {'id': 5, 'link': 'https://nitroscans.com/series/gangho-apocalypse/', 'chapter': 5},
        {'id': 14, 'link': 'https://manga4life.com/manga/Chronicles-of-Heavenly-Demon', 'chapter': 117},
        {'id': 1, 'link': 'https://www.nitroscans.com/series/i-stole-the-number-one-rankers-soul/', 'chapter': 14},
        {'id': 13, 'link': 'https://manga4life.com/manga/Tensei-Shitara-Slime-Datta-Ken', 'chapter': 104},
    ]

    return await asyncio.gather(*(
        manga(session, bookmark) if 'https://manga4life.com'  in bookmark['link'] else (
        nitro(session, bookmark) if 'https://nitroscans.com'  in bookmark['link'] else (
        nitro(session, bookmark)))
        for bookmark in bookmarks))


@app.get('/api/filter/<h>')
def filter(h):
     return {}
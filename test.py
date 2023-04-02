
from requests_html import AsyncHTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio, logging, structlog
from arsenic import get_session, services, browsers
from colorama import Fore

def set_arsenic_log_level(level = logging.ERROR):
    logger = logging.getLogger('arsenic')

    def logger_factory():
        return logger

    structlog.configure(logger_factory=logger_factory)
    logger.setLevel(level)

async def nitro(bookmark):
    service = services.Chromedriver(binary='./chromedriver')
    browser = browsers.Chrome()
    browser.capabilities = {
        "goog:chromeOptions": {"args": ["--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]}
    }
    async with get_session(service, browser) as session:
        await session.get(bookmark['link'])
        await session.wait_for_element(20, 'ul li.wp-manga-chapter a')
        chapters = await session.get_elements("ul li.wp-manga-chapter a")

        link = bookmark['link']
        latest_chapter = bookmark['chapter']
        num_chapters = 0

        for chapter in chapters:
            chapter_text = await chapter.get_text()
            try:
                chapter_num = float(chapter_text.strip()[8:])
            except ValueError:
                chapter_link = await chapter.get_attribute('href')
                chapter_num = float(chapter_link.split('/chapter-')[-1][:-1].replace('-', '.'))

            if chapter_num > bookmark['chapter']:
                if num_chapters == 0:
                    link = await chapter.get_attribute('href')
                num_chapters += 1
            else:
                continue

            if chapter_num > latest_chapter:
                latest_chapter = chapter_num


        return {
                'id': bookmark['id'], 
                'link': link, 
                'chapter': latest_chapter,
                'num_chapters': num_chapters, 
            }


async def run():
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
    results = []
    for bookmark in bookmarks:
        results.append(asyncio.create_task(nitro(bookmark)))

    list_of_results = await asyncio.gather(*results)
    return list(results)

if __name__ == '__main__':
    set_arsenic_log_level()
    df = asyncio.run(run())
    for result in df:
        print(result)


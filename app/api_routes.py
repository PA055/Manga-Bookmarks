from fastapi import Depends
from requests_html import AsyncHTMLSession
from requests.structures import CaseInsensitiveDict
from sqlalchemy.orm import Session
import asyncio, app
from app import api_models, helper


async def nitro(session, bookmark):
    # r = await session.get(bookmark.link)
    # print(Fore.GREEN + f'query 1 for {bookmark.link}' + Fore.RESET)
    # manga = json.loads(r.html.find('script#wp-manga-js-extra', first=True).search('var manga = {};')[0].replace('\\', ''))
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["Content-Length"] = "0"
    # chr = await session.post(manga['base_url'] + 'ajax/chapters/', headers=headers)
    chr = await session.post(bookmark.link + 'ajax/chapters/', headers=headers)
    # print(Fore.GREEN + f'query 2 for {bookmark.link}' + Fore.RESET)
    chapters = [c for c in chr.html.find('li.wp-manga-chapter a') if 'chapter ' in c.text.lower().strip()]
    # print(*["'" + c.text + "'" for c in chapters], sep=', ')
    olderChapters = [c for c in chapters if float(c.text.lower().strip()[8:]) > bookmark.chapter]
    # print(Fore.YELLOW + f'finish for {bookmark.link}' + Fore.RESET)
    if len(olderChapters) == 0:
            return {'id': bookmark.id, 'link': bookmark.link, 'chapter': bookmark.chapter, 'num_chapters': 0}
    return {'id': bookmark.id, 'link': min(olderChapters, key=lambda a: float(a.text[8:])).attrs['href'], 'chapter': helper.clean_float(max(chapters, key=lambda a: float(a.text[8:])).text[8:]), 'num_chapters': len(olderChapters)}

async def manga(session, bookmark):
    r = await session.get(bookmark.link)
    # print(Fore.GREEN + f'query 1 for {bookmark.link}' + Fore.RESET)
    xml = r.html.find('link[title="RSS Feed"]', first=True).attrs['href']
    xmlr = await session.get(xml)
    # print(Fore.GREEN + f'query 2 for {bookmark.link}' + Fore.RESET)
    chapters = [i.text.split('\n') for i in xmlr.html.find("item") if "chapter " in i.text.split('\n')[0].lower().strip()]
    # print(*["'" + c[0] + "'" for c in chapters], sep=', ')
    idx = chapters[0][0].lower().find('chapter ')
    olderChapters = [c for c in chapters if float(c[0][idx+8:]) > bookmark.chapter]
    # print(Fore.YELLOW + f'finish for {bookmark.link}' + Fore.RESET)
    if len(olderChapters) == 0:
        return {'id': bookmark.id, 'link': bookmark.link, 'chapter': bookmark.chapter, 'num_chapters': 0}
    return {'id': bookmark.id, 'link': min(olderChapters, key=lambda a: float(a[0][idx+8:]))[1], 'chapter': helper.clean_float(max(chapters, key=lambda a: float(a[0][idx+8:]))[0][idx+8:]), 'num_chapters': len(olderChapters)}

@app.api_app.get('/api/all')
async def main(db: Session = Depends(app.get_db)):
    session = AsyncHTMLSession()
    bookmarks = api_models.get_all_bookmarks(db)

    results = await asyncio.gather(*(
        manga(session, bookmark) if 'https://manga4life.com'  in bookmark.link else (
        nitro(session, bookmark) if 'https://nitroscans.com'  in bookmark.link else (
        nitro(session, bookmark)))
        for bookmark in bookmarks))

    # return results

    updates = {}
    for bookmark in results:
        updates[bookmark['id']] = bookmark

    return [{
        'id': i.id,
        'mname': i.mname,
        'link': i.link,
        'chapter': helper.clean_float(i.chapter),
        'latest': helper.clean_float(updates[i.id]['chapter']),
        'latest_link': updates[i.id]['link'],
        'num_new_chapters': updates[i.id]['num_chapters']
    } for i in bookmarks]

from fastapi import Depends
from requests_html import AsyncHTMLSession
from requests.structures import CaseInsensitiveDict
from sqlalchemy.orm import Session
import asyncio, app, traceback, time
from app import api_models, helper
from config import Settings

def list_rindex(li, x, key=lambda v: v):
    for i in (range(len(li))):
        if key(li[i]) == x:
            return i
    raise ValueError("{} is not in list".format(x))
    
async def fallback(bookmark):
    return {
        'id': bookmark.id,
        'link': bookmark.link,
        'chapter': '??',
        'num_chapters': -1
    }

async def mpark(session, bookmark):
    try:
        link = bookmark.link
        if not Settings.USE_ORIGINAL:
            if not bookmark.link.startswith(Settings.MANGAPARK_WEBSITE_HOST):
                host = helper.get_host(bookmark.link)
                link = Settings.MANGAPARK_WEBSITE_HOST + bookmark.link[len(host):]
            else:
                link = bookmark.link

        r = await session.get(link)
        chapters = [c for c in r.html.find('div.scrollable-panel > div > div > div > a')]
        olderChapters = [c for c in chapters if helper.get_numbers(c.text) > bookmark.chapter]

        # with open('./debug/mangapark/' + bookmark.mname + '.txt', 'w') as f:
        #     f.write(str([[helper.get_numbers(chapter.text[:25]), chapter.attrs['href']] for chapter in chapters]).replace('[', '\n    ['))

        if len(olderChapters) == 0:
            return {
                'id': bookmark.id,
                'link': link,
                'chapter': bookmark.chapter,
                'num_chapters': 0
            }

        return {
            'id': bookmark.id,
            'link': Settings.MANGAPARK_WEBSITE_HOST + min(olderChapters, key=lambda a: helper.get_numbers(a.text[:25])).attrs['href'],
            'chapter': helper.clean_float(helper.get_numbers(max(chapters, key=lambda a: helper.get_numbers(a.text[:25])).text[:25])),
            'num_chapters': len(olderChapters)
        }
    except Exception:
        print('-'*50)
        print(bookmark.mname)
        traceback.print_exc()
        print('-'*50)
        return await fallback(bookmark)

async def asura(session, bookmark):
    try:
        link = bookmark.link
        if not Settings.USE_ORIGINAL:
            if not bookmark.link.startswith(Settings.ASURASCANS_WEBSITE_HOST):
                host = helper.get_host(bookmark.link)
                link = Settings.ASURASCANS_WEBSITE_HOST + bookmark.link[len(host):]
            else:
                link = bookmark.link
                
        if link[28:link.index('-')] != Settings.ASURASCANS_WEBSITE_NUMBER and False:
            link = link[:28] + Settings.ASURASCANS_WEBSITE_NUMBER + link[link.index('-'):]
            
        r = await session.get(link)
        chapters = [c for c in r.html.find('ul.clstyle a')]
        olderChapters = [c for c in chapters if helper.get_numbers(c.text[:25]) > bookmark.chapter]
        
        # with open('./debug/asurascans/' + bookmark.mname + '.txt', 'w') as f:
        #     f.write(str([[helper.get_numbers(chapter.text[:25]), chapter.attrs['href']] for chapter in chapters]).replace('[', '\n    ['))
        
        if len(olderChapters) == 0:
            return {
                'id': bookmark.id,
                'link': link,
                'chapter': bookmark.chapter,
                'num_chapters': 0
            }

        return {
            'id': bookmark.id,
            'link': min(olderChapters, key=lambda a: helper.get_numbers(a.text[:25])).attrs['href'],
            'chapter': helper.clean_float(helper.get_numbers(max(chapters, key=lambda a: helper.get_numbers(a.text[:25])).text[:25])),
            'num_chapters': len(olderChapters)
        }
    except Exception:
        print('-'*50)
        print(bookmark.mname)
        traceback.print_exc()
        print('-'*50)
        return await fallback(bookmark)
    
async def nitro(session, bookmark):
    try:
        link = bookmark.link
        if not Settings.USE_ORIGINAL:
            if not bookmark.link.startswith(Settings.NITROSCANS_WEBSITE_HOST):
                host = helper.get_host(bookmark.link)
                link = Settings.NITROSCANS_WEBSITE_HOST + bookmark.link[len(host):]
            else:
                link = bookmark.link
        
        if Settings.REPLACE_SERIES_WITH_MANGAS:
            l = link.split('/')
            l[3] = 'mangas'
            link = '/'.join(l)
        
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = "0"
        chr = await session.post(link + 'ajax/chapters/', headers=headers)
        
        chapters = [c for c in chr.html.find('li.wp-manga-chapter a')]
        olderChapters = [c for c in chapters if helper.get_chapter_number(c.text) > bookmark.chapter]
 
        # with open('./debug/nitroscans/' + bookmark.mname + '.txt', 'w') as f:
        #     f.write(str([[helper.get_chapter_number(chapter.text), chapter.attrs['href']] for chapter in chapters]).replace('[', '\n    ['))

        if len(olderChapters) == 0:
                return {
                    'id': bookmark.id,
                    'link': link,
                    'chapter': bookmark.chapter,
                    'num_chapters': 0
                }
        
        return {
            'id': bookmark.id,
            'link': min(olderChapters, key=lambda a: helper.get_chapter_number(a.text)).attrs['href'],
            'chapter': helper.clean_float(helper.get_chapter_number(max(chapters, key=lambda a: helper.get_chapter_number(a.text)).text)),
            'num_chapters': len(olderChapters)
        }
    except Exception:
        print('-' * 50)
        print(bookmark.mname)
        traceback.print_exc()
        print('-' * 50)
        return await fallback(bookmark)

async def manga(session, bookmark):
    try:
        link = bookmark.link
        if not Settings.USE_ORIGINAL:
            if not bookmark.link.startswith(Settings.MANGA4LIFE_WEBSITE_HOST):
                host = helper.get_host(bookmark.link)
                link = Settings.MANGA4LIFE_WEBSITE_HOST + bookmark.link[len(host):]
            else:
                link = bookmark.link
        
        r = await session.get(link)
        xml = r.html.find('a[href*="rss"]', first=True).attrs['href']
        xmlr = await session.get(helper.get_host(bookmark.link) + xml)

        chapters = [i.text.split('\n') for i in xmlr.html.find("item")]
        olderChapters = chapters[:list_rindex(chapters, bookmark.chapter, key=lambda x: helper.get_chapter_number(x[0]))]
        
        # with open('./debug/manga4life/' + bookmark.mname + '.txt', 'w') as f:
        #     f.write(str([[helper.get_chapter_number(chapter[0])] + chapter for chapter in chapters]).replace('[', '\n    ['))

        if len(olderChapters) == 0:
            return {
                'id': bookmark.id,
                'link': link,
                'chapter': bookmark.chapter,
                'num_chapters': 0
            }
    
        return {
            'id': bookmark.id,
            'link': helper.clean_up(min(olderChapters, key=lambda a: helper.get_chapter_number(a[0]))[1]),
            'chapter': helper.clean_float(helper.get_chapter_number(max(chapters, key=lambda a: helper.get_chapter_number(a[0]))[0])),
            'num_chapters': len(olderChapters)
        }
    except Exception:
        print('-' * 50)
        print(bookmark.mname)
        traceback.print_exc()
        print('-' * 50)
        return await fallback(bookmark)


@app.api_app.get('/api/all')
async def main(db: Session = Depends(app.get_db)):
    session = AsyncHTMLSession()
    bookmarks = api_models.get_all_bookmarks(db)

    results = await asyncio.gather(*(
        manga(session, bookmark) if 'https://manga4life.com'  in bookmark.link else (
        nitro(session, bookmark) if 'https://nitroscans.com'  in bookmark.link else (
        nitro(session, bookmark) if 'https://darkscans.com'   in bookmark.link else (
        asura(session, bookmark) if 'https://asuracomic.net'  in bookmark.link else (
        mpark(session, bookmark) if 'https://mangapark.net'   in bookmark.link else (
        fallback(bookmark))))))
        for bookmark in bookmarks))

    updates = {}
    for bookmark in results:
        updates[bookmark['id']] = bookmark

    return [{
        'id': i.id,
        'mname': i.mname,
        'link': i.link,
        'status': i.status,
        'chapter': helper.clean_float(i.chapter),
        'latest': helper.clean_float(updates[i.id]['chapter']),
        'latest_link': updates[i.id]['link'],
        'num_new_chapters': updates[i.id]['num_chapters'],
        'site': "Manga4Life" if 'https://manga4life.com' in i.link else (
                "Nitro Scans" if 'https://nitroscans.com' in i.link else (
                "Asura Scans" if 'https://asuracomic.net' in i.link else (
                "Manga Park" if 'https://mangapark.net' in i.link else (
                "Unknown - " + helper.get_host(i.link)))))
    } for i in bookmarks]


@app.api_app.get('/api/status/{status}')
async def status(status: int, db: Session = Depends(app.get_db)):
    start = time.time()
    
    session = AsyncHTMLSession()
    bookmarks = api_models.get_bookmarks_by_status(db, status)

    results = await asyncio.gather(*(
        manga(session, bookmark) if 'https://manga4life.com'  in bookmark.link else (
        nitro(session, bookmark) if 'https://nitroscans.com'  in bookmark.link else (
        nitro(session, bookmark) if 'https://darkscans.com'   in bookmark.link else (
        asura(session, bookmark) if 'https://asuracomic.net'  in bookmark.link else (
        mpark(session, bookmark) if 'https://mangapark.net'   in bookmark.link else (
        fallback(bookmark))))))
        for bookmark in bookmarks))

    updates = {}
    for bookmark in results:
        updates[bookmark['id']] = bookmark

    print(f"Time Taken: {time.time() - start} seconds")
    
    return [{
        'id': i.id,
        'mname': i.mname,
        'link': i.link,
        'status': i.status,
        'chapter': helper.clean_float(i.chapter),
        'latest': helper.clean_float(updates[i.id]['chapter']),
        'latest_link': updates[i.id]['link'],
        'num_new_chapters': updates[i.id]['num_chapters'],
        'site': "Manga4Life" if 'https://manga4life.com' in i.link else (
                "Nitro Scans" if 'https://nitroscans.com' in i.link else (
                "Asura Scans" if 'https://asuracomic.net' in i.link else (
                "Manga Park" if 'https://mangapark.net' in i.link else (
                    "Unknown - " + helper.get_host(i.link)))))
    } for i in bookmarks]

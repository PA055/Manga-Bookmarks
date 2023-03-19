from requests_html import AsyncHTMLSession, HTMLSession
asession = AsyncHTMLSession()
session = HTMLSession()

def clean_float(f):
    return int(f) if float(f) == int(f) else float(f)

async def crawlNitroScans(bookmark):
    r = await asession.get(bookmark.link)
    await r.html.arender()
    chapters = [a for a in r.html.find('a') if 'chapter ' in a.text.lower()]
    olderChapters = [a for a in chapters if float(a.text[8:]) > bookmark.chapter]
    return {'id': bookmark.id, 'link': min(olderChapters, key=lambda a: float(a.text[8:]), default=bookmark.link).attrs['href'], 'chapter': clean_float(max(olderChapters, key=lambda a: float(a.text[8:]), default=bookmark.chapter).text[8:]), 'num_chapters': len(olderChapters)}

async def crawlManga4Life(bookmark):
    r = session.get(bookmark.link)
    xml = r.html.find('link[title="RSS Feed"]', first=True).attrs['href']
    xmlr = session.get(xml)
    chapters = [i.split('\n') for i in xmlr.html.find("item")]
    idx = chapters[0].lower().find('chapter ')
    olderChapters = [c for c in chapters if float(c[0][idx+8:]) > bookmark.chapter]
    return {'id': bookmark.id, 'link': min(olderChapters, key=lambda a: float(a[0][idx+8:]), default=bookmark.link)[1], 'chapter': clean_float(max(olderChapters, key=lambda a: float(a[0][idx+8:]), default=bookmark.chapter)[0][8:]), 'num_chapters': len(olderChapters)}


def crawl_sites(bookmarks):
    def find(id, list):
        for v in list:
            if v['id'] == id:
                return v
    results = asession.run(*[lambda: crawlNitroScans(b) for b in bookmarks if 'https://nitroscans.com' in b.link])
    nitroscans = {i.id: find(i.id, results) for i in bookmarks}

    return {i.id: {'link': i.link, 'chapter': 0, 'num chpaters': 0} for i in bookmarks}



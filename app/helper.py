def clean_float(f):
    return int(f) if float(f) == int(f) else float(f)

def crawl_sites(bookmarks):
    return {i.id: {'link': i.link, 'chapter': 0} for i in bookmarks}


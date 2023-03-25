import asyncio
from app import app, db
from app.models import *
from app.helper import *

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Bookmark': Bookmark, 'bookmarks': Bookmark.query.all(), 'crawl': crawl}

if __name__ == '__main__':
    asyncio.run(app.run_task(port=5050))

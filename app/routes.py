from quart import render_template, url_for, flash, redirect
from app.forms import *
from app.models import *
from app.helper import *
from app import app


@app.route('/')
async def index():
    bookmarks = Bookmark.query.all()
    crawled = crawl_sites(bookmarks)
    bookmarks = [{
        'mname': i.mname,
        'link': i.link,
        'chapter': clean_float(i.chapter),
        'latest': crawled[i.id]['chapter'],
        'latest_link': crawled[i.id]['link']
    } for i in bookmarks]
    return await render_template('index.html', bookmarks=bookmarks)


@app.route('/new', methods=['GET', 'POST'])
async def new():
    form = NewBookmarkForm()
    if form.validate_on_submit():
        bkmrk = Bookmark(mname=form.mname.data, link=form.link.data, chapter=form.chapter.data)
        db.session.add(bkmrk)
        db.session.commit()
        return redirect(url_for('index'))
    return await render_template('new.html', form=form)

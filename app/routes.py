from flask import render_template, url_for, flash, redirect
from app.forms import *
from app.models import *
from app.helper import *
from app import app


@app.route('/')
def index():
    bookmarks = Bookmark.query.all()
    crawled = crawl_sites(bookmarks)
    bookmarks = [{
        'mname': i.mname,
        'link': i.link,
        'chapter': clean_float(i.chapter),
        'latest': crawled[i.id]['chapter'],
        'latest_link': crawled[i.id]['link']
    } for i in bookmarks]
    return render_template('index.html', bookmarks=bookmarks)


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = NewBookmarkForm()
    if form.validate_on_submit():
        flash(f'Created new bookmark with mname={form.mname.data}, link={form.link.data}, and chapter={form.chapter.data}')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)

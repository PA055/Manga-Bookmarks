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
        'id': i.id,
        'mname': i.mname,
        'link': i.link,
        'chapter': clean_float(i.chapter),
        'latest': crawled[i.id]['chapter'],
        'latest_link': crawled[i.id]['link']
    } for i in bookmarks]

    return render_template('index.html', bookmarks=bookmarks)


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = BookmarkForm()
    if form.validate_on_submit():
        bkmrk = Bookmark(mname=form.mname.data, link=form.link.data, chapter=form.chapter.data)
        db.session.add(bkmrk)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    bkmrk = Bookmark.query.get_or_404(id)
    db.session.delete(bkmrk)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    form = BookmarkForm()
    bkmrk = Bookmark.query.get_or_404(id)
    if form.validate_on_submit():
        bkmrk.mname = form.mname.data
        bkmrk.link = form.link.data
        bkmrk.chapter = form.chapter.data
        db.session.commit()
        return redirect(url_for('index'))
    form.mname.data = bkmrk.mname
    form.link.data = bkmrk.link
    form.chapter.data = bkmrk.chapter
    return render_template('new.html', form=form)

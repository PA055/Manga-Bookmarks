from flask import render_template, url_for, flash, redirect, request
from app.forms import *
from app.models import *
from app.helper import *
from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = BookmarkForm(status = 2)
    if form.validate_on_submit():
        bkmrk = Bookmark(mname=form.mname.data, link=form.link.data, chapter=form.chapter.data, status=form.status.data)
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
        bkmrk.status = form.status.data
        db.session.commit()
        return redirect(url_for('index'))
    form.mname.data = bkmrk.mname
    form.link.data = bkmrk.link
    form.chapter.data = clean_float(bkmrk.chapter)
    form.status.data = bkmrk.status
    return render_template('new.html', form=form)


@app.route('/read/<int:id>/', methods=['GET', 'POST'])
def read(id):
    bk = Bookmark.query.get_or_404(id)
    if request.method == 'POST':
        latest = request.values.get('latest')
    else:
        latest = request.args.get('latest')

    if latest is None:
        latest = 0

    bk.chapter = latest
    db.session.commit()

    return redirect(url_for('index'))

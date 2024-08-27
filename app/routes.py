from flask import render_template, url_for, flash, redirect, request, make_response
from app.forms import *
from app.models import *
from app.helper import *
from app import app, USER_ID
import random

@app.route('/login')
def login():
    return redirect(url_for('index'))
    if not request.headers['X-Replit-User-Id']:
        return render_template('replitAuth.html')
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('id', request.headers['X-Replit-User-Id'])

    return resp

@app.route('/invalid-user')
def invalidUser():
    return redirect(url_for('index'))
    return f"Fork This repl and change the USER_ID variable in ./app/__init__.py to be your replit ID: {request.cookies.get('id')}"


@app.route('/')
def index():
    if random.randint(1, 10) == 1:
        return redirect(url_for('backup'))

    # if not request.cookies.get('id'):
    #     return redirect(url_for('login'))
    # if request.cookies.get('id') != USER_ID:
    #     return redirect(url_for('invalidUser'))

    return render_template('index.html')



@app.route('/new', methods=['GET', 'POST'])
def new():
    # if not request.cookies.get('id'):
    #     return redirect(url_for('login'))
    # if request.cookies.get('id') != USER_ID:
    #     return redirect(url_for('invalidUser'))

    form = BookmarkForm(status = 2)
    if form.validate_on_submit():
        bkmrk = Bookmark(mname=form.mname.data, link=form.link.data, chapter=form.chapter.data, status=form.status.data)
        db.session.add(bkmrk)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new.html', form=form, new=True)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    # if not request.cookies.get('id'):
    #     return redirect(url_for('login'))
    # if request.cookies.get('id') != USER_ID:
    #     return redirect(url_for('invalidUser'))

    bkmrk = Bookmark.query.get_or_404(id)
    db.session.delete(bkmrk)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # if not request.cookies.get('id'):
    #     return redirect(url_for('login'))
    # if request.cookies.get('id') != USER_ID:
    #     return redirect(url_for('invalidUser'))

    form = BookmarkForm()
    bkmrk = Bookmark.query.get_or_404(id)
    if form.validate_on_submit():
        bkmrk.mname = form.mname.data
        bkmrk.link = form.link.data
        bkmrk.chapter = form.chapter.data
        bkmrk.status = form.status.data
        db.session.commit()
        return f"<a href={url_for('index')}>Home</a>"
    form.mname.data = bkmrk.mname
    form.link.data = bkmrk.link
    form.chapter.data = clean_float(bkmrk.chapter)
    form.status.data = bkmrk.status
    return render_template('new.html', form=form, new=False)


@app.route('/read/<int:id>/', methods=['GET', 'POST'])
def read(id):
    # if not request.cookies.get('id'):
    #     return redirect(url_for('login'))
    # if request.cookies.get('id') != USER_ID:
    #     return redirect(url_for('invalidUser'))

    bk = Bookmark.query.get_or_404(id)
    if request.method == 'POST':
        latest = request.values.get('latest')
    else:
        latest = request.args.get('latest')

    if latest is None:
        latest = 0

    bk.chapter = latest
    db.session.commit()

    if random.randint(1, 10) == 1:
        return redirect(url_for('backup'))
    return "Done"


@app.route('/backup')
def backup():
    bookmarks = Bookmark.query.all()
    with open('./MangaBackup.md', 'w+') as f:
        f.writelines([
            f'[{bookmark.mname}]({bookmark.link}) -- {clean_float(bookmark.chapter)} -- {"Reading" if bookmark.status == 2 else ("On Hold" if bookmark.status == 1 else "To Read")}  \n'
            for bookmark in bookmarks
        ])

    return redirect(url_for('index'))

@app.route('/restore')
@app.route('/recover')
def restore():
    Bookmark.query.delete()
    with open('./MangaBackup.md', 'r') as f:
        bookmarkLines = f.readlines()

    # bookmarks = []
    for bookmark in bookmarkLines:
        linkedName, chapter, statusWord = bookmark.strip().split(' -- ')
        mname = linkedName[1:linkedName.rfind(']')]
        link = linkedName[linkedName.rfind('(')+1: -1]
        status = 2 if statusWord == 'Reading' else (1 if statusWord == "On Hold" else 0)

        bk = Bookmark(mname=mname, link=link, chapter=chapter, status=status)
        # bookmarks.append(bk)
        db.session.add(bk)

    db.session.commit()
    return redirect(url_for('index'))

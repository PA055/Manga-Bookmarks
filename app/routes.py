from flask import render_template, url_for, flash, redirect
from app.forms import *
from app import app


@app.route('/')
def index():
    bookmarks = [
        {
            "mname": "Loner Life in Another World",
            "link": "https://manga4life.com/manga/Hitoribocchi-no-Isekai-Kouryaku",
            "chapter": 173
        },
        {
            "mname": "Player Who Returned 10,000 Years Later",
            "link": "https://nitroscans.com/series/player-who-returned-10000-years-later/",
            "chapter": 19,
            "latest": 20,
            "latest_link": "https://nitroscans.com/series/player-who-returned-10000-years-later/chapter-20/"
        }
    ]
    return render_template('index.html', bookmarks=bookmarks)


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = NewBookmarkForm()
    if form.validate_on_submit():
        flash(f'Created new bookmark with mname={form.mname.data}, link={form.link.data}, and chapter={form.chapter.data}')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)

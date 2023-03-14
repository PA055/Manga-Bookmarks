from flask import render_template, url_for
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


@app.route('/new')
def new():
    return render_template('new.html')

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    PORT=5050
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fuhs9ehufhu4byufsabeyfu43oauwhruu4byhf8yseabfou8ib3fouybawe8f7h3j'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Settings():
    USE_ORIGINAL = False
    REPLACE_SERIES_WITH_MANGAS = False
    # NITROSCANS_WEBSITE_HOST = "https://darkscans.net"
    NITROSCANS_WEBSITE_HOST = "https://nitroscans.net"
    # NITROSCANS_WEBSITE_HOST = "https://darkscans.com"
    # NITROSCANS_WEBSITE_HOST = "https://nitroscans.com"
    # NITROSCANS_WEBSITE_HOST = "https://mangabaz.net"
    MANGA4LIFE_WEBSITE_HOST = "https://manga4life.com"
    ASURASCANS_WEBSITE_HOST = 'https://asuracomic.net'
    ASURASCANS_WEBSITE_NUMBER = '1908287720'
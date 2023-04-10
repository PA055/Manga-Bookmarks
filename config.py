import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    PORT=5050
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fuhs9ehufhu4byufsabeyfu43oauwhruu4byhf8yseabfou8ib3fouybawe8f7h3j'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

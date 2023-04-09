from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from app.api_db import Base, engine, SessionLocal

USER_ID = '3632971'

Base.metadata.create_all(bind=engine)

api_app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app import api_routes, api_models

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

api_app.mount("/", WSGIMiddleware(app))

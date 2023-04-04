from sqlalchemy import Column, Numeric, String, Integer
from sqlalchemy.orm import Session

from app.api_db import Base

class Bookmark(Base):
    __tablename__ = 'bookmark'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    mname = Column(String(256), unique=True, index=True)
    link = Column(String(512), unique=True, index=True)
    chapter = Column(Numeric(20, 2, asdecimal=False))
    status = Column(Integer, index=True, default=2)

    def __repr__(self):
        return f'{self.mname} - Chapter {self.chapter} with id={self.id}'


def get_all_bookmarks(db: Session):
    return db.query(Bookmark).all()

def edit_bookmark_by_id(db: Session, id: int, mname: str, link: str, chapter: int):
    bookmark = db.query(Bookmark).filter(Bookmark.id == id).first()
    bookmark.mname = mname
    bookmark.link = link
    bookmark.chapter = chapter
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark


def edit_bookmark_chapter(db: Session, id: int, chapter: int):
    bookmark = db.query(Bookmark).filter(Bookmark.id == id).first()
    bookmark.chapter = chapter
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark


def get_bookmarks_by_status(db: Session, status: int):
    return db.query(Bookmark).filter(Bookmark.status == status).all()

from app import db


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(256), index=True, unique=True)
    link = db.Column(db.String(512), index=True, unique=True)
    chapter = db.Column(db.DECIMAL(20, 2))
    status = db.Column(db.Integer, index=True, default=2)

    def __repr__(self):
        return f'{self.mname} - Chapter {self.chapter} with id={self.id}'

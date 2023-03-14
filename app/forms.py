from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import URLField, DecimalField
from wtforms.validators import DataRequired

class NewBookmarkForm(FlaskForm):
    mname = StringField("Manga Name")
    link = URLField("Manga Link")
    chapter = DecimalField("Current Chapter")

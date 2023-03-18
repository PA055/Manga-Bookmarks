from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, DecimalField
from wtforms.validators import DataRequired

class NewBookmarkForm(FlaskForm):
    mname = StringField("Manga Name", validators=[DataRequired()])
    link = URLField("Manga Link", validators=[DataRequired()])
    chapter = DecimalField("Current Chapter", validators=[DataRequired()])
    submit = SubmitField()

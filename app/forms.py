from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, DecimalField, SelectField
from wtforms.validators import DataRequired, InputRequired

class BookmarkForm(FlaskForm):
    mname = StringField("Manga Name", validators=[DataRequired()])
    link = URLField("Manga Link", validators=[DataRequired()])
    chapter = DecimalField("Current Chapter", validators=[InputRequired()])
    status = SelectField("Status", choices = [(2, "Reading"), (1, "On Hold"), (0, "To Read")])
    submit = SubmitField()

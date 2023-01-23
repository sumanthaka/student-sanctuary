from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class EditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=30)])
    courses = SelectField("Course", choices=["BCA", "Bsc"])
    submit = SubmitField("Save")

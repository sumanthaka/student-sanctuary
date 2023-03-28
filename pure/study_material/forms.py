from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField
from wtforms.validators import DataRequired


class Study_Material_Form(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')

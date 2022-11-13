from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, PasswordField, StringField, TextAreaField
from wtforms.validators import Email, DataRequired


class Admin_LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


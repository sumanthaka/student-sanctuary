from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, ValidationError, SelectField, PasswordField
from wtforms.validators import Email, DataRequired, EqualTo, Length

from pure.models import Student


class Student_LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Student_SignupForm(FlaskForm):
    def validate_email(self, email):
        if Student.check_existence(email.data):
            raise ValidationError('Email already exists. Please try another email.')

    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[Email(), DataRequired()])
    college = SelectField('College', choices=Student.get_colleges(), validators=[DataRequired()])
    course = SelectField('Course', choices=Student.get_all_courses())
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Register')
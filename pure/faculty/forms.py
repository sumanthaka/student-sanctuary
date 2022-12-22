from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import EmailField, StringField, SubmitField, ValidationError, SelectField, PasswordField, FileField
from wtforms.validators import Email, DataRequired, Length, EqualTo, InputRequired

from pure.models import Faculty


class Faculty_LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Faculty_SignupForm(FlaskForm):
    def validate_email(self, email):
        if Faculty.check_existence(email.data):
            raise ValidationError('Email already exists. Please try another email.')

    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[Email(), DataRequired()])
    college = SelectField('College', choices=Faculty.get_colleges())
    qualification = StringField('Qualification', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Register')


class UploadMarks_Form(FlaskForm):
    exam_name = StringField('Exam Name', validators=[DataRequired()])
    marks_file = FileField('Marks List', validators=[FileRequired(), FileAllowed(['xlsx'], 'Excel Files only!')])
    submit = SubmitField('Submit')

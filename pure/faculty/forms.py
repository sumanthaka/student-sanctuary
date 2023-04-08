from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, ValidationError, SelectField, PasswordField, DateField, \
    MultipleFileField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import Email, DataRequired, Length, EqualTo, Regexp

from pure.models import Faculty


class Faculty_LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Faculty_SignupForm(FlaskForm):
    def validate_email(self, email):
        if Faculty.check_existence(email.data):
            raise ValidationError('Email already exists. Please try another email.')

    name = StringField('Name', validators=[DataRequired(), Regexp('[A-Za-z]', message="Please give a valid name")])
    email = EmailField('Email', validators=[Email(), DataRequired()])
    college = SelectField('College', choices=Faculty.get_colleges())
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Register')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class EventForm(FlaskForm):
    title = StringField('Name', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    participants = MultiCheckboxField('Participants', choices=[])
    desc = TextAreaField('Description', validators=[DataRequired()])
    images = MultipleFileField('Images')
    submit = SubmitField('Submit')

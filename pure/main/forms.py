from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo

from pure.models import User


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[Length(min=2, max=30), DataRequired()])
    email = EmailField('Email', validators=[Email(), DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send')


class RequestResetForm(FlaskForm):
    def validate_email(self, email):
        if User.check_existence(email.data) is False:
            raise ValidationError('Email does not exist')

    email = EmailField('Email', validators=[Email(), DataRequired()])
    submit = SubmitField('reset password')


class ResetForm(FlaskForm):
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Reset')

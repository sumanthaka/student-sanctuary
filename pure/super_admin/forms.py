from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, PasswordField, StringField, TelField, FileField
from wtforms.validators import Email, DataRequired, Length


class Super_Admin_LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Create_College(FlaskForm):
    college = StringField('College', validators=[DataRequired()])
    college_mail = EmailField('College Email', validators=[Email(), DataRequired()])
    name = StringField('Admin Name', validators=[Length(min=2, max=40), DataRequired()])
    mobile = TelField('Phone Number', validators=[Length(min=10), DataRequired()])
    logo = FileField('Logo', validators=[DataRequired()])
    submit = SubmitField('Create')

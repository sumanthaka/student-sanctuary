from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectMultipleField, BooleanField, widgets
from wtforms.validators import DataRequired


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Announcement_Form(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    target_everyone = BooleanField('Everyone')
    target_students = BooleanField('Only Students')
    target_faculty = BooleanField('Only Faculty')
    target = MultiCheckboxField('Target', choices=['BCA', 'BSc'])
    desc = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Publish')

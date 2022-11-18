from flask import url_for
from flask_mail import Message

from pure import mail
from pure import app
from pure.models import User


def send_reset_mail(user):
    token = User.get_reset_token(user)
    msg = Message('Password Reset', sender='no-reply@studentsanctuary.com', recipients=[user["email"]])
    msg.body = f"""To reset password click the below link
    {url_for('main.reset_password', token=token, _external=True)}"""
    mail.send(msg)


def send_contact_mail(name, email, subject, message):
    msg = Message(subject, sender=email, recipients=[app.config['MAIL_USERNAME']])
    msg.body = f"""Name: {name}
    Sender: {email}
    Message: {message}"""
    mail.send(msg)

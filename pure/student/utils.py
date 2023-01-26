from flask import url_for
from flask_mail import Message

from pure import mail
from pure.models import User


def send_verify_mail(user):
    token = User.get_reset_token(user)
    msg = Message('Email Verification', sender='no-reply@studentsanctuary.com', recipients=[user["email"]])
    msg.body = f"""To verify your email click the below link
    {url_for('student.email_verify', token=token, _external=True)}"""
    mail.send(msg)
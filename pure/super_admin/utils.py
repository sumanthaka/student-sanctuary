import string
import random

from flask import url_for
from flask_mail import Message

from pure import mail
from pure.models import User


def generate_random_password():
    # characters to generate password from
    alphabets = list(string.ascii_letters)
    digits = list(string.digits)
    special_characters = list("!@#$%^&*()")
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

    # number of character types
    alphabets_count = 10
    digits_count = 4
    special_characters_count = 2

    # initializing the password
    password = []

    # picking random alphabets
    for i in range(alphabets_count):
        password.append(random.choice(alphabets))

    # picking random digits
    for i in range(digits_count):
        password.append(random.choice(digits))

    # picking random alphabets
    for i in range(special_characters_count):
        password.append(random.choice(special_characters))

    # shuffling the resultant password
    random.shuffle(password)

    # converting the list to string
    # printing the list
    return "".join(password)


def send_reset_mail(user):
    token = User.get_reset_token(user)
    msg = Message('Password Reset', sender='no-reply@studentsanctuary.com', recipients=[user["email"]])
    msg.body = f"""Your are now successfully registered to Student Sanctuary. 
    Thank you for choosing our platform!
    Please set your password at the given link below
    {url_for('main.reset_password', token=token, _external=True)}"""
    mail.send(msg)

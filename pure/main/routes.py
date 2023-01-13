from flask import Blueprint, render_template, send_from_directory, redirect, url_for, flash

from pure import bcrypt
from pure.main.forms import ContactForm, RequestResetForm, ResetForm
from pure.main.utils import send_reset_mail, send_contact_mail
from pure.models import User


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home_page():
    return render_template('home/home.html')


@main.route('/<path:path>')
def catch_all(path):
    return send_from_directory('static', path)


@main.route('/apply_now')
def apply_now():
    return render_template('home/apply_form.html')


@main.route('/contact_us', methods=['POST', 'GET'])
def contact_us():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        send_contact_mail(contact_form.name.data, contact_form.email.data, contact_form.subject.data,
                          contact_form.message.data)
        return redirect(url_for('main.home_page'))
    return render_template('home/contact_us.html', form=contact_form)


@main.route('/reset', methods=['POST', 'GET'])
def reset_request():
    reset_request_form = RequestResetForm()
    if reset_request_form.validate_on_submit():
        user = User.get_data(reset_request_form.email.data)
        if user is None:
            flash("Cannot change password for this user")
            return render_template('auth/reset.html', form=reset_request_form)
        send_reset_mail(user)
        return redirect(url_for('main.home_page'))
    else:
        print(reset_request_form.errors)
    return render_template('auth/reset.html', form=reset_request_form)


@main.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    user = User.verify_reset_token(token)
    password_reset_form = ResetForm()
    if user is None:
        flash("This is an invalid or expired token")
        return redirect(url_for("main.reset_request"))
    if password_reset_form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(password_reset_form.password.data)
        user.password = password_hash
        user.set_password(user.email, user.college)
        return redirect(url_for('main.home_page'))
    return render_template("auth/reset_password.html", form=password_reset_form)

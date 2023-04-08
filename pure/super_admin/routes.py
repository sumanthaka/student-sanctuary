import os

import phonenumbers as phonenumbers
from flask import Blueprint, flash, redirect, url_for, render_template, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from pure.models import Super_Admin
from pure.super_admin.forms import Super_Admin_LoginForm, Create_College
from pure.super_admin.utils import generate_random_password, send_reset_mail

super_admin = Blueprint('super_admin', __name__)


@super_admin.route('/super_admin', methods=['POST', 'GET'])
def admin_signin():
    super_admin_login_form = Super_Admin_LoginForm()
    if super_admin_login_form.validate_on_submit():
        attempted_admin = Super_Admin(super_admin_login_form.email.data)
        if attempted_admin.id == "":
            flash("Username and password does not match")
        else:
            if attempted_admin.check_password(super_admin_login_form.password.data):
                login_user(attempted_admin)
                return redirect(url_for('profile.super_admin_profile_page'))
            else:
                flash("Username password are not matching")
    return render_template('auth/login.html', form=super_admin_login_form, user="Super Admin")


@super_admin.route('/create_college', methods=['POST', 'GET'])
@login_required
def create_college():
    try:
        if current_user.user:
            abort(403)
    except AttributeError:
        create_college_form = Create_College()
        if create_college_form.validate_on_submit():
            number = create_college_form.mobile.data
            phone_number = phonenumbers.parse(number)
            if phonenumbers.is_valid_number(phone_number):
                logo = create_college_form.logo.data
                print(logo.filename)
                sec_filename = secure_filename(logo.filename)
                path = os.path.join(os.path.abspath(os.curdir), 'pure', 'static', 'college_logos', sec_filename)
                if os.path.exists(path):
                    flash("Logo already exists")
                    return redirect(url_for('super_admin.create_college'))
                logo.save(path)
                admin = Super_Admin.create_college(create_college_form.college.data, create_college_form.college_mail.data,
                                                   create_college_form.name.data, create_college_form.mobile.data,
                                                   generate_random_password(), sec_filename)
                if admin:
                    send_reset_mail(admin)
                else:
                    flash("College already exists")
                return redirect(url_for('super_admin.create_college'))

        return render_template('portal/create_college.html', form=create_college_form)


@super_admin.route('/delete_college', methods=['POST', 'GET'])
@login_required
def delete_college():
    try:
        if current_user.user:
            abort(403)
    except AttributeError:
        if request.method == 'POST':
            college = str(request.data, 'utf-8')
            Super_Admin.remove_college(college)
        return render_template('portal/delete_college.html', colleges=Super_Admin.get_colleges())


@super_admin.route('/logout', methods=['POST', 'GET'])
def logout_page():
    logout_user()
    return redirect(url_for('main.home_page'))

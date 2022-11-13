from flask import Blueprint, flash, redirect, url_for, render_template, send_from_directory
from flask_login import login_user, logout_user, login_required

from pure.faculty.forms import Faculty_LoginForm, Faculty_SignupForm
from pure.models import Faculty

faculty = Blueprint('faculty', __name__)


@faculty.route('/faculty/signin', methods=['POST', 'GET'])
def faculty_signin():
    faculty_login_form = Faculty_LoginForm()
    if faculty_login_form.validate_on_submit():
        attempted_faculty = Faculty()
        if attempted_faculty.check_existence(faculty_login_form.email.data):
            if attempted_faculty.check_password(faculty_login_form.email.data, faculty_login_form.password.data):
                attempted_faculty.set_object(faculty_login_form.email.data)
                if attempted_faculty.user == "faculty":
                    if attempted_faculty.approved:
                        login_user(attempted_faculty)
                        flash(f"Logged in!! as {attempted_faculty.name}")
                        return redirect(url_for('profile.profile_page'))
                    else:
                        flash("Admin has not approved yet")
                else:
                    flash("Username password are not matching")
        else:
            flash("Username password are not matching")
    return render_template('auth/login.html', form=faculty_login_form, user="faculty")


@faculty.route('/faculty/signup', methods=['POST', 'GET'])
def faculty_signup():
    faculty_signup_form = Faculty_SignupForm()
    if faculty_signup_form.validate_on_submit():
        student_to_create = Faculty()
        student_to_create.create_user(name=faculty_signup_form.name.data,
                                      email=faculty_signup_form.email.data,
                                      college=faculty_signup_form.college.data,
                                      qualification=faculty_signup_form.qualification.data,
                                      password=faculty_signup_form.password.data)
        return redirect(url_for('main.home_page'))
    if faculty_signup_form.errors:
        for error in faculty_signup_form.errors.values():
            flash(error)
    return render_template('auth/signup.html', form=faculty_signup_form, user="faculty")


@faculty.route('/logout', methods=['POST', 'GET'])
def logout_page():
    logout_user()
    return redirect(url_for('main.home_page'))

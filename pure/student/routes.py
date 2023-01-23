from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user

from pure.models import Student
from pure.student.forms import Student_LoginForm, Student_SignupForm

student = Blueprint('student', __name__)


@student.route('/student/signin', methods=['POST', 'GET'])
def student_signin():
    student_login_form = Student_LoginForm()
    if student_login_form.validate_on_submit():
        attempted_student = Student()
        if attempted_student.check_existence(student_login_form.email.data):
            if attempted_student.check_password(student_login_form.email.data, student_login_form.password.data):
                attempted_student.set_object(student_login_form.email.data)
                if attempted_student.user == "student":
                    login_user(attempted_student)
                    flash(f"Logged in!! as {attempted_student.name}")
                    return redirect(url_for('profile.profile_page'))
        else:
            flash("Username password are not matching")
    return render_template('auth/login.html', form=student_login_form, user="student")


@student.route('/student/signup', methods=['POST', 'GET'])
def student_signup():
    student_signup_form = Student_SignupForm()
    student_signup_form.college.choices = Student.get_colleges()
    student_signup_form.course.choices = Student.get_all_courses()
    if student_signup_form.validate_on_submit():
        student_to_create = Student()
        student_to_create.create_user(name=student_signup_form.name.data,
                                      email=student_signup_form.email.data,
                                      college=student_signup_form.college.data,
                                      course=student_signup_form.course.data,
                                      password=student_signup_form.password.data)
        return redirect(url_for('student.student_signin'))
    if student_signup_form.errors:
        for error in student_signup_form.errors.values():
            flash(error)
    return render_template('auth/signup.html', form=student_signup_form, user="student")


@student.route('/course_options/<college>', methods=['POST', 'GET'])
def course_option(college):
    college = college.replace(' ', '_')
    courses = Student.get_courses(college)
    return courses


@student.route('/logout', methods=['POST', 'GET'])
def logout_page():
    logout_user()
    return redirect(url_for('main.home_page'))

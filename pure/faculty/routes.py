import os.path
import uuid

import openpyxl as openpyxl

from flask import Blueprint, flash, redirect, url_for, render_template, send_from_directory, abort, request, send_file
from flask_login import login_user, logout_user, login_required, current_user

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
    faculty_signup_form.college.choices = Faculty.get_colleges()
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


@faculty.route('/upload_marks', methods=['POST', 'GET'])
@login_required
def upload_marks():
    if current_user.user != 'faculty':
        abort(403)
    if request.method == 'POST':
        data = request.form
        exam_info = {}
        max_marks = {}
        exam_info.update({'exam_name': data['exam_name'].lower()})
        for subject in list(data.keys())[1:]:
            max_marks.update({subject: int(data.get(subject))})
        exam_info.update({'max_marks': max_marks})
        upload_done = current_user.upload_exam(exam_info, request.files['marks_file'])
        if not upload_done[0]:
            flash(upload_done[1])
    return render_template('portal/upload_marks.html', subjects_list=current_user.get_subjects(current_user.course_faculty))


@faculty.route('/download_template', methods=['POST', 'GET'])
@login_required
def send_template():
    if request.method == 'POST':
        data = str(request.data, 'utf-8').split(',')
        if data[0] == 'add':
            filepath = os.path.join(os.path.abspath(os.curdir), 'pure', 'static', 'mark_files')
            filename = str(uuid.uuid4())
            excel_file_path = os.path.join(filepath, filename)+'.xlsx'
            book = openpyxl.Workbook()
            worksheet = book.active
            headers = ['Name', 'Email']
            subjects = current_user.get_subjects(current_user.course_faculty)
            headers += subjects
            worksheet.append(headers)
            student_list = current_user.get_course_student()
            for student in student_list:
                worksheet.append([student['name'], student['email']])
            for i in range(ord('A'), ord('A')+len(subjects)+2):
                worksheet.column_dimensions[chr(i)].width = 20
            book.save(excel_file_path)
            response = send_file(excel_file_path, as_attachment=True)
            response.set_cookie('filename', excel_file_path)
            return response
        else:
            file_path = data[1].split('=')[1][1:-1]
            os.remove(file_path)
            return ""


@faculty.route('/report', methods=['POST', 'GET'])
@login_required
def view_report():
    if current_user.user != 'faculty':
        abort(403)
    return render_template('portal/report_marks.html')


@faculty.route('/logout', methods=['POST', 'GET'])
def logout_page():
    logout_user()
    return redirect(url_for('main.home_page'))

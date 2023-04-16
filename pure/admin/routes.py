from flask import Blueprint, flash, redirect, url_for, render_template, request, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from pure.admin.forms import Admin_LoginForm
from pure.models import Admin

admin = Blueprint('admin', __name__)


@admin.route('/admin/signin', methods=['POST', 'GET'])
def admin_signin():
    admin_login_form = Admin_LoginForm()
    if admin_login_form.validate_on_submit():
        attempted_admin = Admin()
        if attempted_admin.check_existence(admin_login_form.email.data, specific=True):
            if attempted_admin.check_password(admin_login_form.email.data, admin_login_form.password.data):
                attempted_admin.set_object(admin_login_form.email.data)
                if attempted_admin.user == "admin":
                    login_user(attempted_admin)
                    return redirect(url_for('profile.profile_page'))
                else:
                    flash("Please login through the specific page")
        else:
            flash("Username password are not matching")
    return render_template('auth/login.html', form=admin_login_form, user="admin")


@admin.route('/college_management', methods=['POST', 'GET'])
@login_required
def college_management():
    try:
        current_user.user
        if current_user.user != 'admin':
            abort(403)
        return render_template('portal/management.html')
    except AttributeError:
        abort(403)


@admin.route('/course_management', methods=['POST', 'GET'])
@login_required
def course_management():
    if current_user.user != 'admin':
        abort(403)
    if request.method == 'POST':
        data = str(request.data, 'utf-8').split(',')
        print(data)
        if data[-1] == 'add':
            if not current_user.add_course(data[:-1]):
                flash('Course already exists')
        elif data[-1] == 'proceed':
            current_user.next_semester()
        else:
            current_user.delete_course(data[0])

    return render_template('portal/course_management.html', courses=current_user.get_courses())


@admin.route('/subject_management', methods=['POST', 'GET'])
@login_required
def subject_management():
    if current_user.user != 'admin':
        abort(403)
    if request.method == 'POST':
        data = str(request.data, 'utf-8').split(',')
        if data[-1] == 'get':
            requested_semester = data[0]
            requested_course = data[1]
            subjects_list = current_user.get_subjects(requested_semester, requested_course)
            return jsonify({'subjects': subjects_list})
        elif data[-1] == 'get_duration':
            course_duration = current_user.get_duration(data[0])
            return str(course_duration)
        elif data[-1] == 'add':
            if not current_user.add_subject(data[0], data[1], data[2]):
                flash('Subject already exists')
        elif data[-1] == 'delete':
            current_user.delete_subject(data[0], data[1], data[2])

    return render_template('portal/subject_management.html', courses=current_user.get_courses())


@admin.route('/faculty_approval', methods=['POST', 'GET'])
@login_required
def faculty_approval():
    if current_user.user != 'admin':
        abort(403)
    if request.method == 'POST':
        data = str(request.data, 'utf-8').split(',')
        if data[1] == 'approve':
            current_user.approve_faculty(data[0])
        else:
            current_user.reject_faculty(data[0])

    return render_template('portal/faculty_approval.html', faculty_list=current_user.get_unapproved_faculty_list())


@admin.route('/faculty_management', methods=['POST', 'GET'])
@login_required
def faculty_management():
    if current_user.user != 'admin':
        abort(403)
    if request.method == 'POST':
        data = request.json
        if 'update' in data.keys():
            return jsonify({'status': current_user.update_teacher(data['faculty_id'], data['course'], data['subjects'])})
        elif 'get_details' in data.keys():
            return jsonify(current_user.get_faculty_details(data['faculty_id']))
    return render_template('portal/faculty_management.html', faculty_list=current_user.get_faculty_list(), course_list=current_user.get_courses(), subject_list=current_user.get_all_subjects())


@admin.route('/role_management', methods=['POST', 'GET'])
@login_required
def role_management():
    if current_user.user != 'admin':
        abort(403)
    if request.method == 'POST':
        data = request.json
        if 'add_role' in data.keys():
            if current_user.create_role(data['role'], data['permissions']) is False:
                flash("Already existing role")
        elif 'delete_role' in data.keys():
            candidates = current_user.get_candidates()
            for candidate in candidates:
                if candidate['role'] == data['role']:
                    current_user.change_role(candidate['email'])
            current_user.delete_role(data['role'])
        elif 'delete_candidate' in data.keys():
            current_user.change_role(data['email'])
        elif 'assign_role' in data.keys():
            student = current_user.get_student(data['candidate_mail'])
            if student is None:
                flash("No such student exists")
            else:
                if current_user.assign_role(data['candidate_mail'], data['role']) is False:
                    flash("User is not a student! Roles feature available only for students")

    return render_template('portal/role_management.html', roles=current_user.get_roles(),
                           candidates=current_user.get_candidates(), courses=current_user.get_courses())


@admin.route('/role_management/candidates/<course>', methods=['POST', 'GET'])
@login_required
def handle_crs(course):
    if current_user.user != 'admin':
        abort(403)
    if request.method == 'POST':
        data = request.json
        if 'delete_cr' in data.keys():
            current_user.change_role(data["email"])
        elif 'assign_cr' in data.keys():
            student = current_user.get_student(data['email'])
            if student is None:
                flash("No such user exists")
            else:
                if student['course'] == course:
                    cr = current_user.get_crs(course)
                    if cr["email"] is not None:
                        current_user.change_role(cr["email"])
                    current_user.assign_role(data["email"], 'cr')
                else:
                    flash(f"User does not belong to {course}")

    return current_user.get_crs(course)


@admin.route('/student_moderation', methods=['POST', 'GET'])
@login_required
def student_moderation():
    if current_user.user != 'admin':
        abort(403)
    if request.method == 'POST':
        data = request.json
        action = data['action']
        if action == 'unsuspend':
            current_user.unsuspend_student(data['student_email'])
        elif action == 'delete':
            current_user.delete_student(data['student_email'])
        elif action == 'ban':
            current_user.ban_student(data['student_email'])
    return render_template('portal/admin_student_moderation.html', students=current_user.get_suspended_students())


@admin.route('/logout', methods=['POST', 'GET'])
def logout_page():
    logout_user()
    return redirect(url_for('main.home_page'))

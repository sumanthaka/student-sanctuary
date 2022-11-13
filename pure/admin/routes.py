from flask import Blueprint, flash, redirect, url_for, render_template, make_response, request
from flask_login import login_user, logout_user, current_user

from pure.admin.forms import Admin_LoginForm
from pure.models import Admin

admin = Blueprint('admin', __name__)


@admin.route('/admin/signin', methods=['POST', 'GET'])
def admin_signin():
    admin_login_form = Admin_LoginForm()
    if admin_login_form.validate_on_submit():
        attempted_admin = Admin()
        if attempted_admin.check_existence(admin_login_form.email.data):
            if attempted_admin.check_password(admin_login_form.email.data, admin_login_form.password.data):
                attempted_admin.set_object(admin_login_form.email.data)
                if attempted_admin.user == "admin":
                    login_user(attempted_admin)
                    flash(f"Logged in!! as {attempted_admin.name}")
                    return redirect(url_for('profile.profile_page'))
                else:
                    flash("Username password are not matching")
        else:
            flash("Username password are not matching")
    return render_template('auth/login.html', form=admin_login_form, user="admin")


@admin.route('/college_management', methods=['POST', 'GET'])
def college_management():
    return render_template('portal/management.html')


@admin.route('/course_management', methods=['POST', 'GET'])
def course_management():
    if request.method == 'POST':
        data = str(request.data, 'utf-8').split(',')
        if data[1] == 'add':
            current_user.add_course(data[0])
        else:
            current_user.delete_course(data[0])

    return render_template('portal/course_management.html', courses=current_user.get_courses())


@admin.route('/faculty_approval', methods=['POST', 'GET'])
def faculty_approval():
    if request.method == 'POST':
        data = str(request.data, 'utf-8').split(',')
        if data[1] == 'approve':
            current_user.approve_faculty(data[0])
        else:
            current_user.reject_faculty(data[0])

    return render_template('portal/faculty_approval.html', faculty_list=current_user.get_faculty_list())


@admin.route('/role_management', methods=['POST', 'GET'])
def role_management():
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
    return render_template('portal/role_management.html', roles=current_user.get_roles(), candidates=current_user.get_candidates())


@admin.route('/logout', methods=['POST', 'GET'])
def logout_page():
    logout_user()
    return redirect(url_for('main.home_page'))

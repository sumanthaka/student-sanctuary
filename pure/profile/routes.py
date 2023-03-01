from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask_login import login_required, current_user


profile = Blueprint('profile', __name__)


@profile.route('/profile')
@login_required
def profile_page():
    return render_template('portal/profile.html')


@profile.route('/super_admin/profile')
@login_required
def super_admin_profile_page():
    return render_template('portal/super_admin_profile.html')


@profile.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    try:
        current_user.user
        if request.method == 'POST':
            print(request.form)
            current_user.name = request.form['username']
            if 'course' in request.form.keys():
                current_user.course = request.form['course']
            current_user.update_user()
            return redirect(url_for('profile.profile_page'))
        return render_template('portal/edit_profile.html')
    except AttributeError:
        abort(403)




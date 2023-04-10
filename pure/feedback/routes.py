from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask_login import login_required, current_user


feedback = Blueprint('feedback', __name__)


@feedback.route('/admin_feedback')
@login_required
def admin_feedback():
    if current_user.user != 'admin':
        abort(403)
    return render_template('feedback/create_feedback.html')

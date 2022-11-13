from flask import Blueprint, render_template
from flask_login import login_required

profile = Blueprint('profile', __name__)


@profile.route('/profile')
@login_required
def profile_page():
    return render_template('portal/profile.html')

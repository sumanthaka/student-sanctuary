import os

from flask import Blueprint, render_template, abort, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from pure.models import Advertisement

ads = Blueprint('ads', __name__)


@ads.route('/ads')
def ads_page():
    return render_template('ads/ads.html', ads=Advertisement.get_all_ads())


@ads.route('/admin_ads', methods=['GET', 'POST'])
@login_required
def admin_ads_page():
    if current_user.user != 'admin':
        abort(403)

    if request.method == 'POST':
        data = request.form
        file = request.files['ads_file']
        sec_filename = secure_filename(file.filename)
        path = os.path.join(os.path.abspath(os.curdir), 'pure', 'static', 'ads', sec_filename)
        if os.path.exists(path):
            flash(f'File already exists: {file.filename}')

        else:
            file.save(path)
            Advertisement.create_ad(sec_filename, data['ad_link'], current_user.college)
    return render_template('ads/admin_ads.html')

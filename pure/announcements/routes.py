from flask import Blueprint, render_template
from flask_login import login_required, current_user

from pure.announcements.forms import Announcement_Form
from pure.models import Announcement

announcement = Blueprint('announcement', __name__)


@announcement.route('/admin/portal/announcement_maker', methods=['POST', 'GET'])
@login_required
def announcement_maker():
    announcement_maker_form = Announcement_Form()
    if announcement_maker_form.validate_on_submit():
        announcement = Announcement(author=[current_user.email, current_user.name],
                                    target=announcement_maker_form.target.data,
                                    title=announcement_maker_form.title.data,
                                    subject=announcement_maker_form.subject.data,
                                    desc=announcement_maker_form.desc.data)
        announcement.create_announcement(current_user.college)
    return render_template('portal/announcements_maker.html', form=announcement_maker_form)

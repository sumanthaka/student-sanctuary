from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from pure.announcements.forms import Announcement_Form, Cr_Announcement_Form
from pure.models import Announcement, User

announcement = Blueprint('announcement', __name__)


@announcement.route('/announcement_maker', methods=['POST', 'GET'])
@login_required
def announcement_maker():
    if current_user.user == "student":
        if 'announcement_maker' not in current_user.get_permissions():
            return redirect(url_for('profile.profile_page'))
    if current_user.role == 'cr':
        announcement_maker_form = Cr_Announcement_Form()
        announcement_maker_form.target.choices.append(current_user.course)
    else:
        announcement_maker_form = Announcement_Form()
        announcement_maker_form.target.choices = User.get_courses(current_user.college)

    if announcement_maker_form.validate_on_submit():
        everyone_target = announcement_maker_form.target_everyone.data
        faculty_target = announcement_maker_form.target_faculty.data
        target_list = announcement_maker_form.target.data
        if everyone_target:
            target = ['Everyone']
        elif faculty_target:
            target = ['All Faculty']
        elif target_list:
            target = target_list
        else:
            flash("Please select a target audience")
            return redirect(url_for('announcement.announcement_maker'))
        announcement = Announcement(author=[current_user.email, current_user.name],
                                    target=target,
                                    title=announcement_maker_form.title.data,
                                    subject=announcement_maker_form.subject.data,
                                    desc=announcement_maker_form.desc.data)
        announcement.create_announcement(current_user.college)
        return redirect(url_for('announcement.announcement_maker'))
    return render_template('portal/announcements_maker.html', form=announcement_maker_form)


@announcement.route('/announcements', methods=['POST', 'GET'])
@login_required
def announcements():
    announcements_list = Announcement.get_announcements(current_user.college, current_user.user, current_user.course)
    return render_template('portal/announcements.html', announcements=announcements_list)

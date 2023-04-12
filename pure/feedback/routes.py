from flask import Blueprint, render_template, redirect, url_for, abort, request, jsonify
from flask_login import login_required, current_user

from pure.models import Feedback

feedback = Blueprint('feedback', __name__)


@feedback.route('/admin_feedback')
@login_required
def admin_feedback():
    if current_user.user != 'admin':
        abort(403)
    return render_template('feedback/admin_feedback.html')


@feedback.route('/feedback_questions', methods=['GET', 'POST'])
@login_required
def feedback_questions():
    if current_user.user != 'admin' and current_user.user != 'student':
        abort(403)
    if request.method == 'POST':
        form_id = request.data.decode('utf-8')
        questions = Feedback.get_questions(form_id, current_user.college)
        return jsonify({'questions': questions})
    return redirect(url_for('feedback.admin_feedback'))


@feedback.route('/draft_feedback', methods=['GET', 'POST'])
@login_required
def draft_feedback():
    if current_user.user != 'admin':
        abort(403)
    if request.method == 'POST':
        if request.json['type'] == 'save':
            form_id = request.json['form_id']
            questions = request.json['questions']
            Feedback.update_form(form_id, questions, current_user.college)
        elif request.json['type'] == 'create':
            form_name = request.json['form_title']
            if form_name == '':
                form_name = 'Untitled Form'
            Feedback.create_form(form_name, current_user.college)
        elif request.json['type'] == 'delete':
            form_id = request.json['form_id']
            Feedback.delete_form(form_id, current_user.college)
        elif request.json['type'] == 'publish':
            form_id = request.json['form_id']
            target = request.json['target']
            Feedback.publish_form(form_id, target, current_user.college)

    draft_forms = Feedback.get_draft_forms(current_user.college)
    return render_template('feedback/draft_feedback.html', forms=draft_forms, courses=current_user.get_courses())


@feedback.route('/open_feedback', methods=['GET', 'POST'])
@login_required
def open_feedback():
    if current_user.user != 'admin':
        abort(403)
    if request.method == 'POST':
        form_id = request.data.decode('utf-8')
        Feedback.close_form(form_id, current_user.college)
        Feedback.summarize_form(form_id, current_user.college)
    published_forms = Feedback.get_published_forms(current_user.college)
    return render_template('feedback/open_feedback.html', forms=published_forms)


@feedback.route('/student_feedback', methods=['GET', 'POST'])
@login_required
def student_feedback():
    if current_user.user != 'student':
        abort(403)
    if request.method == 'POST':
        if request.json['type'] == 'get_faculty':
            form_id = request.json['form_id']
            faculty = Feedback.get_faculty_list(form_id, current_user)
            return jsonify({'faculty': faculty})
        if request.json['type'] == 'submit':
            form_id = request.json['form_id']
            faculty = request.json['faculty_id']
            answers = request.json['answers']
            Feedback.submit_form(form_id, faculty, current_user.id, answers, current_user.college)
    forms = Feedback.get_published_forms(current_user.college, current_user.course)
    return render_template('feedback/student_feedback.html', forms=forms)


@feedback.route('/result_feedback', methods=['GET', 'POST'])
@login_required
def result_feedback():
    if current_user.user != 'admin':
        abort(403)
    if request.method == 'POST':
        if request.json['type'] == 'get_faculty':
            form_id = request.json['form_id']
            faculty = Feedback.get_form_faculty(form_id, current_user.college)
            return jsonify({'faculty': faculty})
        if request.json['type'] == 'get_result':
            form_id = request.json['form_id']
            faculty_id = request.json['faculty_id']
            result = Feedback.get_form_result(form_id, faculty_id, current_user.college)
            return jsonify({'result': result})
    forms = Feedback.get_closed_forms(current_user.college)
    return render_template('feedback/result_feedback.html', forms=forms)

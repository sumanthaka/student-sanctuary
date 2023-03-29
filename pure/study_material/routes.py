import os

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from pure.models import Study_material

study_material = Blueprint('study_material', __name__)


@study_material.route('/study_material_upload', methods=['POST', 'GET'])
@login_required
def study_material_upload():
    if current_user.user != "faculty":
        abort(403)
    if request.method == 'POST':
        data = request.form
        files = request.files.getlist('notes_file')
        rep_file = []
        for file in files:
            sec_filename = secure_filename(file.filename)
            path = os.path.join(os.path.abspath(os.curdir), 'pure', 'static', 'notes_files', sec_filename)
            if os.path.exists(path):
                rep_file.append(file.filename)
                continue
            file.save(path)
            file_info = {'filename': file.filename, 'subject_id': data['subject'], 'path': path}
            current_user.upload_notes(file_info)
        if rep_file:
            flash(f'File(s) already exists: {rep_file}')
    return render_template('portal/study_material.html', subjects=current_user.get_faculty_subjects())


@study_material.route('/study_material', methods=['POST', 'GET'])
@login_required
def study_material_student():
    if current_user.user != "student":
        abort(403)
    return render_template('portal/study_material_student.html', subjects=current_user.get_subjects(current_user.get_current_sem(current_user.course), current_user.course, req_id=True))


@study_material.route('/study_material_list', methods=['POST', 'GET'])
@login_required
def study_material_list():
    if request.method == 'POST':
        data = str(request.data, 'utf-8').split(',')
        if data[-1] == 'get':
            notes_list = Study_material.get_notes(current_user.college, data[0])
            return jsonify({'notes': notes_list})
        elif data[-1] == 'delete':
            if current_user.user != "faculty":
                abort(403)
            path = Study_material.delete_notes(current_user.college, data[0])
            os.remove(path)
            return jsonify({'status': 'success'})
        elif data[-1] == 'download':
            path = Study_material.get_notes_path(current_user.college, data[0])
            return send_file(path)
    return jsonify({'notes': []})



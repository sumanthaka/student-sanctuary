import os.path
import uuid

import openpyxl as openpyxl
import pdfkit as pdfkit
from bokeh.io import curdoc
from bokeh.embed import components
from bokeh.models import CategoricalAxis
from bokeh.plotting import figure
from bokeh.resources import CDN

from flask import Blueprint, flash, redirect, url_for, render_template, abort, request, send_file, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from pure.faculty.forms import Faculty_LoginForm, Faculty_SignupForm, EventForm
from pure.models import Faculty, Event

faculty = Blueprint('faculty', __name__)


@faculty.route('/faculty/signin', methods=['POST', 'GET'])
def faculty_signin():
    faculty_login_form = Faculty_LoginForm()
    if faculty_login_form.validate_on_submit():
        attempted_faculty = Faculty()
        if attempted_faculty.check_existence(faculty_login_form.email.data, specific=True):
            if attempted_faculty.check_password(faculty_login_form.email.data, faculty_login_form.password.data):
                attempted_faculty.set_object(faculty_login_form.email.data)
                if attempted_faculty.user == "faculty":
                    if attempted_faculty.approved:
                        login_user(attempted_faculty)
                        return redirect(url_for('profile.profile_page'))
                    else:
                        flash("Admin has not approved yet")
                else:
                    flash("Please login through the specific page")
        else:
            flash("Username password are not matching")
    return render_template('auth/login.html', form=faculty_login_form, user="faculty")


@faculty.route('/faculty/signup', methods=['POST', 'GET'])
def faculty_signup():
    faculty_signup_form = Faculty_SignupForm()
    faculty_signup_form.college.choices = Faculty.get_colleges()
    if faculty_signup_form.validate_on_submit():
        faculty_to_create = Faculty()
        faculty_to_create.create_user(name=faculty_signup_form.name.data,
                                      email=faculty_signup_form.email.data,
                                      college=faculty_signup_form.college.data,
                                      password=faculty_signup_form.password.data)
        return redirect(url_for('faculty.faculty_signin'))
    if faculty_signup_form.errors:
        for error in faculty_signup_form.errors.values():
            flash(error)
    return render_template('auth/signup.html', form=faculty_signup_form, user="faculty")


@faculty.route('/upload_marks', methods=['POST', 'GET'])
@login_required
def upload_marks():
    if current_user.user != 'faculty':
        abort(403)
    if request.method == 'POST':
        data = request.form
        exam_info = {}
        max_marks = {}
        exam_info.update({'exam_name': data['exam_name'].lower()})
        for subject in list(data.keys())[1:]:
            max_marks.update({subject: int(data.get(subject))})
        exam_info.update({'max_marks': max_marks})
        upload_done = current_user.upload_exam(exam_info, request.files['marks_file'])
        if not upload_done[0]:
            flash(upload_done[1])
    return render_template('portal/upload_marks.html', subjects_list=current_user.get_subjects(current_user.get_current_sem(current_user.course_faculty), current_user.course_faculty))


@faculty.route('/download_template', methods=['POST', 'GET'])
@login_required
def send_template():
    if current_user.user != 'faculty':
        abort(403)
    if request.method == 'POST':
        data = str(request.data, 'utf-8').split(',')
        if data[0] == 'add':
            filepath = os.path.join(os.path.abspath(os.curdir), 'pure', 'static', 'mark_files')
            filename = str(uuid.uuid4())
            excel_file_path = os.path.join(filepath, filename)+'.xlsx'
            book = openpyxl.Workbook()
            worksheet = book.active
            headers = ['Name', 'Email']
            subjects = current_user.get_subjects(current_user.get_current_sem(current_user.course_faculty), current_user.course_faculty)
            headers += subjects
            worksheet.append(headers)
            student_list = current_user.get_course_student()
            for student in student_list:
                worksheet.append([student['name'], student['email']])
            for i in range(ord('A'), ord('A')+len(subjects)+2):
                worksheet.column_dimensions[chr(i)].width = 20
            book.save(excel_file_path)
            response = send_file(excel_file_path, as_attachment=True)
            response.set_cookie('filename', excel_file_path)
            return response
        else:
            file_path = data[1].split('=')[1][1:-1]
            os.remove(file_path)
            return ""


@faculty.route('/report', methods=['POST', 'GET'])
@login_required
def view_report():
    if current_user.user != 'faculty':
        abort(403)
    cdn_js = CDN.js_files
    return render_template('portal/report_marks.html', js_cdn=cdn_js)


@faculty.route('/exams_avg', methods=['POST'])
@login_required
def exams_avg():
    if current_user.user != 'faculty':
        abort(403)
    semester = int(request.data)
    return render_template('portal/exams_avg.html', exam_list=current_user.get_exams(semester))


@faculty.route('/exams_avg/<examid>', methods=['POST', 'GET'])
@login_required
def exam_avg_graph(examid):
    if current_user.user != 'faculty':
        abort(403)
    curdoc().theme = "night_sky"
    x, y, title = current_user.exam_sub_avg(examid)
    plot = figure(x_range=x, y_range=(0, max(y) + 10), tools='save', tooltips=[("(x,y)", "(@x, $y)")], title=title.capitalize())
    plot.title.align = 'center'
    plot.sizing_mode = "scale_width"
    plot.background_fill_color = '#00000000'
    plot.xaxis.axis_label = 'Subjects'
    plot.yaxis.axis_label = 'Marks'
    plot.vbar(x, top=y, width=0.5, color='#dedede')
    script, div = components(plot, wrap_script=False, theme=curdoc().theme)
    return {'script': script, 'div': div}


@faculty.route('/student_report', methods=['POST', 'GET'])
@login_required
def student_report():
    if current_user.user != 'faculty':
        abort(403)
    return render_template('portal/student_report.html', student_list=current_user.get_course_student())


@faculty.route('/student_report/<studentid>/<semval>', methods=['POST', 'GET'])
@login_required
def student_report_graphs(studentid, semval):
    if current_user.user != 'faculty':
        abort(403)
    curdoc().theme = "night_sky"
    x, y = current_user.student_all_marks(studentid, semval)
    average = y['avg']
    if not average:
        return {'script': '', 'div': ''}
    marks = y['marks']
    exam_names = y['exam_names']
    script, div = "", ""
    for i in range(len(marks)):
        exam_mark = marks[i][1:]
        plot = figure(x_range=x, y_range=(0, max(exam_mark)+10), tools='save', tooltips=[("(x,y)", "(@x, $y)")], title=exam_names[i].capitalize())
        plot.title.align = 'center'
        plot.background_fill_color = '#00000000'
        plot.xaxis.axis_label = 'Subjects'
        plot.yaxis.axis_label = 'Marks'
        plot.vbar(x, top=exam_mark, width=0.5, color='#dedede')
        gen_script, gen_div = components(plot,  wrap_script=False, theme=curdoc().theme)
        script += gen_script
        div += gen_div
    plot = figure(x_range=exam_names, y_range=(0, max(average)+10), tools='save', tooltips=[("(x,y)", "(@x, $y)")], title="Exam Average Trends over Time")
    plot.xaxis[0] = CategoricalAxis()
    plot.line(x=exam_names, y=average, color='#dedede', line_width=4)
    plot.circle(x=exam_names, y=average, size=10, color='#dedede')
    plot.title.align = 'center'
    plot.background_fill_color = '#00000000'
    plot.xaxis.axis_label = 'Exams'
    plot.yaxis.axis_label = 'Marks'
    gen_script, gen_div = components(plot, wrap_script=False, theme=curdoc().theme)
    script += gen_script
    div += gen_div
    return {'script': script, 'div': div}


@faculty.route('/event_report', methods=['POST', 'GET'])
@login_required
def event_report():
    if current_user.user != 'faculty':
        abort(403)
    event_form = EventForm()
    event_form.participants.choices = current_user.get_courses(current_user.college)

    if event_form.validate_on_submit():
        paths = []
        if event_form.images.data:
            images = event_form.images.data
            rep_file = []
            for image in images:
                sec_filename = secure_filename(image.filename)
                path = os.path.join(os.path.abspath(os.curdir), 'pure', 'static', 'events_images', sec_filename)
                if os.path.exists(path):
                    rep_file.append(image)
                    continue
                paths.append(sec_filename)
                image.save(os.path.join(os.path.abspath(os.curdir), 'pure', 'static', 'events_images', sec_filename))
            if rep_file:
                flash(f'Following files are already present in the server and are not uploaded again: {rep_file}')

        event = Event(title=event_form.title.data,
                      desc=event_form.desc.data,
                      date=event_form.date.data,
                      participants=event_form.participants.data,
                      paths=paths,
                      author=current_user.email)
        event.create_event(current_user.college)
        return redirect(url_for('faculty.event_report'))
    return render_template('portal/event_report.html', form=event_form, events=Event.get_events(current_user.college, current_user.email))


@faculty.route('/delete_event', methods=['POST'])
@login_required
def delete_event():
    if current_user.user != 'faculty':
        abort(403)
    data = request.data.decode('utf-8')
    print(data)
    images = Event.delete_event(current_user.college, data)
    for image in images:
        os.remove(os.path.join(os.path.abspath(os.curdir), 'pure', 'static', 'events_images', image))
    return redirect(url_for('faculty.event_report'))


@faculty.route('/generate_event_report', methods=['POST', 'GET'])
@login_required
def generate_event_report():
    if current_user.user != 'faculty':
        abort(403)
    event_id = request.data.decode('utf-8')
    event_info = Event.get_event(current_user.college, event_id)
    participants = {}
    participants_count = 0
    for participant in event_info['participants']:
        students_info = current_user.get_course_students(participant)
        name_list = []
        for student in students_info:
            name_list.append(student['name'])
        participants[participant] = name_list
        participants_count += len(name_list)
    rendered = render_template('event_report/event_report_pdf.html', event=event_info, participants=participants, participants_count=participants_count, logo=current_user.get_logo())
    # return rendered
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    css = [os.path.join(os.path.abspath(os.curdir), 'pure', 'static', 'style.css'), os.path.join(os.path.abspath(os.curdir), 'pure', 'static', 'bootstrap', 'css', 'bootstrap.min.css')]
    pdf = pdfkit.from_string(rendered, False, configuration=config, options={"enable-local-file-access": ""}, css=css)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=event_report.pdf'
    return response


@faculty.route('/student_moderation', methods=['POST', 'GET'])
@login_required
def student_moderation():
    if current_user.user != 'faculty':
        abort(403)
    if request.method == 'POST':
        student_email = request.data.decode('utf-8')
        current_user.suspend_student(student_email)
    return render_template('portal/student_moderation.html', students=current_user.get_course_students(current_user.course_faculty))


@faculty.route('/logout', methods=['POST', 'GET'])
def logout_page():
    logout_user()
    return redirect(url_for('main.home_page'))

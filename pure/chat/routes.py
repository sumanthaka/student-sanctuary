from flask import Blueprint, render_template, abort, request
from flask_login import login_required, current_user
from flask_socketio import join_room, leave_room

from pure import socketio
from pure.models import Chat

chat = Blueprint('chat', __name__)


@chat.route('/chat')
@login_required
def chat_page():
    try:
        if current_user.user == 'student' or current_user.user == 'faculty':
            return render_template('chat/chat.html')
        else:
            abort(403)
    except AttributeError:
        abort(403)


@socketio.on('join_room')
def handle_join_room(data):
    if current_user.user == 'student':
        room_id = Chat.get_room_id_course(current_user.college, data['email'])
    else:
        room_id = Chat.get_room_id_faculty(current_user.college)
    join_room(room_id)
    session_id = request.sid
    data = {}
    data.update({'room': room_id})
    messages = current_user.get_messages(room_id)
    data.update({'messages': messages})
    socketio.emit('join_room_announcement', data, to=session_id)


@socketio.on('change_room')
def handle_change_room(data):
    leave_room(data['current_room'])
    if data['room_choice'] == 'college':
        room_id = Chat.get_room_id_college(current_user.college)
        join_room(room_id)
        session_id = request.sid
        data = {}
        data.update({'room': room_id})
        messages = current_user.get_messages(room_id)
        data.update({'messages': messages})
        socketio.emit('join_room_announcement', data, to=session_id)

    elif data['room_choice'] == 'Course':
        if current_user.user == "student":
            room_id = Chat.get_room_id_course(current_user.college, data['email'])
        else:
            room_id = Chat.get_room_id_course_faculty(current_user.college, data['email'])
        join_room(room_id)
        session_id = request.sid
        data = {}
        data.update({'room': room_id})
        messages = current_user.get_messages(room_id)
        data.update({'messages': messages})
        socketio.emit('join_room_announcement', data, to=session_id)

    elif data['room_choice'] == 'student_council':
        room_id = Chat.get_room_id_council(current_user.college)
        join_room(room_id)
        session_id = request.sid
        data = {}
        data.update({'room': room_id})
        messages = current_user.get_messages(room_id)
        data.update({'messages': messages})
        socketio.emit('join_room_announcement', data, to=session_id)


@socketio.on('send_message')
def handle_send_message(data):
    room_id = data['room']
    current_user.save_message(room_id, data['email'], data['name'], data['message'])
    socketio.emit('receive_message', data, to=room_id)

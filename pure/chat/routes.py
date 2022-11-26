from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_socketio import join_room, leave_room

from pure import socketio
from pure.models import Chat

chat = Blueprint('chat', __name__)


@chat.route('/chat')
@login_required
def chat_page():
    return render_template('chat/chat.html')


@socketio.on('join_room')
def handle_join_room(data):
    room_id = Chat.get_room_id_course(current_user.college, data['email'])
    join_room(room_id)
    print('change', room_id)
    data.update({'room': room_id})
    socketio.emit('join_room_announcement', data, room=room_id)


@socketio.on('change_room')
def handle_change_room(data):
    leave_room(data['current_room'])
    if data['room_choice'] == 'college':
        room_id = Chat.get_room_id_college(current_user.college)
        join_room(room_id)
        data.pop('current_room')
        data.update({'room': room_id})
        socketio.emit('join_room_announcement', data, room=room_id)

    if data['room_choice'] == 'Course':
        room_id = Chat.get_room_id_course(current_user.college, data['email'])
        join_room(room_id)
        data.update({'room': room_id})
        socketio.emit('join_room_announcement', data, room=room_id)


@socketio.on('send_message')
def handle_send_message(data):
    room_id = data['room']
    print(data['name'], room_id)
    socketio.emit('receive_message', data, to=room_id)

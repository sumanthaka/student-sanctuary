from flask import Blueprint, render_template

from pure import socketio

chat = Blueprint('chat', __name__)


@chat.route('/chat')
def chat_page():
    return render_template('chat/chat.html')


@socketio.on('join_room')
def handle(data):
    print(data)
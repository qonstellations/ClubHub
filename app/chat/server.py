"""

RUN THIS FILE INDEPENDENTLY BEFORE RUNNING MAIN.PY

"uv run -m app.chat.server"

"""

# app/chat/server.py

from flask import Flask, request
from flask_socketio import SocketIO, emit
from app.core.user import User

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

connected_users = dict() # dict([str, User])

@socketio.on("connect")
def on_connect():
    print(f"[CONNECT] {request.sid}")

@socketio.on("add_user")
def add_user(data):
    user = User.conv_to_obj(data["user"])
    connected_users[request.sid] = user

    emit(
        "system_message",
        f"**{user.first_name} joined the chat**",
        broadcast=True
    )

@socketio.on("send_message")
def on_send_message(data):
    user = connected_users.get(request.sid)

    if not user:
        return

    message = f"{user.first_name}: {data['message']}"

    emit(
        "new_message",
        message,
        broadcast=True
    )

@socketio.on("disconnect")
def on_disconnect():
    user = connected_users.pop(request.sid, None)

    if user:
        emit(
            "system_message",
            f"**{user.first_name} left the chat**",
            broadcast=True
        )

    print(f"[DISCONNECT] {request.sid}")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10001)

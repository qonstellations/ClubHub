"""

RUN THIS FILE INDEPENDENTLY BEFORE RUNNING MAIN.PY

"uv run -m app.chat.server"

"""

from app.db.models import User

from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# socket_id -> user object
users = {}

@socketio.on("connect")
def on_connect():
    print("Client connected")

@socketio.on("add_user")
def add_user(data):
    from flask import request
    user = User.conv_to_obj(data["user"])
    users[request.sid] = user

    emit("system_message", f"{user.first_name} joined the chat", broadcast=True)

@socketio.on("send_message")
def send_message(data):
    from flask import request
    user = users.get(request.sid, "Unknown")

    message = f"{user.first_name}: {data['message']}"
    emit("new_message", message, broadcast=True)

@socketio.on("disconnect")
def on_disconnect():
    from flask import request
    user = users.pop(request.sid, None)
    if user:
        emit("system_message", f"{user.first_name} left the chat", broadcast=True)
    print("Client disconnected")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10001)

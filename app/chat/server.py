from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# socket_id -> nickname
users = {}

@socketio.on("connect")
def on_connect():
    print("Client connected")

@socketio.on("set_nickname")
def set_nickname(data):
    nickname = data["nickname"]
    users[id(socketio)] = nickname   # temporary key replaced below

    # better: use request.sid
    from flask import request
    users[request.sid] = nickname

    emit("system_message", f"{nickname} joined the chat", broadcast=True)

@socketio.on("send_message")
def send_message(data):
    from flask import request
    nickname = users.get(request.sid, "Unknown")

    message = f"{nickname}: {data['message']}"
    emit("new_message", message, broadcast=True)

@socketio.on("disconnect")
def on_disconnect():
    from flask import request
    nickname = users.pop(request.sid, None)
    if nickname:
        emit("system_message", f"{nickname} left the chat", broadcast=True)
    print("Client disconnected")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10001)

from app.core.user import User

import socketio
import threading

current_user = None

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")
    sio.emit("add_user", {"user": current_user.conv_to_wire()})

@sio.on("new_message")
def on_message(msg):
    print(msg)

@sio.on("system_message")
def on_system(msg):
    print(f"[SYSTEM] {msg}")

@sio.event
def disconnect():
    print("Disconnected from server")

def write():
    while True:
        try:
            msg = input()
            if not msg:
                raise ValueError("No message provided!")
                return
            sio.emit("send_message", {"message": msg})
        except (KeyboardInterrupt, EOFError):
            sio.disconnect()
            break

def start_client(user):
    global current_user
    current_user = user

    sio.connect("http://127.0.0.1:10001")
    threading.Thread(target=write, daemon=True).start()
    sio.wait()
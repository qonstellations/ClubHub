import socketio
import threading

nickname = input("Choose a nickname: ")

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")
    sio.emit("set_nickname", {"nickname": nickname})

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
            sio.emit("send_message", {"message": msg})
        except (KeyboardInterrupt, EOFError):
            sio.disconnect()
            break

sio.connect("http://127.0.0.1:10001")

write_thread = threading.Thread(target=write)
write_thread.start()

sio.wait()

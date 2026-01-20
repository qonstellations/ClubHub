from app.core.user import User
from app.core.club import Club
from app.core.channel import Channel

import socketio

sio = socketio.Client()

def start_client(
    user : User, 
    club : Club, 
    channel : Channel
):
    from app.tui.chat import ChatScreen
    chat_ui = ChatScreen(
        user=user,
        club=club,
        channel=channel,
        sio=sio
    )

    sio.connect("http://127.0.0.1:10001")
    chat_ui.run(headless=False) # Set headless=True for debugging textual based errors

    @sio.event
    def connect():
        sio.emit("add_user", {"user": user.conv_to_wire()})
    
    @sio.event
    def new_message(msg):
        chat_ui.call_from_thread(chat_ui.add_message, msg)
    
    @sio.event
    def system_message(msg):
        chat_ui.call_from_thread(chat_ui.add_message, f"[SYSTEM] {msg}")

    sio.disconnect()
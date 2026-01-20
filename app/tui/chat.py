from app.core.user import User
from app.core.club import Club
from app.core.channel import Channel
from app.chat.client import start_client

from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from textual.containers import Vertical

import socketio

def start_chat(
    user : User, 
    club : Club, 
    channel : Channel
):
    start_client(
        user=user,
        club=club,
        channel=channel
    )

class ChatScreen(App):
    # Using Textual CSS to style the chat UI screen
    CSS = """
    #header {
        height: 3;
        border: round green;
        content-align: center middle;
        padding: 0 1;
    }

    #messages {
        height: 1fr;
        border: round blue;
        padding: 1 2;
    }

    #input {
        height: 3;
        border: round white;
        padding: 0 1;
    }
    """

    def __init__(
        self, 
        user : User, 
        club : Club, 
        channel : Channel, 
        sio: socketio.Client
    ):
        super().__init__()
        self.user = user
        self.club = club
        self.channel = channel
        self.sio = sio
        self.buffer = ""

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(f"{self.club.name} | {self.channel.name}", id="header"),
            Static("", id="messages"),
            Input(placeholder="Type message… (/exit to leave)", id="input"),
        )

    def add_message(self, msg: str):
        self.buffer += msg + "\n"
        self.query_one("#messages", Static).update(self.buffer)

    def on_input_submitted(self, event: Input.Submitted):
        msg = event.value.strip()
        event.input.value = ""

        if not msg:
            return

        if msg == "/exit":
            self.sio.disconnect()
            self.exit()
            return

        self.add_message(f"{self.user.first_name}: {msg}")
        self.sio.emit("send_message", {"message": msg})

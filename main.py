# from app.tui.run import welcome
from app.core.user import authenticate_user, create_user
from app.chat import client

def main():
    # welcome()

    """

    RUN THIS BEFORE RUNNING MAIN.PY

    "uv run -m app.chat.server"

    """

    # user = create_user("pookie@gmail.com", "abc123", "abc123", "pookie", "wookie")

    user = authenticate_user("pookie@gmail.com", "abc123")

    client.start_client(user=user)
    client.write()

if __name__ == "__main__":
    main()
from app.tui.run import welcome, homepage
from app.core.user import authenticate_user, create_user
from app.chat import client

def main():
    welcome()

    """

    RUN THIS BEFORE RUNNING MAIN.PY

    "uv run -m app.chat.server"

    """

    # user = create_user("pookie@gmail.com", "abc123", "abc123", "pookie", "wookie")

    # user = authenticate_user("makhanchor@gmail.com", "ghopghop")
    # homepage(user=user)

if __name__ == "__main__":
    main()

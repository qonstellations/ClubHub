from app.db.models import User
from app.db.client import db
from app.db.query import find_user

from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(
    email: str,
    password1: str, 
    password2: str,
    first_name: str,
    last_name: str
) -> User:
    
    if not all([email, password1, password2, first_name, last_name]):
        raise ValueError("All fields are compulsory")

    if password1 != password2:
        raise ValueError("Passwords do not match")

    if len(password1) < 5:
        raise ValueError("Password must be at least 5 characters")

    if find_user(email=email) is not None:
        raise ValueError("User with this email already exists!")

    email = email.lower().strip()

    user = User(
        _id=None,
        email=email,
        pw_hash=generate_password_hash(password1),
        first_name=first_name,
        last_name=last_name
    )
    
    new_user_id = db.users.insert_one(user.conv_to_doc()).inserted_id
    user._id = new_user_id

    return user

def authenticate_user(email : str, password: str) -> User:
    remote_user = find_user(email=email)

    if remote_user is None:
        raise ValueError("User with given email not found")
    else:
        if check_password_hash(remote_user.pw_hash, password):
            return remote_user
        else:
            raise ValueError("Passwords do not match!")
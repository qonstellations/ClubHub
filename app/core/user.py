from app.db.user import User, ObjectId, insert_user, find_user
from app.db.club import Club, find_club
from app.db.role import Role, find_role
from app.db.membership import find_memberships

from functools import wraps
from pymongo.errors import DuplicateKeyError
from werkzeug.security import check_password_hash

def create_user(
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
    # making the email (entered by the user) in lower cases and removing any whitespaces present in it.

    user = insert_user(
        email=email,
        password=password1,
        first_name=first_name,
        last_name=last_name
    )

    return user

def authenticate_user(
    email : str,
    password: str
) -> User:
    remote_user = find_user(email=email)

    if remote_user is None:
        raise ValueError("User with given email not found")
    else:
        if check_password_hash(remote_user.pw_hash, password):
            return remote_user
        else:
            raise ValueError("Passwords do not match!")

# Decorator for only admin functions
def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("user") or args[0]
        club = kwargs.get("club") or args[1]

        membership = find_memberships(user_id=user._id, club_id=club._id)[0]

        if not membership.is_admin:
            raise PermissionError("Admin privileges required")

        return func(*args, **kwargs)
    return wrapper

def get_user_clubs(
    user : User
) -> list:
    memberships = find_memberships(user_id=user._id)

    if memberships is None:
        return None

    club_list = list()
    for membership in memberships:
        club_list.append(find_club(_id=membership.club_id))

    if club_list == []:
        return None
    else:
        return club_list

def get_user_role(
    user : User,
    club : Club
) -> Role:
    membership = find_memberships(user_id=user._id, club_id=club._id)[0]
    user_role = find_role(_id=membership.role_id)
    return user_role
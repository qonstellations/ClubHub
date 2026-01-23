from app.db.club import Club, ObjectId, insert_club, get_club_member_count
from app.db.role import insert_role, find_role, find_roles_list
from app.db.user import User, find_user
from app.db.membership import insert_membership, Membership
from app.core.user import is_admin
from app.config import ADMIN_BOOTSTRAP_KEYS

def create_club(
    name: str,
    description: str,
    club_code: str,
    secret_key: str,
    creator: User
) -> Club:

    expected_secret_key = ADMIN_BOOTSTRAP_KEYS.get(club_code)
    if expected_secret_key is None:
        raise ValueError("Invalid club code")
    if secret_key != expected_secret_key:
        raise ValueError("Secret key doesn't match")
    
    if not name or not description or not secret_key or creator is None:
        raise ValueError("All fields are compulsory")
    
    try:
        club = insert_club(name=name, description=description, club_code=club_code)
        lead_role =insert_role(name="Lead", club_id=club._id)
        lead_membership = insert_membership(
            user_id=creator._id, 
            club_id=club._id, 
            role_id=lead_role._id,
            is_admin=True
        )
    except Exception as e:
        # Delete Club and Lead Role from MongoDB
        # if all 3 are not created succesfully
        # This avoids residual data
        print(e)

    return club

def club_member_count(
    club : Club
) -> int:
    mem_count = get_club_member_count(club=club)
    
    if mem_count == 0:
        raise ValueError("Club not Found!")
    else:
        return mem_count
    
def add_club_member(
    email: str,
    role_name : str,
    club : Club,
    user : User,
    make_admin : bool
) -> Membership:
    
    role = find_role(name=role_name, club_id=club._id)
    found_user = find_user(email=email)

    if found_user is not None:
        if not is_admin(user=user, club=club):
            raise PermissionError("Admin privileges required")

        if role is not None:
            print(role._id)
            print(role.name)
            raise ValueError("Role already exists")
        
        role = insert_role(name=role_name, club_id=club._id)
        membership = insert_membership(
            user_id=found_user._id, 
            club_id=club._id, 
            role_id=role._id,
            is_admin=make_admin
        )
        return membership
    else:
        raise ValueError("User not found")
    
def get_roles(
    _id : None,
    club : Club
)->list:
    
    roles_list = find_roles_list(club_id=club._id)

    if roles_list == []:
        return None
    else:
        return roles_list


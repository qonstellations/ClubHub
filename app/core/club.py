from app.db.club import Club, ObjectId, insert_club, get_club_member_count
from app.db.role import insert_role, find_roles, Role
from app.db.user import User, find_user
from app.db.membership import insert_membership, find_memberships, Membership
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
    club : Club,
    role : Role,
    user : User,
    make_admin : bool
) -> Membership:
    
    role = find_roles(name=role.name, club_id=club._id)[0]
    found_user = find_user(email=email)

    if found_user is not None:
        if not is_admin(user=user, club=club):
            raise PermissionError("Admin privileges required")
        
        membership = insert_membership(
            user_id=found_user._id, 
            club_id=club._id, 
            role_id=role._id,
            is_admin=make_admin
        )
        return membership
    else:
        raise ValueError("User not found")
    
def get_club_roles(
    _id : None,
    club : Club
)->list: 
    roles_list = find_roles(club_id=club._id)

    return None if roles_list == [] else roles_list

def add_club_role(
    name : str,
    club : Club
):
    if not all([name, club]):
        raise ValueError("All fields are compulsory")

    role = insert_role(name=name, club_id=club._id)
    return role
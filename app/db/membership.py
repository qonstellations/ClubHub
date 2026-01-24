from app.db.models import Membership, ObjectId, datetime
from app.db.client import db

def insert_membership(
    user_id: ObjectId,
    club_id: ObjectId,
    role_id: ObjectId,
    is_admin: bool
) -> Membership:

    membership = Membership(
        _id=None,
        user_id=user_id,
        club_id=club_id,
        role_id=role_id,
        joined_at=datetime.now(),
        left_at=None,
        is_admin=is_admin
    )

    new_membership_id = db.memberships.insert_one(membership.conv_to_doc()).inserted_id
    membership._id = new_membership_id

    return membership

def find_memberships(
    _id : ObjectId = None,
    user_id: ObjectId = None, 
    club_id: ObjectId = None, 
    role_id: ObjectId = None,
    is_admin: bool = None
) -> list | None:

    if _id is None and user_id is None and club_id is None and role_id is None and is_admin is None:
        raise ValueError("All fields are compulsory")

    query_filter = dict()

    if _id is not None:
        query_filter.update({"_id" : _id})
    if user_id is not None:
        query_filter.update({"user_id" : user_id})
    if club_id is not None:
        query_filter.update({"club_id" : club_id})
    if role_id is not None:
        query_filter.update({"role_id" : role_id})
    if is_admin is not None:
        query_filter.update({"is_admin" : is_admin})
    
    memberships = list()

    with db.memberships.find(filter=query_filter) as cursor:
        for doc in cursor:
            memberships.append(Membership.conv_to_obj(doc))

    if memberships == []:
        return None
    else:
        return memberships
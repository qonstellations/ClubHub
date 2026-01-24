from app.db.models import Role, ObjectId
from app.db.client import db

def insert_role(
    name: str,
    club_id: ObjectId
) -> Role:
    role = Role(
        _id=None,
        name=name,
        club_id=club_id,
        count=1
    )

    new_role_id = db.roles.insert_one(role.conv_to_doc()).inserted_id
    role._id = new_role_id

    return role

def find_roles(
    _id : ObjectId = None,
    name: str = None,
    club_id : str = None
)-> list | None:
    
    query_filter = dict()

    if _id is not None:
        query_filter.update({"_id" : _id})
    if name is not None:
        # searches name even with first few keywords
        query_filter.update({"name" : {"$regex": f"^{name}", "$options": "i"}})
    if club_id is not None:
        query_filter.update({"club_id" : club_id})
    
    if _id is None and name is None and club_id is None:
        raise ValueError("Atleast one query must be specified for search")
    
    roles = list()

    with db.roles.find(filter=query_filter) as cursor:
        for doc in cursor:
            roles.append(Role.conv_to_obj(doc))

    if roles == []:
        return None
    else:
        return roles
    
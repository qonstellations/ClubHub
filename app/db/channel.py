from app.db.models import Channel, ObjectId
from app.db.client import db

def insert_channel(
    club_id: ObjectId,
    name: str,
    created_by: ObjectId
) -> Channel:

    channel = Channel(
        _id=None,
        club_id=club_id,
        name=name,
        created_by=created_by,
        created_at=datetime.now()
    )

    new_channel_id = db.channels.insert_one(channel.conv_to_doc()).inserted_id
    channel._id = new_channel_id

    return channel

def find_channels(
    _id : ObjectId = None,
    club_id: ObjectId = None,
    name: str = None,
) -> list | None:

    query_filter = dict()

    if _id is not None:
        query_filter.update({"_id" : _id})
    elif club_id is not None:
        query_filter.update({"club_id" : club_id})
    elif name is not None:
        # searches name even with first few keywords
        query_filter.update({"name" : {"$regex": f"^{name}", "$options": "i"}})
    else:
        raise ValueError("Atleast one query must be specified for search")
    
    channels = list()

    with db.channels.find(filter=query_filter) as cursor:
        for doc in cursor:
            channels.append(Channel.conv_to_obj(doc))

    if channels == []:
        return None
    else:
        return channels
from app.db.channel import Channel, ObjectId, find_channels, insert_channel
from app.db.club import Club
from app.db.user import User
from app.core.user import is_admin

def get_club_channels(
    club : Club
) -> list:
    channels = find_channels(club_id=club._id)

    return channels

@is_admin
def create_channel(
    club: Club,
    name: str,
    user: User,
) -> Channel:
    
    if name is None or not user or not club:
        raise ValueError("All fields are compulsory")
    
    channel = insert_channel(
        club_id=club._id,
        name=name,
        created_by=user._id
    )

    return channel
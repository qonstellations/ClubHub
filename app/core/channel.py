from app.db.channel import ObjectId, find_channels, insert_channel
from app.db.club import Club
from app.core.user import is_admin

def get_club_channels(
    club : Club
) -> list:
    channels = find_channels(club_id=club._id)

    if channels is None:
        raise ValueError("No channels found!")
    else:
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
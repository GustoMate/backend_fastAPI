from sqlalchemy.orm import Session
from ..database.models import Friends, Users

def get_friends(db: Session, user_id: int):
    friends = db.query(Friends).filter(Friends.user_id == user_id).all()
    friend_details = []
    for friend in friends:
        user = db.query(Users).filter(Users.user_id == friend.friend_id).first()
        if user:
            friend_details.append({
                "friend_id": user.user_id,
                "friend_name": user.username,
                "friend_email": user.useremail,
                "created_at": friend.created_at,
                "updated_at": friend.updated_at
            })
    return friend_details

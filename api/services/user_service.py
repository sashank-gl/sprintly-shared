from models.user import User
from extensions import db

def get_user(user_id):
    return User.query.get_or_404(user_id)


def update_avatar(user_id, avatar_url):
    user = User.query.get_or_404(user_id)
    user.avatar_url = avatar_url
    db.session.commit()
    return user


def remove_avatar(user_id):
    user = User.query.get_or_404(user_id)
    user.avatar_url = None
    db.session.commit()
    return user
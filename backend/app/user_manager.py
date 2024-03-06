from app import db, login
from app.models import User

import sqlalchemy as sa
from flask_login import login_user, logout_user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


def user_sign_up(username, password):
    # Check if user exists
    query = sa.select(User).where(User.username.like(username))
    user = db.session.scalars(query).first()
    if user:
        return "exists"
    
    # Add user to database
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    # Login user
    login_user(new_user)
    return "success"


def user_login(username, password):
    # Query user database
    query = sa.select(User).where(User.username.like(username))
    user = db.session.scalars(query).first()

    # Check for login success
    if user and user.check_password(password):
        login_user(user)
        return True
    
    # Handle login failure
    return False


def user_logout():
    logout_user()
    return True
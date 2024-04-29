from app import db, login
from app.models import User
from app import sql_utils
import sqlalchemy as sa
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


def user_sign_up(username, password):
    # Check if user exists
    query = sa.select(User).where(User.username.like(username))
    user = db.session.scalars(query).first()
    if user:
        return None
    
    # Add user to database
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    # Add default list to SEASONS table
    season_names = ["MLB 2020", "MLB 2021", "MLB 2022", "MLB 2023", "MLB 2024"]
    for season_name in season_names:
        record = {
            "user_id": new_user.id,
            "name": season_name,
        }
        sql_utils.insert_record("SEASONS", record)

    # Complete login process
    user_login(username, password)


def user_login(username, password):

    # Retrieve user from database
    query = sa.select(User).where(User.username.like(username))
    user = db.session.scalars(query).first()

    # Handle login success
    if user and user.check_password(password):
        login_user(user)
        token = create_access_token(identity=user.id)
        ids, names = sql_utils.get_cols("SEASONS", ["id", "name"], 
                                        "user_id",  user.id, sort="DESC")
        return {
            "token": token,
            "season_names": names,
            "season_ids": ids,
        }
    
    return None


def user_logout():
    logout_user()
    return True
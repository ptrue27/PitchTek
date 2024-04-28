from app import db, login
from app.models import User
from config import Config

import sqlite3
import os
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
    seasons = ["MLB 2024", "MLB 2023", "MLB 2022"]
    for season in seasons:
        add_season(new_user.id, season)

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
        ids, names = get_seasons(user.id)
        return {
            "token": token,
            "season_names": names,
            "season_ids": ids,
        }
    
    return None


def user_logout():
    logout_user()
    return True


def get_seasons(user_id):
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, Config.APP_DB))
    cursor = conn.cursor()

    # SQL query to fetch all seasons for the given user_id
    select_query = """
        SELECT id, name
        FROM SEASONS
        WHERE user_id = ?
    """
    
    # Execute the query with the provided user_id
    cursor.execute(select_query, (user_id,))
    seasons = cursor.fetchall()

    # Separate the IDs and the names into two distinct lists
    ids = []
    names = []
    for row in seasons:
        ids.append(row[0])
        names.append(row[1])

    # Close the connection
    cursor.close()
    conn.close()

    return ids, names


def add_season(user_id, season_name, get_id=False):
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, Config.APP_DB))
    cursor = conn.cursor()

    # SQL query to insert a new season
    insert_query = """
        INSERT INTO SEASONS (user_id, name) VALUES (?, ?)
    """
    cursor.execute(insert_query, (user_id, season_name))
    conn.commit()

    # Get the ID of the newly inserted record if requested
    if get_id:
        new_season_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return new_season_id
    
    cursor.close()
    conn.close()
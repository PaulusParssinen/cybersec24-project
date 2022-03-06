from flask import session, current_app
from chatapp.db import db
from werkzeug.security import check_password_hash, generate_password_hash, secrets

def create(username, password):
    password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, { "username": username, "password": password_hash})
        db.session.commit()
    except BaseException as ex:
        current_app.logger.error(ex)
        return False
    return login(username, password)

def get(id):
    sql = "SELECT * FROM users WHERE id=:id"
    return db.session.execute(sql, { "id": id }).fetchone()

def get_user_group(user_id):
    user = get(user_id)
    sql = "SELECT id, rank, name FROM user_groups WHERE id=:id"
    return db.session.execute(sql, { "id": user.user_group_id }).fetchone()

def get_user_group_by_name(group_name):
    sql = "SELECT id, rank, name FROM user_groups WHERE name=:name"
    return db.session.execute(sql, { "name": group_name }).fetchone()

def update(id, username): 
    try:
        sql = "UPDATE users SET username=:username WHERE id=:id RETURNING *"
        result = db.session.execute(sql, { "id": id, "username": username })
        db.session.commit()
        return result.fetchone()
    except BaseException as ex:
        current_app.logger.error(ex)
    return None

def add_avatar(): pass

def delete(id):
    try:
        sql = "DELETE FROM users WHERE id=:id"
        db.session.execute(sql, { "id": id })
        db.session.commit()
        return True
    except BaseException as ex:
        current_app.logger.error(ex)
    return False

def login(username, password):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, { "username": username })
    user = result.fetchone()
    
    if user and check_password_hash(user.password, password):
        populate_session(user)
        return True
    return False

def session_has_rank(min_rank):
    user_id = current_user_id()
    if not user_id: 
        return False
    return has_rank(user_id, min_rank)

def session_has_group(group_name):
    user_id = current_user_id()
    if not user_id: 
        return False
    return has_group(user_id, group_name)

def has_group(user_id, group_name):
    required_group = get_user_group_by_name(group_name)
    return has_rank(user_id, required_group.rank)

def has_rank(user_id, min_rank):
    user_group = get_user_group(user_id)
    # Is the users rank equal or greater than the required group rank
    return min_rank <= user_group.rank
    
def populate_session(user):
    session["id"] = user.id
    session["username"] = user.username
    session["csrf_token"] = secrets.token_hex(16)

def logout(): 
    session.pop("id", None)
    session.pop("username", None)
    session.pop("crsf_token", None)

def current_user_id():
    return session.get("id", 0)
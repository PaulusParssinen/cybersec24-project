from flask import session, current_app
from chatapp.db import db
from werkzeug.security import check_password_hash, generate_password_hash

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
    result = db.session.execute(sql, { "id": id })
    return result.fetchone()

def update(user_id, username=None, password=None): pass
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

def populate_session(user):
    session["id"] = user.id
    session["username"] = user.username

def logout(): 
    session.pop("id", None)
    session.pop("username", None)

def current_user_id():
    return session.get("id", 0)
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
    
def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, { "username": username })
    user = result.fetchone()
    
    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        return True
    return False

def delete(user_id): pass
def edit(): pass

def logout(): 
    del session["user_id"]

def current_user_id():
    return session.get("user_id", 0)
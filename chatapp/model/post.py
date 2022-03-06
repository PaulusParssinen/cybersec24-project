from flask import session, current_app
from chatapp.db import db

def create(thread_id, user_id, body):
    try:
        sql = "INSERT INTO posts (thread_id, user_id, content_body) VALUES (:thread_id, :user_id, :content_body) RETURNING id"
        result = db.session.execute(sql, { "thread_id": thread_id, "user_id": user_id, "content_body": body })
        db.session.commit()
        return result.fetchone()
    except BaseException as ex:
        current_app.logger.error(ex)
    return None

def get(id):
    sql = "SELECT * FROM posts WHERE id=:id"
    return db.session.execute(sql, { "id": id }).fetchone()

def get_all(thread_id):
    sql = "SELECT * FROM posts WHERE thread_id=:thread_id ORDER BY id"
    return db.session.execute(sql, { "thread_id": thread_id })

def update(id, body):
    try:
        sql = "UPDATE posts SET content_body=:content_body WHERE id=:id RETURNING *"
        result = db.session.execute(sql, { "id": id, "content_body": body })
        db.session.commit()
        return result.fetchone()
    except BaseException as ex:
        current_app.logger.error(ex)
    return None

def delete(id):
    try:
        sql = "DELETE FROM posts WHERE id=:id"
        db.session.execute(sql, { "id": id })
        db.session.commit()
        return True
    except BaseException as ex:
        current_app.logger.error(ex)

def search(text):
    sql = "SELECT * FROM posts WHERE content_body LIKE :text"
    return db.session.execute(sql, { "text": "%" + text + "%" })
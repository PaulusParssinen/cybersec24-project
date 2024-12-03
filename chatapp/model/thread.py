from flask import session, current_app
from chatapp.db import db

def create(board_id, user_id, title, body):
    try:
        sql = "INSERT INTO threads (board_id, user_id, title, content_body) VALUES (:board_id, :user_id, :title, :content_body) RETURNING id"
        result = db.session.execute(sql, { "board_id": board_id, "user_id": user_id, "title": title, "content_body": body })
        thread_id = result.fetchone()
        db.session.commit()
        return thread_id
    except BaseException as ex:
        current_app.logger.error(ex)
    return None

def get(id):
    sql = "SELECT * FROM threads WHERE id=:id"
    return db.session.execute(sql, { "id": id }).fetchone()

def get_recent_threads(board_id, count=5):
    sql = "SELECT * FROM threads WHERE board_id=:board_id ORDER BY id DESC LIMIT :count"
    return db.session.execute(sql, { "board_id": board_id, "count": count })

def update(id, title, body):
    try:
        sql = "UPDATE threads SET title=:title, content_body=:content_body WHERE id=:id RETURNING id"
        result = db.session.execute(sql, { "id": id, "title": title, "content_body": body })
        thread_id = result.fetchone().id
        db.session.commit()
        return thread_id
    except BaseException as ex:
        current_app.logger.error(ex)
    return None

def delete(id):
    try:
        sql = "DELETE FROM threads WHERE id=:id"
        db.session.execute(sql, { "id": id })
        db.session.commit()
        return True
    except BaseException as ex:
        current_app.logger.error(ex)
    return False
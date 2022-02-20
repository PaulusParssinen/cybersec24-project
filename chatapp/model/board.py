from flask import session, current_app
from chatapp.db import db

def create(name, description, min_rank=0):
    try:
        sql = "INSERT INTO boards (name, description, min_user_rank) VALUES (:name, :description, :min_user_rank) RETURNING id"
        result = db.session.execute(sql, { "name": name, "description": description, "min_user_rank": min_rank })
        db.session.commit()
        return result.fetchone()
    except BaseException as ex:
        current_app.logger.error(ex)
    return None

def get(id):
    sql = "SELECT * FROM boards WHERE id=:id"
    return db.session.execute(sql, { "id": id }).fetchone()

def get_all():
    return db.session.execute("SELECT * FROM boards")

def get_board_view(board_id):
    sql = "SELECT t.id, t.title as title, p.id AS last_post_id, p.created_at AS last_created_at FROM threads AS t " \
        "LEFT JOIN posts p ON t.id=p.thread_id WHERE t.board_id=:board_id AND "\
            "(p.id IS NULL OR "\
                "p.id IN (SELECT MAX(id) FROM posts GROUP BY thread_id))"
    
    return db.session.execute(sql, { "board_id": board_id })

def delete(id):
    try:
        sql = "DELETE FROM boards WHERE id=:id"
        db.session.execute(sql, { "id": id })
        db.session.commit()
        return True
    except BaseException as ex:
        current_app.logger.error(ex)
    return False
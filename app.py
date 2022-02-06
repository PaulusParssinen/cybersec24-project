from os import getenv
from flask import Flask

from chatapp.db import db
from chatapp.routes import root_bp, user_bp, board_bp, thread_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.secret_key = getenv("SECRET_KEY")
    
    # Init database
    db.init_app(app)
    
    # Register routes
    app.register_blueprint(root_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(board_bp)
    app.register_blueprint(thread_bp)
    
    return app
from os import getenv
from datetime import datetime

from flask import Flask

from chatapp.db import db
from chatapp.limiter import limiter
from chatapp.route import root_bp, user_bp, board_bp, thread_bp, moderation_bp
from chatapp.model.user import is_admin, is_mod

def format_short_date(value):
    return datetime.fromisoformat(str(value)).strftime("%x")

def format_date(value):
    return datetime.fromisoformat(str(value)).strftime("%x %X")

def get_username_filter(id):
    sql = "SELECT username FROM users WHERE id=:id"
    return db.session.execute(sql, { "id": id }).fetchone().username

def create_app(show_routes=False):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config["AVATAR_DIRECTORY"] = getenv("AVATAR_DIRECTORY")
    app.secret_key = getenv("SECRET_KEY")
    
    app.logger.setLevel(getenv("LOG_LEVEL", "INFO"))

    # Init database
    db.init_app(app)

    # If the database is in memory, we need seed it with schema.sql:
    if app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:":
        with app.app_context():
          app.logger.info("In-memory database configuration detected, creating database schema..")
          with db.engine.connect() as connection:
            underlying_connection = connection.connection
            cursor = underlying_connection.cursor()
            try:
              with open("schema.sql") as f:
                cursor.executescript(f.read())
              underlying_connection.commit()
            except Exception as e:
              underlying_connection.rollback()
              print(f"Error initializing database: {e}")
            finally:
              cursor.close()
              app.logger.info("In-memory database schema created!")
    
    # Initializer Rate Limiter
    limiter.init_app(app)

    # Register Jinja filter
    app.jinja_env.filters["username"] = get_username_filter
    app.jinja_env.filters["short_date"] = format_short_date
    app.jinja_env.filters["date"] = format_date
    
    # Register global Jinja helper fucntions
    app.jinja_env.globals['is_mod'] = is_mod
    app.jinja_env.globals['is_admin'] = is_admin
    
    # Register routes
    app.register_blueprint(root_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(board_bp)
    app.register_blueprint(thread_bp)
    app.register_blueprint(moderation_bp)
    
    if (show_routes):
        print(app.url_map)
    
    return app
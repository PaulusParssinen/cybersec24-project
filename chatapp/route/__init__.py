from functools import wraps
from flask import url_for, request, redirect, session, flash

from chatapp.model.user import get_user_group, get_user_group_by_name

# CSRF token verification
def csrf(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST" and session["csrf_token"] != request.form["csrf_token"]:
            flash("Invalid Cross-site Request Forgery token was detected.", "warning")
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

# Decorators to reduce duplicate access control code

# Routes that can be only navigated when session is not authenticated
def guest(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id", 0):
            return redirect(url_for("root.index"))
        return f(*args, **kwargs)
    return decorated_function

# Routes only for authenticated users
def authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("id", 0):
            return redirect(url_for("root.login"))
        return f(*args, **kwargs)
    return decorated_function

# Routes that require user's group rank to be atleast min_rank
def rank_required(min_rank):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            session_id = session.get("id", 0)
            if not session_id:
                flash("You must be authenticated to access that resource.", "info")
                return redirect(url_for("root.login"))

            user_group = user.get_user_group(session_id)
            if min_rank > user_group.rank:
                flash("You do not have permission to view that resource!", "error")
                return redirect(url_for("root.index"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Routes that require user's group to be group_name, or group of higher rank.
def group_required(group_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            session_id = session.get("id", 0)
            if not session_id:
                flash("You must be authenticated to access that resource.", "info")
                return redirect(url_for("root.login"))
            
            user_group = get_user_group(session_id)
            min_required_group = get_user_group_by_name(group_name)
            if min_required_group.rank > user_group.rank:
                flash("You do not have permission to view that resource!", "error")
                return redirect(url_for("root.index"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

from chatapp.route.root import root_bp
from chatapp.route.user import user_bp
from chatapp.route.board import board_bp
from chatapp.route.thread import thread_bp
from chatapp.route.moderation import moderation_bp
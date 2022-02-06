from flask import Blueprint, render_template, request, redirect, flash, url_for
from chatapp.model import user, board, thread, post

# TODO: Split 'em up to own files
root_bp = Blueprint('root', __name__)
user_bp = Blueprint('user', __name__, url_prefix='/user')
board_bp = Blueprint('board', __name__, url_prefix='/board')
thread_bp = Blueprint('thread', __name__, url_prefix='/thread')

@root_bp.route('/')
def index():
     # TODO: Threads for each board
     # TODO: Pull the most recent post for each recent thread
     
     # Temporarily hardcoded objects to show what it'd look like :D
     last_reply = { 'id': 2051, 'created_at': '2051-01-01' }
     threads = [
          { 'id': 1337, 'title': "I thought what I'd do was, I'd pretend I was one of those deaf-mutes", 'last_reply': last_reply },
          { 'id': 1338, 'title': "Lorem ipsum dolor sit amet", 'last_reply': last_reply },
          { 'id': 1339, 'title': "Lorem ipsum dolor sit amet", 'last_reply': last_reply },
          { 'id': 1340, 'title': "Lorem ipsum dolor sit amet", 'last_reply': last_reply },
          { 'id': 1341, 'title': "Lorem ipsum dolor sit amet", 'last_reply': last_reply },
          { 'id': 1342, 'title': "Lorem ipsum dolor sit amet", 'last_reply': last_reply }
     ]
     boards = [{ 'name': 'General board', 'recent_threads': threads}]
     return render_template("index.j2", boards=boards)

@root_bp.route('/login', methods=["GET", "POST"])
def login():
     if request.method == "GET":
          return render_template("login.j2")
     
     if request.method == "POST":
          username = request.form["username"]
          password = request.form["password"]
          if user.login(username, password):
               return redirect(url_for('root.index'))
          else:
               flash("Details did not match with any user.", "error")
               return redirect(url_for("root.login"))

@root_bp.route("/logout")
def logout():
    user.logout()
    return redirect(url_for('root.index'))

@root_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
         return render_template("register.j2")
    
    if request.method == "POST":
         username = request.form["username"]
         password = request.form["password"]
         password_again = request.form["password_again"]
         
         if password != password_again:
              flash("The passwords don't match!", "error")
              return redirect(url_for('root.register'))
         
         if user.create(username, password):
              return redirect(url_for('root.index'))
         else:
              flash("Registration failed. Try another username", "error")
              return redirect(url_for('root.register'))

@user_bp.route("/<int:user_id>", methods=["GET"])
def show_profile(user_id): pass

@user_bp.route("/<int:user_id>/edit", methods=["POST"])
def edit_profile(user_id): pass

# TODO: Moderation

# Boards
@board_bp.route("/<int:board_id>", methods=["GET"])
def index(board_id): pass

@board_bp.route("/create", methods=["GET", "POST"])
def create_board(): pass

@board_bp.route("/<int:board_id>", methods=["DELETE"])
def delete_board(board_id): pass

@board_bp.route("/<int:board_id>", methods=["POST"])
def create_thread(board_id): pass

# Threads
@thread_bp.route("/<int:thread_id>")
def show_thread(thread_id): pass

@thread_bp.route("/<int:thread_id>/edit", methods=["POST"])
def edit_thread(thread_id): pass

@thread_bp.route("/<int:thread_id>", methods=["DELETE"])
def delete_thread(thread_id): pass

# Post aka "reply" specific routes
@thread_bp.route("/<int:thread_id>", methods=["POST"])
def add_reply(thread_id): pass

@thread_bp.route("/<int:thread_id>/<int:post_id>/edit", methods=["POST"])
def edit_reply(thread_id, post_id): pass

@thread_bp.route("/<int:thread_id>/<int:post_id>", methods=["DELETE"])
def delete_reply(thread_id, post_id): pass
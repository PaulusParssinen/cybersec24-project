from flask import Blueprint, render_template, request, redirect, flash, url_for
from chatapp.model import user, board, thread, post

# TODO: Split 'em up to own files
root_bp = Blueprint('root', __name__)
user_bp = Blueprint('user', __name__, url_prefix='/user')
board_bp = Blueprint('board', __name__, url_prefix='/board')
thread_bp = Blueprint('thread', __name__, url_prefix='/thread')
mod_bp = Blueprint('mod', __name__, url_prefix='/moderation')

@root_bp.route('/')
def index():
    # TODO: pass threads somehow
    return render_template("index.j2", boards=board.get_all())

@root_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.j2")

    username = request.form["username"]
    password = request.form["password"]
    if not user.login(username, password):
        flash("Details did not match with any user.", "error")
        return redirect(url_for("root.login"))
    
    flash("Logged in!", "success")
    return redirect(url_for('root.index'))

@root_bp.route("/logout")
def logout():
    user.logout()
    flash("Logged out", "info")
    return redirect(url_for('root.index'))

@root_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.j2")

    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]

    if password != password_again:
        flash("The passwords don't match!", "error")
        return redirect(url_for('root.register'))

    if not user.create(username, password):
        flash("Registration failed. Try another username", "error")
        return redirect(url_for('root.register'))

    return redirect(url_for('root.index'))

@user_bp.route("/<int:user_id>", methods=["GET"])
def show_profile(user_id):
    return render_template("profile.j2", user=user.get(user_id))

@user_bp.route("/<int:user_id>/edit", methods=["POST"])
def edit_profile(user_id): pass

# TODO: Moderation

# Boards
@board_bp.route("/<int:board_id>", methods=["GET"])
def show_board(board_id): 
    return render_template("board.j2", board=board.get(board_id), threads=board.get_board_view(board_id))

@board_bp.route("/create", methods=["GET", "POST"])
def create_board():
    if request.method == "GET":
        return render_template("create_board.j2")
    
    name = request.form["name"]
    description = request.form["description"]
    board_id = board.create(name, description)
    
    if board_id is None:
        flash("Failed to create a board", "error")
        return redirect(url_for('board.create_board', board_id=board_id))
    
    flash("Thread created succesfully!", "success")
    return redirect(url_for('thread.show_thread', thread_id=thread_id))

@board_bp.route("/<int:board_id>/new", methods=["GET", "POST"])
def create_thread(board_id):
    if request.method == "GET":
        return render_template("create_thread.j2", board_id=board_id)
    
    title = request.form["title"]
    body = request.form["body"]
    created_thread = thread.create(board_id, user.current_user_id(), title, body)
    
    if created_thread is None:
        flash("Failed to create a thread", "error")
        return redirect(url_for('board.create_thread', board_id=board_id))
    
    flash("Thread created succesfully!", "success")
    return redirect(url_for('thread.show_thread', thread_id=created_thread.id))

@board_bp.route("/<int:board_id>/delete", methods=["POST"])
def delete_board(board_id):
    board.delete(board_id)
    
    flash("Board deleted!", "info")
    return redirect(url_for('root.index'))

# Threads
@thread_bp.route("/<int:thread_id>")
def show_thread(thread_id):
    posts = post.get_all(thread_id)
    return render_template("thread.j2", thread=thread.get(thread_id), posts=posts)

@thread_bp.route("/<int:thread_id>/edit", methods=["GET", "POST"])
def edit_thread(thread_id):
    if request.method == "GET":
        return render_template("edit_thread.j2", thread=thread.get(thread_id))
    
    title = request.form["title"]
    body = request.form["body"]
    edited_thread = thread.update(thread_id, title, body)
    
    if edited_thread is None:
        flash("Failed to edit the thread", "error")
        return redirect(url_for('board.show_thread', board_id=board_id))
    
    flash("Thread was edited succesfully!", "success")
    return redirect(url_for('thread.show_thread', thread_id=edited_thread.id))

@thread_bp.route("/<int:thread_id>/delete", methods=["POST"])
def delete_thread(thread_id):
    thread.delete(thread_id)
    
    flash("Thread deleted!", "info")
    return redirect(url_for('root.index'))

# Posts
@thread_bp.route("/<int:thread_id>", methods=["POST"])
def add_post(thread_id):
    created_post = post.create(thread_id, user.current_user_id(), request.form["body"])
    if created_post is None:
        flash("Failed to create a post", "error")
    else: 
        flash("Post added succesfully", "success")
    
    return redirect(url_for('thread.show_thread', thread_id=thread_id))

@thread_bp.route("/<int:thread_id>/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(thread_id, post_id):
    if request.method == "GET":
        return render_template("edit_post.j2", post=post.get(post_id))
    
    edited_post = post.update(post_id, request.form["body"])
    
    if edited_post is None:
        flash("Failed to edit the thread", "error")
        return redirect(url_for('board.show_thread', board_id=board_id))
    
    flash("Thread was edited succesfully!", "success")
    return redirect(url_for('thread.show_thread', thread_id=edited_post.thread_id))

@thread_bp.route("/<int:thread_id>/<int:post_id>/delete", methods=["POST"])
def delete_post(thread_id, post_id):
    post.delete(post_id)
    
    flash("Post deleted!", "info")
    return redirect(url_for('root.index'))
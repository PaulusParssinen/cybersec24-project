from flask import Blueprint, render_template, request, redirect, flash, url_for
from chatapp.model import user, board, thread, post
from chatapp.route import authenticated, group_required, csrf

board_bp = Blueprint("board", __name__, url_prefix="/board")

@board_bp.route("/<int:board_id>", methods=["GET"])
def show_board(board_id): 
    return render_template("board.j2", 
        board=board.get(board_id), 
        threads=board.get_board_view(board_id))

@board_bp.route("/create", methods=["GET", "POST"])
@group_required("Administrator")
# @csrf
def create_board():
    if request.method == "GET":
        return render_template("create_board.j2")
    
    name = request.form["name"].strip()
    description = request.form["description"].strip()
    board_id = board.create(name, description)
    
    if not board_id:
        flash("Failed to create a board", "error")
        return redirect(url_for("board.create_board"))
    
    flash("Board created succesfully!", "success")
    return redirect(url_for("board.show_board", board_id=board_id))

@board_bp.route("/<int:board_id>/new", methods=["GET", "POST"])
@authenticated
# @csrf
def create_thread(board_id):
    if request.method == "GET":
        return render_template("create_thread.j2", board_id=board_id)
    
    title = request.form["title"].strip()
    body = request.form["body"].strip()
    created_thread = thread.create(board_id, user.current_user_id(), title, body)
    
    if not created_thread:
        flash("Failed to create a thread", "error")
        return redirect(url_for("board.create_thread", board_id=board_id))
    
    flash("Thread created succesfully!", "success")
    return redirect(url_for("thread.show_thread", thread_id=created_thread.id))

@board_bp.route("/<int:board_id>/delete", methods=["POST"])
@group_required("Administrator")
# @csrf
def delete_board(board_id):
    board.delete(board_id)
    
    flash("Board deleted!", "info")
    return redirect(url_for("root.index"))

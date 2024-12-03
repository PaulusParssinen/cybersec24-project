from flask import Blueprint, render_template, request, redirect, flash, url_for
from chatapp.model import user, board, thread, post
from chatapp.route import authenticated, csrf

thread_bp = Blueprint("thread", __name__, url_prefix="/thread")

@thread_bp.route("/<int:thread_id>")
def show_thread(thread_id):
    posts = post.get_all(thread_id)
    return render_template("thread.j2", thread=thread.get(thread_id), posts=posts)

@thread_bp.route("/<int:thread_id>/edit", methods=["GET", "POST"])
@authenticated
# @csrf
def edit_thread(thread_id):
    if request.method == "GET":
        return render_template("edit_thread.j2", thread=thread.get(thread_id))
    
    title = request.form["title"].strip()
    body = request.form["body"].strip()
    
    has_error = False
    if not title:
        flash("Empty thread title is not allowed", error)
        has_error |= True
    
    if not body:
        flash("Empty thread body is not allowed", error)
        has_error |= True
    
    if has_error:
        return redirect(url_for('thread.edit_thread', thread_id=thread_id))
    
    thread_id = thread.update(thread_id, title, body)
    
    if not thread_id:
        flash("Failed to edit the thread", "error")
        return redirect(url_for('thread.edit_thread', thread_id=thread_id))
    
    flash("Thread was edited succesfully!", "success")
    return redirect(url_for("thread.show_thread", thread_id=thread_id))

@thread_bp.route("/<int:thread_id>/delete", methods=["GET"])
@authenticated
def delete_thread(thread_id):
    thread.delete(thread_id)
    
    flash("Thread deleted!", "info")
    return redirect(url_for("root.index"))

@thread_bp.route("/<int:thread_id>", methods=["POST"])
@authenticated
# @csrf
def add_post(thread_id):
    created_post = post.create(thread_id, user.current_user_id(), request.form["body"])
    if not created_post:
        flash("Failed to create a post", "error")
    else: 
        flash("Post added succesfully", "success")
    
    return redirect(url_for("thread.show_thread", thread_id=thread_id))

@thread_bp.route("/<int:thread_id>/<int:post_id>/edit", methods=["GET", "POST"])
@authenticated
# @csrf
def edit_post(thread_id, post_id):
    if request.method == "GET":
        return render_template("edit_post.j2", post=post.get(post_id))
    
    edited_post = post.update(post_id, request.form["body"].strip())
    
    if not edited_post:
        flash("Failed to edit the post", "error")
        return redirect(url_for("board.show_thread", thread_id=thread_id))
    
    flash("Post was edited succesfully!", "success")
    return redirect(url_for("thread.show_thread", thread_id=edited_post.thread_id))

@thread_bp.route("/<int:thread_id>/<int:post_id>/delete", methods=["GET"])
@authenticated
def delete_post(thread_id, post_id):
    post.delete(post_id)
    
    flash("Post deleted!", "info")
    return redirect(url_for("root.index"))
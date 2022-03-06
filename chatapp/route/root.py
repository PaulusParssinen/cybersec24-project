from flask import Blueprint, render_template, request, redirect, flash, url_for
from chatapp.model import user, board, thread, post

root_bp = Blueprint("root", __name__)

@root_bp.route("/")
def index():
    # TODO: pass threads somehow
    return render_template("index.j2", boards=board.get_all())

@root_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.j2")

    username = request.form["username"]
    password = request.form["password"]
    if not user.login(username, password):
        flash("Details did not match with any user.", "error")
        return redirect(url_for("root.login"))
    
    flash("Logged in!", "success")
    return redirect(url_for("root.index"))

@root_bp.route("/logout")
def logout():
    user.logout()
    flash("Logged out", "info")
    return redirect(url_for("root.index"))

@root_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.j2")

    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]

    if password != password_again:
        flash("The passwords don't match!", "error")
        return redirect(url_for("root.register"))

    if not user.create(username, password):
        flash("Registration failed. Try another username", "error")
        return redirect(url_for("root.register"))

    return redirect(url_for("root.index"))

@root_bp.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.j2")

    query = request.form["query"].strip()

    if not query:
        flash("The search query was empty. Please provide valid search query.", "error")
        return redirect(url_for("root.search"))
    
    query_results = post.search(query)
    
    if not query_results:
        flash("No results were found for the search query!", "error")
        return redirect(url_for("root.search"))

    return render_template("search_results.j2", query=query, results=query_results)
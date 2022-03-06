from flask import Blueprint, render_template, request, redirect, flash, url_for
from chatapp.model import user
from chatapp.route import authenticated

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/<int:user_id>", methods=["GET"])
@authenticated
def show_profile(user_id):
    return render_template("profile.j2", user=user.get(user_id))

@user_bp.route("/<int:user_id>/edit", methods=["POST"])
@authenticated
def edit_profile(user_id):
    edited_post = user.update(user_id, request.form["username"])
    
    if not edited_post:
        flash("Failed to edit the user profile", "error")
        return redirect(url_for("user.show_profile", user_id=user_id))
    
    flash("User profile was edited succesfully!", "success")
    return redirect(url_for("user.show_profile", user_id=user_id))
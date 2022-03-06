from flask import Blueprint, render_template, request, redirect, flash, url_for
from chatapp.model import user

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/<int:user_id>", methods=["GET"])
def show_profile(user_id):
    return render_template("profile.j2", user=user.get(user_id))

@user_bp.route("/<int:user_id>/edit", methods=["POST"])
def edit_profile(user_id): pass
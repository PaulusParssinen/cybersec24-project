from flask import Blueprint, render_template, request, redirect, flash, url_for
from chatapp.model import user, board, thread, post
from chatapp.route import group_required

moderation_bp = Blueprint("moderation", __name__, url_prefix="/moderation")

@moderation_bp.route("/")
@group_required("Moderator")
def index():
    return render_template('moderation_dashboard.j2')
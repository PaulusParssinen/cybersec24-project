from flask import Blueprint, render_template, request, redirect, flash, url_for
from chatapp.model import user, board, thread, post

moderation_bp = Blueprint('moderation', __name__, url_prefix='/moderation')
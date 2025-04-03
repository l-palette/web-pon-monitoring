from flask import Blueprint

view_bp = Blueprint('view', __name__)

from .view import *

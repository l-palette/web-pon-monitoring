from flask import Blueprint

register_bp = Blueprint('register', __name__)

from .register import *

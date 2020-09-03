from flask import Blueprint

bp = Blueprint('auth', __name__)

from srcode.auth import routes1
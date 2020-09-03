from flask import Blueprint

bp = Blueprint('user', __name__)

from srcode.user import routes
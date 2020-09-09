from flask import Blueprint

community = Blueprint('community', __name__)

from srcode.community import routes
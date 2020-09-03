from srcode import app
from flask import render_template
from srcode.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
     return render_template('errors/404.html')

@bp.app_errorhandler(500)
def internal_error(error):
     #db.session.rollback()
     return render_template('errors/500.html')
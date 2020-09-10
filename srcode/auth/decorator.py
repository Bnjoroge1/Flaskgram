from flask import flash, redirect, url_for, abort
from flask_login import current_user
from srcode.models import Permission, User
from functools import wraps

def check_confirmed(func):
    '''Checks whether a certain user is confirmed''' 
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if  not current_user.confirmed:
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

def permission_required(permission):
    '''Incase any view functions(routes) are needed to be displayed we call the decorators'''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    '''Admin required decorator can be used incase any routes are needed'''
    return permission_required(Permission.ADMINISTER)(f)   

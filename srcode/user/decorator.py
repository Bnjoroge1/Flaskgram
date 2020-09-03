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
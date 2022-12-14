from functools import wraps
from flask import redirect, flash, url_for
from flask_login import current_user
from app.extensions import login
from app.models import User
from app.app import app
from app.app_setup import setup


# This callback is used to reload the user object from the user ID stored in the session. It should take the str ID of a user, and return the corresponding user object.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Before first request create tables in the database
@app.before_first_request
def init():
    setup()


# Decorator to authorize access by roles
def role_required(role):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role == role:
                return func(*args, **kwargs)
            else:
                flash('You don\'t have permissions to access this page.', 'error')
                return redirect(url_for('home'))
        return wrapper
    return actual_decorator

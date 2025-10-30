from functools import wraps
import flask
from flask import redirect, url_for, flash
from flask_login import current_user


def roles_required(*roles):
    def wrapper(func):
        def decorator(*args, **kwargs):
            if not current_user.is_authenticated:
                flask.abort(401)
                return redirect(url_for('login'))
            if not current_user.role or not current_user.role in roles:
                flask.abort(403)
                return redirect(url_for('index'))
            return func(*args, **kwargs)
        return decorator()
    return wrapper
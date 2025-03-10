from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
import json
from flask import request

def admin_required(f):
    """
    Decorator to restrict access to admin users only.
    Redirects non-admin or unauthenticated users to the home page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is authenticated and an admin
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)

    return decorated_function

def get_user_from_cookie():
    user_data = request.cookies.get('user_data')
    if not user_data:
        return None
    try:
        return json.loads(user_data)
    except json.JSONDecodeError:
        return None

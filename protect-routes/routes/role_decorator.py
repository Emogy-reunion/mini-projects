from functools import wraps
from flask_login import current_user
from flask import redirect, url_for

def role_required(role):
    '''
    - This function is a decorator that checks the current user's role
    - It takes a single argument role - role required to access resource
    - If the user's role doesn't match the required role, they are redirected to
      unauthorized page
    - It returns a decorator
    '''

    def wrapper(f):
        @wraps(f)

        def decorated_function(*args, **kwargs):
            # check user roles
            if current_user.role != role:
                return redirect(url_for('dash.unauthorized'))
            return f(*args, **kwargs)

        return decorated_function
    return wrapper

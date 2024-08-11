'''
This module handles updating posts and user profile
edit blueprint is registered and used to create routes
'''
from flask import Blueprint
from flask_login import login_required

edit = Blueprint('edit', __name__)

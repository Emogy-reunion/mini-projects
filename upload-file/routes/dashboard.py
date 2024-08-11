'''
This module handles rendering user dashboards
dash blueprint is registered
The blueprint is used to create routes
'''
from flask import Blueprint, render_template
from flask_login import login_required

dash = Blueprint('dash', __name__)

@dash.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

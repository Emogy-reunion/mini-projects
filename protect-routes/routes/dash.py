'''
This module contains dashboard the user sees after logging in
'''

from flask import Blueprint, render_template
from flask_login import login_required

dash = Blueprint('dash', __name__)

@dash.route('/dashboard')
@login_required
def dashboard():
    '''
    renders the logged in user dashboard
    '''
    return render_template('dashboard.html')

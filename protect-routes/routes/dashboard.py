from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user


dash = Blueprint('dash', __name__)

@dash.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    renders the logged in users dashboard
    """
    if current_user.role == 'admin':
        return redirect(url_for('dash.admin_dashboard'))
    return render_template('dashboard.html')

from flask import render_template, Blueprint
from flask_login import login_required

dash = Blueprint('dash', __name__)

@dash.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

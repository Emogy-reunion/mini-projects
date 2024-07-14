from flask import Flask, url_for, redirect, flash, render_template
from config import Config
from flask_login import LoginManager
from model import db, User, bcrypt
from form import RegistrationForm, LoginForm
from  routes.auth import auth

#initialize the flask app
app = Flask(__name__)

#configure flask app with settings defined in the configuration file
app.config.from_object(Config)

#initialize the db instance with the app instance
db.init_app(app)
bcrypt.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


app.register_blueprint(auth)

@login_manager.user_loader
def load_user(user_id):
    """loads user with this user_id from the database to the session"""
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)

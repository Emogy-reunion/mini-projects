from flask import Flask, url_for
from config import Config
from model import db, bcrypt, User, Posts, Images
from routes.authentication import auth
from routes.dashboard import dash
from routes.upload import post
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)

loginmanager = LoginManager(app)
loginmanager.login_view = 'login'

app.register_blueprint(auth)
app.register_blueprint(dash)
app.register_blueprint(post)

def create_model():
    with app.app_context():
        db.create_all()

create_model()

@loginmanager.user_loader
def load_user(user_id):
    '''
    loads the user into the session
    '''
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)

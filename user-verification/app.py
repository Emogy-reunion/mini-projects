from create_app import create_app
from model import db, bcrypt, User
from routes.authentication import mail, auth
from routes.dashboard import dash
from flask_login import LoginManager


app = create_app()

loginmanager = LoginManager(app)
loginmanager.login_view = 'login'
db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(dash)

with app.app_context():
    db.create_all()

@loginmanager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

if __name__ == '__main__':
    app.run(debug=True)

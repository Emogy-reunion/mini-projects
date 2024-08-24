from flask import Flask
from model import db, bcrypt, User
from routes.authentication import mail, auth
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)

app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

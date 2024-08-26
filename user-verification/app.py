from create_app import create_app
from model import db, bcrypt, User
from routes.authentication import mail, auth
from routes.dashboard import dash


app = create_app()


db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(dash)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

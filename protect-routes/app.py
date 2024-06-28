from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired

#initialize the flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mark:7hhYhn>4@localhost/flaskpractice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MY-SECRET-KEY'

db = SQLAlchemy(app)

class User(db.Model):
    """
    representation of the user table
    the table has the following column: id, firstname, lastname, email, passwordhash
    """
    __tablename__ = 'user1'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    passwordhash = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()




if __name__ == '__main__':
    app.run(debug=True)

"""
This module contains implementation of password hashing using Bcrypt
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#initialize the application instance
app = Flask(__name__)

app.config['SECRET_KEY'] = 'MY-SECRET-KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mark:7hhYhn>4@localhost/flaskpractice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Users(db.Model):
    """
    A representation of the users table
    Each table has columns: id, firstname, lastname, email, passwordhash
    """
    __tablename__ = 'users2'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    passwordhash = db.Column(db.String(150), nullable=False)

if __name__ == '__main__':
    app.run(debug=True)

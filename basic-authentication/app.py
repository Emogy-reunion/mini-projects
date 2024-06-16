"""
Flask application for user management

This module creates a Flask application with SQLAlchemy integration to manage users in a mysql database
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#initialize the flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mark:7hhYhn>4@localhost/flaskpractice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    """
    Represents a user in the application
    This class defines the structure of the 'user' table in the database
    Each user has an id, fullname, email, username and password
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

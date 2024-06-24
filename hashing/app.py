"""
This module contains implementation of password hashing using Bcrypt
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#initialize the application instance
app = Flask(__name__)

app.config['SECRET_KEY'] = 'MY-SECRET-KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:mark:7hhYhn>4@localhost/flaskpractice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True)

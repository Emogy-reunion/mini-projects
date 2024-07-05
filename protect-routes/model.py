from flask_sqlalchemy import SQLAlchemy
from app import bcrypt

db = SQLAlchemy()

class User(db.Model):
    """
    Representation of the user table.
    The table has the following columns: id, firstname, lastname, email, username, passwordhash.
    """
    __tablename__ = 'user1'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passwordhash = db.Column(db.String(50), nullable=False)


    def __init__(self, firstname, middlename, lastname, email, username, password):
        """
        initializes the user data
        """
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        """
        Hashes the password and initializes it
        """
        self.passwordhash = bcrypt.generate_password_hash(password)

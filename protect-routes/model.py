from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    """
    Representation of the user table.
    The table has the following columns: id, firstname, lastname, email, username, passwordhash.
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passwordhash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(32), nullable=False, default='user')


    def __init__(self, firstname, middlename, lastname, email, username, password, role=role):
        """
        initializes the user data
        """
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email
        self.username = username
        self.role = role
        self.set_password(password)

    def set_password(self, password):
        """
        Hashes the password and initializes it
        """
        self.passwordhash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        compares the user password and the stored hash
        returns True if the passwords match and False if otherwise
        """
        return bcrypt.check_password_hash(self.passwordhash, password)

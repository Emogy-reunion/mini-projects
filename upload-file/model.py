from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    """
    A representation of the user table
    This table will store a user's personal information
    One user can have multiple posts
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Posts', backref='user', lazy=True)

    def __init__(self, firstname, lastname, email, password, gender):
        '''
        initializes the user data
        '''
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.gender = gender
        self.set_password(password)

    def set_password(self, password):
        '''
        generates password hash and saves it to the database
        '''
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')


    def check_password(self, password):
        """
        compares the entered password and stored hash to see if they match
        """
        return bcrypt.check_password_hash(self.password_hash, password)

class Posts(db.Model):
    """
    A representation of the posts table
    This table will store information about the post
    One post can have multiple images
    """

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.relationship('Images', backref='post', lazy=True)

    def __init__(self, title, post_id):
        self.title = title
        self.user_id = user_id

class Images(db.Model):
    """
    A representation of the images table
    This table stores image filenames
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    filename = db.Column(db.String(150), nullable=False)

    def __init__(self, filename, post_id):
        self.filename = filename
        self.post_id = post_id

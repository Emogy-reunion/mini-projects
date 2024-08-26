from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from create_app import create_app
from flask_login import UserMixin

app = create_app()
db = SQLAlchemy()
bcrypt = Bcrypt()

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

class User(UserMixin, db.Model):
    '''
    A model that represents the user table
    It's attributes represents the columns of the table
    It is used to create user instances that translate to users in the table
    '''

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        return serializer.dumps({'user_id': self.id})

    @staticmethod
    def verify_token(token):
        try:
            data = serializer.loads(token, max_age=3600)
            return User.query.get(data['user_id'])
        except Exception as e:
            return None

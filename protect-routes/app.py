from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Regexp, Optional, Length, EqualTo

#initialize the flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mark:7hhYhn>4@localhost/flaskpractice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MY-SECRET-KEY'

db = SQLAlchemy(app)

class User(db.Model):
    """
    representation of the user table
    the table has the following column: id, firstname, lastname, email, username, passwordhash
    """
    __tablename__ = 'user1'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passwordhash = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

class RegistrationForm(FlaskForm):
    """
    represents the registration form fields
    the form has the following fields: firstname, middlename, lastname, email, username,
        password, confirmpassword, submit
    """

    firstname = StringField("First Name", validators=[DataRequired()])
    middlename = StringField("Middle Name", validators=[Optional()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Regexp(r'^\w+$', message="Username must contain only letters, numbers, or underscore.")])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8, message="Password must be at least 8 characters long."),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character.")
        ])
    confirmpassword = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Sign Up')




if __name__ == '__main__':
    app.run(debug=True)

"""
Flask application for user management

This module creates a Flask application with SQLAlchemy integration to manage users in a mysql database
"""
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, InputRequired
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

#initialize the flask app
app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mark:7hhYhn>4@localhost/flaskpractice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
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

class CreateAccount(FlaskForm):
    """
    This class defines the structure of the registration form
    FlaskForm: base class for creating forms
    The form has fields Full Name, Email, Username, Password, Confirm Password
    """

    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    """
    This class defines the structure of the login form
    FlaskForm: base class for creating forms
    The form has fields  Email, Password, Remember me
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

@login_manager.user_loader
def load_user(user_id):
    """loads the user from the session"""
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def register():
    """
    This method does two things:
        - if the request is a GET request it renders the registration page
        - if the request is a POST request it handles creation of the user
            - handles form validation
            - extracts data and saves it to the database
    """

    form = CreateAccount()
    if request.method == 'GET':
        """if it's a GET request render the register.html template"""
        return render_template('register.html', form=form)

    if form.validate_on_submit():
        """
        checks if data is valid - according to validators
        if it is not error messages will be displayed
        if it is valid data is extracted and saved to the database
        """

        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data.lower()
        password = form.password.data
        confirm_password = form.confirm_password.data

        #check if user exists
        user = User.query.filter_by(email=email).first()

        if user:
            # if user exists display message
            flash("An account exists for this email. Log In.", "danger")
        else:
            try:
                new_user = User(fullname=name, email=email, username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash("Account Created successfully", "success")
                return redirect(url_for('login'))
            except exception as e:
                db.session.rollback()
                flash("An error occurred during account creation", "danger")
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Authenticates the user
    logs them in by saving their id to the session,
    then redirects them to a dashboard
    """


    form =  LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data.lower()
            password = form.password.data
            remember = form.remember.data

            user = User.query.filter_by(email=email).first()

            if user:
                if user.password == password:
                    '''login the user if the passwords match'''
                    login_user(user, remember=remember)
                    flash("Successfully logged in", "succcess")
                    return redirect(url_for('dashboard'))
                else:
                    flash("Incorrect Password!", "danger")
            else:
                flash("Invalid  Email or Account  Doesn't  Exist!", "danger")
    return render_template('login.html', form=form)



    

if __name__ == "__main__":
    app.run(debug=True)

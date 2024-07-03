"""
This module contains implementation of password hashing using Bcrypt
"""
from flask import Flask, flash, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

#initialize the application instance
app = Flask(__name__)

app.config['SECRET_KEY'] = 'MY-SECRET-KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mark:7hhYhn>4@localhost/flaskpractice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class Users(UserMixin, db.Model):
    """
    A representation of the users table
    Each table has columns: id, firstname, lastname, email, passwordhash
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    passwordhash = db.Column(db.String(150), nullable=False)

    def __init__(self, firstname, lastname, email, password):
        """initializes the user table attributes"""
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password) # calls set_password method to save password

    def set_password(self, password):
        #generates the password hash and saves it in the database
        self.passwordhash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        compares the password with the set password
        it return True if passwords match and false if otherwise"""
        return bcrypt.check_password_hash(user.passwordhash, password)


with app.app_context():
    db.create_all()

class RegistrationForm(FlaskForm):
    """
    represents the fields of the registration form
    it has the following fields: firstname, lastname, email, password, confirm_password

    """
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirmpassword = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """
    a representation of the login form
    it has the following fields: email, password, remember me
    """
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def register():
    """
    this method does two things:
    1. handles user account creation - If the request method is POST
        saves user data to the database
    2. renders the register.html page - if the request method is GET
    """
    form = RegistrationForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            """
            checks if form has valid input
            if it has required input data is extracted and saved to the database
            """
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data.lower()
            password = form.password.data
            
            # queries the database to check if the user exists
            user = Users.query.filter_by(email=email).first()
            if user:
                #if the user exists display message
                flash("An account with this email exists! Log In", "danger")
                return redirect(url_for('register'))
            else:
                #if user doesn't exist create account
                try:
                    new_user = Users(firstname=firstname, lastname=lastname, email=email, password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    flash("Account created successfully!", "success")
                    return redirect(url_for('login'))
                except Exception as e:
                    db.session.rollback()
                    flash("An error occurred while creating your account. Please try again.", "danger")
                    return redirect(url_for('register'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This method handles user authentication and logs them in
    if the request method is GET it renders the login.html page
    if the method is POST  it verifies if the user is authenticated and logs them in the session
    """

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            """
            checks if data is valid, if it is valid it extracts the data
            the user is queried from the database and passwords compared
            """

            email = form.email.data.lower()
            password = form.password.data
            remember = form.remember.data

            user = Users.query.filter_by(email=email).first()

            if user:
                #checks if the user exists
                if password == user.check_password(password):
                    """
                    checks if passwords match
                    if true it logs the user in
                    """
                    login_user(user, remember=remember)
                    flash("Successfully logged in!", "success")
                    return redirect(url_for('dashboard'))
                else:
                    #if passwords don't match
                    flash("Incorrect password!", "danger")
            else:
                #if user doesn't exist
                flash("Incorrect Email or Account doesn't exist", "danger")

    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

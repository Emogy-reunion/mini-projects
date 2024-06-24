"""
This module contains implementation of password hashing using Bcrypt
"""
from flask import Flask, flash, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

#initialize the application instance
app = Flask(__name__)

app.config['SECRET_KEY'] = 'MY-SECRET-KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mark:7hhYhn>4@localhost/flaskpractice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


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

    def __init__(self, firstname, lastname, email, password):
        """initializes the user table attributes"""
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password) # calls set_password method to save password

    def set_password(self, password):
        """
        generates the password hash and saves it in the database
        """
        self.passwordhash = bcrypt.generate_password_hash(password)


with app.app_context():
    db.create_all()

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
            checks if form has required input
            if it has required input data is extracted and saved to the database
            """
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user:
                flash("An account with this email exists! Log In", "danger")
            else:
                user = User(firstname=firstname, lastname=lastname, email=email, password=password)
                flash("Account created successfully!", "success")
                return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

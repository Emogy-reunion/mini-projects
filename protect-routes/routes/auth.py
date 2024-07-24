from flask import url_for, Blueprint, redirect, request, render_template, flash
from form import RegistrationForm, LoginForm
from model import User, db
from  flask_login import login_user, login_required


auth = Blueprint('auth', __name__)

@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Authenticates the user and logs them into the session.
    """
    form = LoginForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            """
            Check if form contains valid data and extract the data.
            """
            email = form.email.data.lower()
            password = form.password.data
            remember = form.remember.data

        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if user:
            """Check if the user exists."""
            if user.check_password(password):
                """Compare the password to see if they match."""
                try:
                    login_user(user, remember=remember)
                    flash("Logged in successfully!", "success")
                    return redirect(url_for('dash.dashboard'))
                except Exception as e:
                    print(e)
                    flash("An error occurred during logging in. Try again", "danger")
                    return redirect(url_for('auth.login'))
            else:
                flash("Incorrect password!", "danger")
                return redirect(url_for('auth.login'))
        else:
            flash("Incorrect email or account doesn't exist", "danger")
            return redirect(url_for('auth.login'))

    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    adds users to the database
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        """
        checks if the form contains valid data
        if the data is valid it is extracted
        the data is then added to the database
        """
        firstname = form.firstname.data
        middlename = form.middlename.data
        lastname = form.lastname.data
        email = form.email.data.lower()
        username = form.username.data.lower()
        password = form.password.data

        #check if the username is used
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username is already taken. Please choose a different one.", "danger")
            return redirect(url_for('auth.register'))

        #check if email is used
        user1 = User.query.filter_by(email=email).first()
        if user1:
            flash("Email is already in use. Please use a different one.", "danger")
            return redirect(url_for('auth.register'))

        #if email and username aren't taken create the account
        try:
            new_user = User(firstname=firstname, middlename=middlename, lastname=lastname,
                            email=email, username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful!", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(e)
            db.session.rollback()
            flash("An error occurred during account creation. Please try again.", "danger")
            return redirect(url_for('auth.register'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('auth.login'))

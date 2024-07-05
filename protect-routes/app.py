from flask import Flask, url_for, redirect, flash, render_template
from config import Config
from flask_login import LoginManager
from model import db, User
from form import RegistrationForm
from flask_bcrypt import Bcrypt

#initialize the flask app
app = Flask(__name__)

#configure flask app with settings defined in the configuration file
app.config.from_object(Config)

#initialize the db instance with the app instance
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """loads user with this user_id from the database to the session"""
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('register'))

        #check if email is used
        user1 = User.query.filter_by(email=email).first()
        if user1:
            flash("Email is already in use. Please use a different one.", "danger")
            return redirect(url_for('register'))

       #if email and username aren't taken create the account
       try:
            new_user = User(firstname=firstname, middlename=middlename, lastname=lastname,
                            email=email, username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful!", "success")
            retun redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred during account creation. Please try again.", "danger")
            return redirect(url_for('register'))
    return render_template('register.html', form=form)



        


if __name__ == '__main__':
    app.run(debug=True)

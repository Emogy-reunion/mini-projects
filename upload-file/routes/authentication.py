from flask import Blueprint, render_template, redirect, request, url_for, flash
from form import RegistrationForm, LoginForm
from flask_login import login_user
from model import User

auth = Blueprint('auth', __name__)

@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Perfoms two tasks:
        if it is a GET request it renders the register.html template
        if it is a POST Method the user is registered to the database
    '''

    if request.method == 'GET':
        form = LoginForm()
        return render_template("login.html", form=form)

    form = LoginForm(request.form) #instantiate form fields with the data
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()
        
        if user:
            if user.check_password(password):
                try:
                    login_user(user, remember=remember)
                    return redirect(url_for('dash.dashboard'))
                except Exception as e:
                    flash('An error occured. Try Again!', 'danger')
                    return redirect(request.url)
            else:
                flash('Incorrect password. Try Again!', 'danger')
                return redirect(request.url)
        else:
            flash('Incorrect email. Try Again!', 'danger')
            return redirect(request.url)
    else:
        return jsonify({'errors': form.errors}), 400




@auth.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Performs two tasks:
        if it is a GET request it renders the register.html template
        if it is a POST Method the user is registered to the database
    '''

    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('login.html', form=form)

    form = RegistrationForm(request.form)

    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data
        gender = form.gender.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email is already used. Please login or choose a different one.", "danger")
            return redirect(request.url)
        else:
            try:
                new_user = User(firstname=firstname, lastname=lastname,
                                email=email, password=password, gender=gender)
                db.session.add(new_user)
                db.session.commit()
                flash("Account created successfully!", "success")
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Try Again!', 'danger')
                return redirect(request.url)
    else:
        return jsonify({'errors': form.errors}), 400

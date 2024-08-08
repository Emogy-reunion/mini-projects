from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from form import RegistrationForm, LoginForm
from flask_login import login_user
from model import User, db

auth = Blueprint('auth', __name__)

@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Perfoms two tasks:
        if it is a GET request it renders the register.html template
        if it is a POST Method the user is registered to the database
    '''

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.form)
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
                        return jsonify({'error': 'An error occurred. Try Again!'})
                else:
                    return jsonify({'error': 'Incorrect password. Try Again!'})
                    
            else:
                return jsonify({'error': "Account doesn't exist!"})

        else:
            return jsonify({'errors': form.errors})
    else:
        return render_template('login.html', form=form)




@auth.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Performs two tasks:
        if it is a GET request it renders the register.html template
        if it is a POST Method the user is registered to the database
    '''

    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.form)

        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            password = form.password.data
            gender = form.gender.data

            user = User.query.filter_by(email=email).first()
            if user:
                return jsonify({"error": 'Email is already in use!'})
            else:
                try:
                    new_user = User(firstname=firstname, lastname=lastname,
                                    email=email, password=password, gender=gender)
                    db.session.add(new_user)
                    db.session.commit()
                    return jsonify({'success': 'Account created successfully!'})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'error': 'An unexpected error occured. Try Again!'})
        else:
            print(form.errors)
            return jsonify({'errors': form.errors})
    else:
        return render_template('register.html', form=form)

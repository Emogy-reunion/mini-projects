from flask import Flask, Blueprint, render_template, request
from form import RegistrationForm, LoginForm
from model import db, User
from flask_mail import Mail, Message

auth = Blueprint('auth', __name__)

mail = Mail()

@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        form = LoginForm(request.form)

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password):
                    if user.verified:
                        try:
                            login_user(user, remember=remember)
                            return jsonify({'success': 'User logged in successfully'})
                        except Exception as e:
                            return jsonify({'error': 'An unexpected error occured. Please Try Again!'})
                    else:
                        return jsonify({'unverified': 'Verify your email before proceeding!'})
                else:
                    return jsonify({'error': 'Incorrect password. Please try again!'})
            else:
                return jsonify({'error': 'Incorrect email. Please try again!'})
        else:
            return jsonify({'errors': form.errors})



@auth.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        form = RegistrationForm(request.form)

        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data.lower()
            password = form.password.data
            
            user = User.query.filter_by(email=email).first()

            if user:
                return jsonify({'error': 'An account with this email already exists. Please use a different email.'})
            else:
                try:
                    new_user = User(firstname=firstname, lastname=lastname, email=email, password=password)
                    db.session.add(new_user)
                    db.session.commit()

                    send_verification_email(new_user)
                    return jsonify({'success': 'Account created succesfully!. Verify your Email!'})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'error': 'An unexpected error occurs!'})
        else:
            return jsonify({'errors': form.errors})

def send_verification_email(user):
    token = user.generate_token()

    verification_url = url_for('auth.verify_email', token, _external=True)
    msg = Message(
            subject='Verify your email',
            sender='info.markrealestateapp734@gmail.com',
            recipients=[user.email]
            )
    msg.body(f'Click the following link to verify your email address:{verification_url}')
    mail.send(msg)

@auth.route('/verify_email/<token>')
def verify_email(token):
    user = User.verify_token(token)

    if user:
        user.verified = True
        db.session.commit()

        flash('Email verified successfully. You can now login', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('The verification link has expired or is invalid. Try again', 'error')
        return redirect(url_for('auth.resend_verification'))



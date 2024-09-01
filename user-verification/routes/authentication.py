from flask import Flask, Blueprint, render_template, request, url_for, redirect, flash, jsonify
from form import RegistrationForm, LoginForm, ReverificationForm, ResetForm, ForgotPassword
from model import db, User
from flask_mail import Mail, Message
from flask_login import login_user

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
        return render_template('register.html', form=form)
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
                    return jsonify({'success': 'Account created succesfully!. A verification email has been sent!'})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'error': 'An unexpected error occured!'})
        else:
            return jsonify({'errors': form.errors})

def send_verification_email(user):
    token = user.generate_token()

    verification_url = url_for('auth.verify_email', token=token, _external=True)
    msg = Message(
            subject='Verify your email',
            sender='info.markrealestateapp734@gmail.com',
            recipients=[user.email]
            )
    msg.body = f'Click the following link to verify your email address: {verification_url}'
    mail.send(msg)

@auth.route('/verify_email/<token>')
def verify_email(token):
    user = User.verify_token(token)

    if user:
        user.verified = True
        db.session.commit()

        return render_template('success.html')
    else:
        flash('The verification link has expired or is invalid. Try again', 'error')
        return redirect(url_for('auth.resend_verification'))


@auth.route('/resend_verification', methods=['GET', 'POST'])
def resend_verification():
    '''
    Allows users to request a reverification email and
        updates the users to verified upon verification
    '''
    form = ReverificationForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            email = form.email.data

            user = User.query.filter_by(email=email).first()

            if user:
                if user.verified:
                    flash('User already verified. Login!', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    send_verification_email(user)
                    flash('A new verification email has been sent', 'success')
                    return redirect(request.url)
            else:
                flash('Incorrect email. Try again!')
                return redirect(request.url)
    return render_template('reverification.html', form=form)


@auth.route('forgot_password', methods=['GET', 'POST'])
def forgot_password():

    form = ForgotPassword()

    if request.method == 'GET':
        return render_template('forgot_password.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data

        user = User.query.filter_by(email=email).first()

        if user:
            reset_email(user)
            flash('A password reset link has been sent. Check your email!', 'success')
            return redirect(request.url)
        else:
            flash('Account not found! Please try again!', 'error')
            return redirect(request.url)

def reset_email(user):
    token = user.generate_token()

    verification_url = url_for('auth.reset_email', token=token, _external=True)
    msg = Message(
            Subject='Password reset',
            sender='info.markrealestateapp734@gmail.com',
            recipients=[user.email])
    msg.body = f'A password reset request has been made for your account, if you made the request click the following link to reset password {verification_url}. If you did not make the request ignore this email'
    mail.send(msg)

@auth.route('/reset_email/<token>')
def reset_email(token):
    user = User.verify_token(token)

    if user:
        return redirect(url_for('auth.reset_password', user=user))
    else:
        flash('The verification link has expired or is invalid. Try again!', 'error')
        return redirect(url_for('auth.forgot_password'))

@auth.route('/reset_password/<user>', methods=['GET', 'POST'])
def reset_password():

    form = ResetForm()

    if request.method == 'GET':
        return render_template('reset.html', form=form)
    else:
        form = ResetForm(request.form)
        if form.validate_on_submit():
            password = form.password.data

            try:
                user.generate_password_hash(password)
                db.session.commit()
                return jsonify({'success': 'Password successfully changed'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'An error occurred. Try again!'})
        else:
            return jsonify({"errors": "form.errors"})
            

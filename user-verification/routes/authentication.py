from flask import Flask, Blueprint, render_template, request
from form import RegistrationForm
from model import db, User
from flask_mail import Mail, Message

auth = Blueprint('auth', __name__)

mail = Mail()

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



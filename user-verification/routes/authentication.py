from flask import Flask, Blueprint, render_template, request
from form import RegistrationForm
from model import db, User

auth = Blueprint('auth', __name__)

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
                    return jsonify({'success': 'Account created succesfully. Login!'})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'error': 'An unexpected error occurs!'})
        else:
            return jsonify({'errors': form.errors})



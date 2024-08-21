from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputField

class LoginForm(FlaskForm):
    '''
    represents the login form fields
    '''

    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('SIGN IN')

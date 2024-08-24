from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Length, Regexp, EqualTo

class RegistrationForm(FlaskForm):
    '''
    Represents the fields of a registration form
    '''
    firstname = StringField('First name', validators=[DataRequired(), Length(min=2, max=30)])
    lastname = StringField('Last name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[Email(), InputRequired(), Length(max=30)])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8, message="Password must be at least 8 characters long."),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character.")
        ])
    confirmpassword = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Sign Up')

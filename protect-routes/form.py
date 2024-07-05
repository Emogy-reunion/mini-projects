from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Email, Regexp, Optional, Length, EqualTo

class RegistrationForm(FlaskForm):
    """
    Represents the registration form fields.
    The form has the following fields: firstname, middlename, lastname, email, username,
    password, confirmpassword, submit.
    """
    firstname = StringField("First Name", validators=[DataRequired()])
    middlename = StringField("Middle Name", validators=[Optional()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Regexp(r'^\w+$', message="Username must contain only letters, numbers, or underscore.")])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8, message="Password must be at least 8 characters long."),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character.")
        ])
    confirmpassword = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    """
    Represents the login form fields"
    The form has the following fields: Email, password, remember me
    """
    email = StringField("Email", validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')

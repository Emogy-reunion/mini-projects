from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
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
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase

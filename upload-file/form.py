from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, Regexp, InputRequired, EqualTo, Email


class RegistrationForm(FlaskForm):
    '''
    A representation of the registration form fields
    '''
    firstname = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    lastname = StringField('Last name', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character.")
        ])
    confirmpassword = PasswordField('Confirm Password', validators=[
        InputRequired(),
        EqualTo('password', message='Passwords must match')
        ])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')],
                         validators=[InputRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    '''
    A representation of the login form fields
    '''

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class UploadForm(FlaskForm):
    '''
    A representation of the upload form fields
    '''

    title = StringField('Title', validators=[DataRequired()])
    files = MultipleFileField('Choose images', validators=[InputRequired()])
    submit = SubmitField('Upload')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
	"""
	Web form class for login form built off a FlaskForm

	Form Fields
	----------
	username : StringField
		user enters username to sign in
	password : PasswordField
		user enters password to sign in
	remember_me : BooleanField
		box where user checks if they want 
	submit : Submit Field
		button user uses to attempt to sign in
	"""

	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """
    Web form class for registration form built off a FlaskForm

	Form Fields
	----------
	username : StringField
		user fills out desired username
	email : StringField
		user fills out desired email
	password : PasswordField
		user enters desired password 
	password2 : PasswordField
		user confirms password to ensure no typos have been made
	
	Methods
	-------
	validate_username(self, username)
		checks if user's desired username is already registered
	
	validate_email(self, email)
		checks if user's desired email is already registered
    """

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('PLease use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

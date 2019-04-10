from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms import IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from project.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20) ])
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20) ])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20) ])
    sex = RadioField('Sex', choices = [('M','Male'),('F','Female')], validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
    phone = IntegerField('Phone #1', validators = [DataRequired(), ])
    phone2 = IntegerField('Phone #2')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
     validators=[DataRequired(), EqualTo('password')])
    role = StringField('Role')
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exist. Please choose a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exist. Please choose a different Email.')

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('Phone No. already exist. Please choose a different Phone No.', 'error')
    
    
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EmailForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user is None:
                raise ValidationError('There is no account with that email, You must register first')

class PasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
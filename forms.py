from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
#import models

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField("Post Comment")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete Comment")

class SearchForm(FlaskForm):
    query = StringField('query', validators=[DataRequired()])
    submit = SubmitField('🔍')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = models.User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PasswordUpdate(FlaskForm):
    currentpassword = PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update Password')

class EmailUpdate(FlaskForm):
    currentemail = StringField('Current Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('New Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Email')

    def validate_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Someone already has an account with this email, please use an alternative email address.')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

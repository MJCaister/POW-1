from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from models import User


# Comment Form on prisoner.html
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(max=500, message='Comment exceeds 500 characters')])
    submit = SubmitField("Post Comment")


# Search form on browse.html
class SearchForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])
    options = SelectField('Refine Search', choices=[('All', 'All'), ('Prisoner', 'Prisoner'),
                                                    ('Unit', 'Unit'), ('Rank', 'Rank'),
                                                    ('Capture', 'Capture')])
    submit = SubmitField('🔍')


# Login form on login.html
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Register account form on register.html
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=32, message="Username cannot exceed 32 characters")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Password must be longer than 8 characters")])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # this checks the username is not within the db
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # checks the email is not already within the database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


# Update Password form for updatepass.html
class PasswordUpdate(FlaskForm):
    currentpassword = PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update Password')


# Update email form for updateemail.html
class EmailUpdate(FlaskForm):
    currentemail = StringField('Current Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('New Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Email')


# Delete account form on deleteaccount.html
class DelAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Delete Account')


# Reset Password Request for requestreset.html
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


# Reset Password form for resetpassword.html
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


# Contact form in footer.html displaying on all pages.
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

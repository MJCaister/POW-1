from flask_mail import Message
from flask import render_template
from threading import Thread
import routes


#Sends the email async
def send_async_email(app, msg):
    with app.app_context():
        routes.mail.send(msg)


# Function that sends the email
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(routes.app, msg)).start()
    #routes.mail.send(msg)


# This is the Password Reset email that is sent
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('New Zealand P.O.W.s - Reset Your Password',
               sender=routes.app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


# This is the update email sent to users when tracked POW is updated
def send_update_email(tuser):
    send_email('New Zealand P.O.W.s - Comment On Tracked Prisoner',
               sender=routes.app.config['ADMINS'][0],
               recipients=[tuser.User.email],
               text_body=render_template('email/POW_Update.txt',
                                         user=tuser, POW=tuser.Prisoner),
               html_body=render_template('email/POW_Update.html',
                                         user=tuser, POW=tuser.Prisoner))


# This is the email that's sent to the admin email when the contact form is used.
def send_admin_contact(name, email, message):
    send_email('New Zealand P.O.W.s - Contact Form',
               sender=routes.app.config['ADMINS'][0],
               recipients=[routes.app.config['ADMINS'][0]],
               text_body=render_template('email/contactform.txt',
                                         name=name, email=email, message=message),
               html_body=render_template('email/contactform.html',
                                         name=name, email=email, message=message))

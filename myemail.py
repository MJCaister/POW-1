from flask_mail import Message
from flask import render_template
from threading import Thread
import routes



def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    routes.mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('New Zealand P.O.W.s - Reset Your Password',
               sender=routes.app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_update_email(tuser):
    send_email('New Zealand P.O.W.s - Comment On Tracked Prisoner',
                sender=routes.app.config['ADMINS'][0],
                recipients=[tuser.User.email],
                text_body=render_template('email/POW_Update.txt',
                                        user=tuser, POW=tuser.Prisoner),
                html_body=render_template('email/POW_Update.html',
                                        user=tuser, POW=tuser.Prisoner))

from os import sync
from config import EmailConfig
from datetime import datetime
from flask_mail import Message
from flask import render_template, current_app
from srcode import mail, app
from threading import Thread
from twilio.rest import Client




def send_async_post_notification_email(app, msg):
     with app.app_context():
          mail.send(msg)

def send_post_notification(subject, sender, recipients, html_body):
     msg = Message(subject, sender=sender, recipients=recipients)
     msg.html = html_body
     '''Pass the _get_current_object() to access the application's instance'''
     Thread(target=send_async_post_notification_email, args=(current_app._get_current_object(), msg)).start()

def send_post_notification_email(followers, user, post, date_posted= datetime.now()):
     send_post_notification('[Flaskgram] Post Notification', sender = EmailConfig.DEFAULT_MAIL_SENDER,
     recipients = [follower_email.email for follower_email in followers],
     html_body= render_template('user/post_notifications.html', post=post, user=user, date_posted=date_posted))

def send_posts(subject, sender, recipients, html_body, body_html, attachments = None, sync =False):
     msg = Message(subject, sender=sender, recipients=recipients, html=html_body, body=body_html)
     '''Pass the _get_current_object() to access the application's instance'''
     if attachments:
          for attachment in attachments:
               msg.attach(*attachment)
     if sync:
          mail.send(msg)
     Thread(target=send_async_post_notification_email, args=(current_app._get_current_object(), msg)).start()


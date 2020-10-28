
from blinker import Namespace
from flask import flash
from .user.email import send_post_notification_email


#Configure the PUB/SUB signal for following/followed user --> send email.
followed_user_signal = Namespace()
user_followed_signal = followed_user_signal.signal('user_followed_signal')

def connect_pub_handlers():
     user_followed_signal.connect(flash('Notification sent!', 'success'))
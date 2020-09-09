from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask import request
from srcode.models import User
from flask_babel import lazy_gettext as _i  #Translating function for i8n and l6n support
#from wtforms.fields.html5 import DateField. Used for dates uses a yy-mm-dd forms


class UpdateAdminAccountForm(FlaskForm):
    email = StringField(_i('Email'), validators=[DataRequired(), Email()])
    username = StringField('Username', validators = [DataRequired(), Length(min=1, max=20, message = 'Username must be between 2 and 20 characters')])
    confirmed = BooleanField('Confirmed')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg','png'])])
    role = SelectField('Role', coerce=int, choices = [(1, 'admin'), (0,'user')])
    bio = StringField('About me', validators = [DataRequired(), Length(min=1, max=100, message ='Must be below 100 characters')])
    submit = SubmitField('Submit')


class UpdateAccountForm(FlaskForm):
     username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
     email = StringField('Email',
                        validators=[DataRequired(), Email()])
     bio = StringField('About me',
                           validators=[DataRequired(), Length(min=1, max=120)])
     picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg','png'])])
     submit = SubmitField('Update')

     def validate_username(self, username):
          if username.data != current_user.username:
               user = User.query.filter_by(username=username.data).first()
               if user:
                    raise ValidationError('That username is taken. Please choose a different one.')

     def validate_email(self, email):
          if email.data != current_user.email:
               user = User.query.filter_by(email=email.data).first()
               if user:
                    raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    tag = StringField('Any Post Tags?')
    content = TextAreaField('Content', validators=[DataRequired()])
    post_image = FileField('Update Post Picture?', validators=[FileAllowed(['jpg','gif','jpeg','png'])])
    submit = SubmitField('Post')
class CommentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Your comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class SearchForm(FlaskForm):
    '''Query is a prefix for standard search engines'''
    q = StringField(_i('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

class follow_unfollowForm(FlaskForm):
    '''Implemented as a form to protect against CSRF attacks'''
    submit = SubmitField('Submit')
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from srcode.models import User, Role
from flask_babel import lazy_gettext as _i  #Translating function for i8n and l6n support
#from wtforms.fields.html5 import DateField. Used for dates uses a yy-mm-dd forms

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    # recaptcha = RecaptchaField()                               
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField(_i('Email'),
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


    # def __init__(self, user, *args, **kwargs):
    #     super(UpdateAdminAccountForm, self).__init__(*args, **kwargs)
    #     self.role.choices = [(role.id, role.name)
    #         for role in Role.query.order_by(Role.name).all()]
    #     self.user = user

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators =[DataRequired(), Email()])
    submit = SubmitField('Submit Request')

class PasswordResetForm(FlaskForm):     
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField(
        'Repeat New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Submit')

#class UnfollowForm(FlaskForm):
#submit = SubmitField('Submit')   

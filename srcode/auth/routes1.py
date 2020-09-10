from flask import render_template, url_for, flash, redirect, request, abort, jsonify, g
from srcode import bcrypt, db
from srcode.auth import bp 
from flask_babel import _
from srcode.auth.forms import RegistrationForm, LoginForm, PasswordResetForm, PasswordResetRequestForm
from srcode.models import User
from srcode.auth.token import confirm_token, generate_confirmation_token
from srcode.auth.email import send_confirmation_email,send_password_reset_email
from flask_login import login_user, current_user, logout_user, login_required
import datetime, time
from flask_dance.contrib.facebook import facebook
from flask_dance.contrib.google import google
from flask_dance.contrib.twitter import twitter
from flask_dance.contrib.github import github



@bp.route('/facebook/login')
def login_facebook():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    response = facebook.get('/me?fields=name,email, id')
    user = User.query.filter_by(email=response.json()['email']).first()
    if not user:
        user = User(email=response.json()['email'], username= response.json()['email'].split('@')[0], social= 'facebook$' + response.json()['id'])
        db.session.add(user)
        db.session.commit()
        redirect(url_for('home'))
        flash(f"AWesome. You have logged in as {response.json()['email'].split('@')[0]}", 'success')
    login_user(user)
    flash(f'Welcome back, {user.username}.')
    return redirect(url_for('home'))
 

@bp.route('/github/login')
def login_github():
    if not github.authorized:
        return redirect(url_for('github.login'))
    response = github.get('/me?fields=name,email, id')
    user = User.query.filter_by(email=response.json()['email']).first()
    if not user:
        user = User(email=response.json()['email'],image_file = response.json()['picture'], username= response.json()['email'].split('@')[0], social= 'github$' + response.json()['id'])
        db.session.add(user)
        db.session.commit()
        redirect(url_for('home'))
        flash(f"AWesome. You have logged in as {response.json()['email'].split('@')[0]}", 'success')
    login_user(user)
    flash(f'Welcome back,{user.username}!')
    return redirect(url_for('home'))   

@bp.route('/google/login')
def login_google():
    if not google.authorized:
             return redirect(url_for('google.login'))
    response = google.get('/oBaseProxy2/v1/userinfo')
    user = User.query.filter_by(email=response.json()['email']).first()
    if not user:
        user = User(email=response.json()['email'], image_file=response.json().get('picture'), username= response.json().get('email').split('@')[0], social= response.json().get('sub'))
        db.session.add(user)
        db.session.commit()
        redirect(url_for('home'))
        flash(f"Awesome. You have logged in as {response.json()['email'].split('@')[0]}", 'success')
    login_user(user)
    flash(f"Welcome back, {response.json()['email'].split('@')[0]}", 'success')
    return redirect(url_for('home'))

@bp.route('/twitter/login')
def login_twitter():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))
    response = twitter.get('account/verify_credentials.json')
    user = User.query.filter_by(username=response.json()['screen_name']).first()
    if not user:
        user = User( username= response.json()['screen_name'], registered_on = datetime.datetime.now(), social= 'twitter$' + response.json()['screen_name'])
        db.session.add(user)
        db.session.commit()
        redirect(url_for('home'))
    login_user(user)
    flash(f"Awesome. You have logged in as {response.json()['screen_name']}", 'success')
    return redirect(url_for('home'))   

@bp.route("/")
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user_email = form.email.data
        user = User(username=form.username.data, email=user_email, confirmed = False, 
        password= hashed_password, registered_on = datetime.datetime.now())
        #user.set_user_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user_email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('auth/activate_email.html', confirm_url=confirm_url)
        send_confirmation_email(user_email, html) 
        flash('Your account has been created and an email verification link has been sent to your email! Please confirm the email to continue', 'success')
        return redirect(url_for('auth.unconfirmed'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email_to_confirm = confirm_token(token)
    except:
        flash('Confirmation link is invalid or has expired', 'danger')
    user = User.query.filter_by(email=email_to_confirm).first_or_404()
    if user.confirmed:
            flash('Awesome, Your account has already been confirmed', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        #add them to the db
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home'))

@bp.route('/resend_confirmation')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/ativate_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_confirmation_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))

@bp.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('home'))
    flash('You are yet to confirm your account. Please do so', 'danger')
    return render_template('auth/unconfirmed.html')

@bp.route('/password_reset', methods=['GET','POST'])   
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password', 'info')
            return redirect(url_for('auth.login'))
    return render_template('auth/password_request_form.html',
                           title='Reset Password', form=form)
    
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Your link is invalid. Redirecting you back home in a few seconds', 'danger')
        time.sleep(3)
        return redirect(url_for('home'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.password = form.new_password.data
        db.session.commit()
        flash('Success, your password has been reset. Login with the new password', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_confirm.html', form=form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Hi, {current_user.username}. Welcome back!", 'success')
            return redirect(next_page) if next_page else redirect(url_for('user.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

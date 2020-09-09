from srcode.essearch import add_to_index
from sqlalchemy import func
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, g, current_app
from srcode import app, db, bcrypt, share
from .models import SavedPosts, User, Post, Permission, Role, PostLike, SavedPosts
from flask_babel import get_locale
from .user import bp
from .user.forms import SearchForm
from flask_login import current_user, login_required
import time, datetime, requests
from config import Config
from guess_language import guess_language
from .uploads3 import save_picture
#from .decorator import check_confirmed, admin_required, permission_required
from flask_dance.contrib.facebook import facebook
from flask_dance.contrib.google import google
from flask_dance.contrib.twitter import twitter
from flask_dance.contrib.github import github



  
# bp.register_blueprint(facebook_blueprint)

# @bp.route('/facebook/login')
# def login_facebook():
#     if not facebook.authorized:
#         return redirect(url_for('facebook.login'))
#     response = facebook.get('/me?fields=name,email, id')
#     user = User.query.filter_by(email=response.json()['email']).first()
#     if not user:
#         user = User(email=response.json()['email'], username= response.json()['email'].split('@')[0], social= 'facebook$' + response.json()['id'])
#         db.session.add(user)
#         db.session.commit()
#         redirect(url_for('home'))
#         flash(f"AWesome. You have logged in as {response.json()['email'].split('@')[0]}", 'success')
#     login_user(user)
#     flash(f'Welcome back, {user.username}.')
#     return redirect(url_for('home'))
 
# bp.register_blueprint(github_blueprint)

# @bp.route('/github/login')
# def login_github():
#     if not github.authorized:
#         return redirect(url_for('github.login'))
#     response = github.get('/me?fields=name,email, id')
#     user = User.query.filter_by(email=response.json()['email']).first()
#     if not user:
#         user = User(email=response.json()['email'],image_file = response.json()['picture'], username= response.json()['email'].split('@')[0], social= 'github$' + response.json()['id'])
#         db.session.add(user)
#         db.session.commit()
#         redirect(url_for('home'))
#         flash(f"AWesome. You have logged in as {response.json()['email'].split('@')[0]}", 'success')
#     login_user(user)
#     flash(f'Welcome back,{user.username}!')
    
#     return redirect(url_for('home'))   

# bp.register_blueprint(google_blueprint)
# @bp.route('/google/login')
# def login_google():
#     if not google.authorized:
#              return redirect(url_for('google.login'))
#     response = google.get('/oauth2/v1/userinfo')
#     user = User.query.filter_by(email=response.json()['email']).first()
#     if not user:
#         user = User(email=response.json()['email'], image_file=response.json().get('picture'), username= response.json().get('email').split('@')[0], social= response.json().get('sub'))
#         db.session.add(user)
#         db.session.commit()
#         redirect(url_for('home'))
#         flash(f"Awesome. You have logged in as {response.json()['email'].split('@')[0]}", 'success')
#     login_user(user)
#     flash(f"Welcome back, {response.json()['email'].split('@')[0]}", 'success')
#     return redirect(url_for('home'))


# bp.register_blueprint(twitter_blueprint)
# @bp.route('/twitter/login')
# def login_twitter():
#     if not twitter.authorized:
#         return redirect(url_for('twitter.login'))
#     response = twitter.get('account/verify_credentials.json')
#     user = User.query.filter_by(username=response.json()['screen_name']).first()
#     if not user:
#         user = User( username= response.json()['screen_name'], registered_on = datetime.datetime.now(), social= 'twitter$' + response.json()['screen_name'])
#         db.session.add(user)
#         db.session.commit()
#         redirect(url_for('home'))
#     login_user(user)
#     flash(f"Awesome. You have logged in as {response.json()['screen_name']}", 'success')
#     return redirect(url_for('home'))   

# @app.route("/home")
# @login_required
# #@check_confirmed
# def home():
#     posts = current_user.followed_posts()
#     return render_template('home.html', title='About', posts=posts)
  

# @app.route("/about")
# #@login_required
# #@check_confirmed
# def about():
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
#     return render_template('about.html',  posts=posts, title='All posts')  
# @app.route('/trending', methods = ['GET', 'POST'])
# def get_trending():
#     posts = db.session.query(Post).outerjoin(PostLike).group_by(Post.id).order_by(func.count().desc()).all() 
#     #posts = Post.query.order_by(Post.likes.desc())
#     return render_template('trending.html', posts = posts)

# @bp.route('/search')
# @login_required
# def search():
#     if not g.search_form.validate():
#         return redirect(url_for('home'))
#     page = request.args.get('page', 1, type=int)
#     posts, total = Post.search(g.search_form.q.data, page,
#                                current_app.config['POSTS_PER_PAGE'])
#     next_url = url_for('search', q=g.search_form.q.data, page=page + 1) \
#         if total > page * current_app.config['POSTS_PER_PAGE'] else None
#     prev_url = url_for('search', q=g.search_form.q.data, page=page - 1) \
#         if page > 1 else None
#     return render_template('search.html', title=_('Search'), posts=posts,
#                            next_url=next_url, prev_url=prev_url)
# @bp.route('/admin')
# @login_required
# @admin_required
# def for_admins_only():
#     return "For administrators!"

# @bp.route('/moderator')
# @login_required
# @permission_required(Permission.MODERATE_COMMENTS)
# def for_moderators_only():
#     return "For comment moderators!"

# @bp.route("/")
# @bp.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data)
#         user_email = form.email.data
#         user = User(username=form.username.data, email=user_email, password=hashed_password, confirmed = False, registered_on = datetime.datetime.now())
#         db.session.add(user)
#         db.session.commit()
#         token = generate_confirmation_token(user_email)
#         confirm_url = url_for('confirm_email', token=token, _external=True)
#         html = render_template('auth/activate_email.html', confirm_url=confirm_url)
#         subject = "Please confirm your email"
#         send_confirmation_email(user_email, subject, html)
        
#         flash('Your account has been created and an email verification link has been sent to your email! Please confirm the email to continue', 'success')
#         return redirect(url_for('auth.unconfirmed'))
#     return render_template('auth/register.html', title='Register', form=form)


# @bp.route('/confirm/<token>')
# def confirm_email(token):
#     try:
#         email_to_confirm = confirm_token(token)
#     except:
#         flash('Confirmation link is invalid or has expired', 'danger')
#     user = User.query.filter_by(email=email_to_confirm).first_or_404()
#     if user.confirmed:
#             flash('Awesome, Your account has already been confirmed', 'success')
#     else:
#         user.confirmed = True
#         user.confirmed_on = datetime.datetime.now()
#         #add them to the db
#         db.session.add(user)
#         db.session.commit()
#         flash('You have confirmed your account. Thanks!', 'success')
#     return redirect(url_for('home'))
# @bp.route('/resend_confirmation')
# @login_required
# def resend_confirmation():
#     token = generate_confirmation_token(current_user.email)
#     confirm_url = url_for('confirm_email', token=token, _external=True)
#     html = render_template('activate_email.html', confirm_url=confirm_url)
#     subject = "Please confirm your email"
#     send_confirmation_email(current_user.email, subject, html)
#     flash('A new confirmation email has been sent.', 'success')
#     return redirect(url_for('auth.unconfirmed'))

# @bp.route('/unconfirmed')
# @login_required
# def unconfirmed():
#     if current_user.confirmed:
#         return redirect(url_for('home'))
#     flash('You are yet to confirm your account. Please do so', 'danger')
#     return render_template('auth/unconfirmed.html')

# @bp.route('/password_reset', methods=['GET','POST'])   
# def password_reset_request():
#     form = PasswordResetRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first_or_404()
#         if user:
#             send_password_reset_email(user)
#             flash('Check your email for the instructions to reset your password', 'info')
#             return redirect(url_for('auth.login'))
#     return render_template('auth/password_request_form.html',
#                            title='Reset Password', form=form)
    
# @bp.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     user = User.verify_reset_password_token(token)
#     if not user:
#         flash('Your link is invalid. Redirecting you back home in a few seconds', 'danger')
#         time.sleep(3)
#         return redirect(url_for('home'))
#     form = PasswordResetForm()
#     if form.validate_on_submit():
#         user.password = form.new_password.data
#         db.session.commit()
#         flash('Success, your password has been reset. Login with the new password', 'success')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/reset_password_confirm.html', form=form)
# @bp.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             flash(f"Hi, {current_user.username}. Welcome back!", 'success')
#             return redirect(next_page) if next_page else redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('auth/login.html', title='Login', form=form)


# @bp.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))



# def save_post_image(post_image):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(post_image.filename)
#     post_fn = random_hex + f_ext
#     post_path = os.path.join(bp.root_path, 'static/post_pics', post_fn)
#     post_image.save(post_path)
#     return post_fn

# @bp.route('/stripe/checkout')
# @login_required
# def get_publishable_key():
#     '''Define the publishable key and return a json object'''
#     stripe_config = {"publicKey": Config.stripe_publishable_key}
#     return jsonify(stripe_config)

# stripe.api_key = Config.stripe_secret_key

# @bp.route("/stripe/checkout-session")
# def create_checkout_session():
#     domain_url = Config.domain_url
#     stripe.api_key = Config.stripe_secret_key

#     try:
#         # Create new Checkout Session for the order
#         # Other optional params include:
#         # [billing_address_collection] - to display billing address details on the page
#         # [customer] - if you have an existing Stripe Customer ID
#         # [payment_intent_data] - lets capture the payment later
#         # [customer_email] - lets you prefill the email input in the form
#         # For full details see https:#stripe.com/docs/api/checkout/sessions/create

#         # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
#         checkout_session = stripe.checkout.Session.create(
#             success_url = domain_url + '/stripe/success?session_id={CHECKOUT_SESSION_ID}',
#             cancel_url = domain_url + '/stripe/cancelled',
#             payment_method_types=["card"],
#             mode="payment",
#             line_items=[
#                 {
#                     "name": "Flaskgram Premium Payment",
#                     "quantity": 1,
#                     "currency": "usd",
#                     "amount": "200",
#                 }
#             ]
#         )
#         return jsonify({"sessionId": checkout_session["id"]})
#     except Exception as e:
#         return jsonify(error=str(e)), 403

# @bp.route('/<username>', methods=['GET'])
# @login_required
# def user_profile(username):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = Post.query.filter_by(author=user)\
#         .order_by(Post.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     form = UpdateAccountForm()
#     form.username.data = user.username
#     form.email.data = user.email
#     form.about_me = user.bio   
#     user_followers,user_following = set(user.followers), len(set(user.followed))
#     no_followers =  len(user_followers)
#     current_user_following = set(current_user.followed)
#     exist_intersection = current_user_following.intersection(user_followers)
#     no_exist_intersection = len(exist_intersection)
#     exist_follows = current_user_following.isdisjoint(user_followers)
#     image_file = f'https://{Config.AWS_BUCKET}.s3.amazonaws.com/profile_pics/Profile_pics/'+ str(user.image_file)
#     return render_template('user.html', title='Your Account',
#                            image_file=image_file, exist_follows=exist_follows, exist_intersection=exist_intersection, user_followers=user_followers, user_following=user_following, no_exist_intersection=no_exist_intersection, no_followers=no_followers, form=form,post=post, posts=posts, user=user)

# @bp.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()
#     if request.method == "POST":
#         if form.validate_on_submit():
#             if form.picture.data:
#                 picture_file = save_picture(form.picture.data, 'profile')
#                 current_user.image_file = picture_file
#             current_user.username = form.username.data
#             current_user.email = form.email.data
#             current_user.bio = form.bio.data
#             db.session.commit()
#             flash(f'Your account has been updated, {current_user.username}!', 'success')
#             return redirect(url_for('account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#         form.bio.data = current_user.bio
#     image_file = f'https://{Config.AWS_BUCKET}.s3.amazonaws.com/profile_pics/Profile_pics/'+ str(current_user.image_file)
#     return render_template('account.html', title='Account',
#                            image_file=image_file, form=form)
# @bp.route('/<string:username>/notifications')
# @login_required
# def get_notifications(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('notifications.html', user=user)

# @bp.route('/edit_admin_profile/<int:id>', methods=['GET', 'POST'])
# #@admin_required
# @login_required
# def edit_profile_admin(id):
#     user = User.query.get_or_404(id)
#     form = UpdateAdminAccountForm(user=user)
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_file = save_picture(form.picture.data)
#             current_user.image_profile = picture_file
#         user.email = form.email.data
#         user.username = form.username.data
#         user.confirmed = form.confirmed.data
#         user.role = Role.query.get(form.role.data)
#         user.bio = form.bio.data
#         db.session.add(user)
#         flash('Your profile is updated!', 'success')
#         return redirect(request.referrer)
#     form.email.data = user.email
#     form.username.data = user.username
#     form.bio = user.bio
#     form.role.data = user.role_id
#     form.confirmed.data = user.confirmed
#     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
#     return render_template('edit_admin_profile.html', image_file=image_file, form=form, user=user)

# @bp.route("/<string:username>/post/new", methods=['GET', 'POST'])
# @login_required
# #@check_confirmed
# def new_post(username):
#     ''' Creates a new post'''
#     user = User.query.filter_by(username=username).first_or_404()
#     form = PostForm()
#     if request.method == 'POST':
#         if form.validate_on_submit() and form.post_image.data: 
#             #post_photo = url_for('static', filename='profile_pics/' + post_file)   
#             #post_photo = current_user.posts.post_image
#             post_language = guess_language(form.content.data)
#             if post_language == 'UNKNOWN' or len(post_language) > 7:
#                 post_language = ''
        
#             post_file = save_picture(form.post_image.data, 'post')
#             if not isinstance(post_file, list):
#                 post = Post(tag=form.tag.data, content=form.content.data, author=current_user, post_image =post_file, language = post_language)
#                 db.session.add(post)
#                 db.session.commit()
#             elif isinstance(post_file, list):
#                 for image in post_file:
#                     post = Post(tag=form.tag.data, content=form.content.data, author=current_user, post_image =image, language = post_language)
#                     db.session.add(post)
#                 db.session.commit()
#             # '''We define a json object to itnerface with Pusher client activity feed'''
#             # data = {
#             #     'id': f"post-{post.id}",
#             #     'title': request.form.get('title'),
#             #     'content': request.form.get('content'),
#             #     'author': request.form.get('author'),
#             #     'date_posted' : request.form.get('date_posted'),
#             #     'status': 'active',
#             #     'event_name': 'added'
#             # }
#             # try:
#             #     pusher.trigger('flaskgram', 'post-added', data)
#             # except:
#             #     flash('You have no internet connection at the moment', 'info')
#             #     #raise ConnectionRefusedError
                
#             flash(f'{current_user.username}, your post has been created!', 'success')
#             '''send a notification email to each of the user's followers'''
#             send_post_notification_email(user.followers, post=post, user=user, date_posted = post.date_posted.strftime('%a,%B,%H, %p'))
#             #send_post_notification_whatsapp(user)
#             return redirect(url_for('home'))
#             return jsonify(data)
          
#     #post_photo = url_for('static', filename='post_pics/' + save_picture(form.post_image.data, 'post'))   
#     return render_template('create_posts.html', title='New Post', 
#                            form=form, legend='New Post')

# @bp.route("/post/<int:post_id>")
# #@check_confirmed
# def post(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('posts.html', title=post.title, post=post)
    

# @bp.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @login_required
# #@check_confirmed
# def update_post(post_id):

#     ''' takes in a specific user_id(attached to the current user), and updates the post belonging to them''' 

#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:  #Only current logged in user should be able to post
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_posts.html', title='Update Post',
#                            form=form, legend='Update Post')


# @bp.route("/post/<int:post_id>/delete", methods=['POST'])
# @login_required
# @check_confirmed
# def delete_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted!', 'success')
#     return redirect(url_for('home'))


# @bp.route("/user/<string:username>")
# @check_confirmed
# def user_posts(username):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = Post.query.filter_by(author=user)\
#         .order_by(Post.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     return render_template('user_posts.html', posts=posts, user=user)



# @bp.route("/post/<int:post_id>/comment/comment_id")
# def comment(post_id, comment_id):
#     comment = Comment.query.get_or_404(comment_id)
#     return render_template('comments.html', title=comment.title, comment=comment)

# @bp.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
# @login_required
# @check_confirmed
# def create_comment(post_id):

#      ''' Create the ability to comment '''
#      form = CommentForm()
#      if form.validate_on_submit():
#           comment = Comment(title=form.title.data, content=form.content.data)
#           db.session.add(comment)
#           #db.session.rollback()
#           db.session.commit()
#           flash(f'{current_user.username}, Your comment has been posted!', 'success')
#           return redirect(url_for('home'))
#      return render_template('create_comments.html', title='Comment', form=form, legend="Write your comment!")


# @bp.route('/<action>/<string:username>', methods= ['POST'])
# @login_required
# #@check_confirmed
# def follow_action(action, username):
#     form = follow_unfollowForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=username).first_or_404()
#         if action == 'follow':
#             current_user.follow(user)
#             db.session.commit()
#             recme2_endpoint = 'https://rec2me.com/api/event'
#             recme2_params = Config.REC2ME_API_KEY
#             requests.post(f'{recme2_endpoint}/{recme2_params}/?userId ={current_user.id}&itemId={user.id}')
#             flash(f"Awesome! You are now following {username}!", 'success')
#         elif action == 'unfollow':
#             current_user.unfollow(user)
#             db.session.commit()
#             flash(f'You have stopped following {username}', 'info')
#     return redirect(request.referrer)
           
# @bp.route('/<username>/<string:action>')
# @login_required
# def post_notifs(username, action):
#     user = User.query.filter_by(username=username)
#     if action == 'yes':
#         current_user.receive_notifs =  True
#         db.session.commit()
#         flash(f'You will be receiveing email and whatsapp notifications from {username}', 'success')
#     elif action == 'no':
#         current_user.receive_notifs = False  
#         db.session.commit()    
#         flash(f'You wont be receiving email and whastsapp otifications from {username}', 'success')  
#     return redirect(request.referrer)
    
# @bp.route('/<username>/followers')
# @login_required
# def all_followers(username):
#     selected_user = User.query.filter_by(username=username).first_or_404()
#     return render_template('followers.html', selected_user=selected_user)

# @bp.route('/<string:username>/following')
# @login_required
# def get_following(username):   
#     selected_user = User.query.filter_by(username=username).first_or_404()
#     selected_user_following = set(selected_user.followed)
#     return render_template('following.html', selected_user_following=selected_user_following, selected_user=selected_user)
# @bp.route('/<string:username>/savedposts')
# @login_required
# def get_saved_posts(username):   
#     selected_user = User.query.filter_by(username=username).first_or_404()
#     saved_posts = SavedPosts.query.filter_by(user_id = selected_user.id).first()
#     return render_template('savedposts.html', saved_posts = saved_posts, selected_user=selected_user)

# @bp.route('/like/<int:post_id>/<action>')
# @login_required
# #@check_confirmed
# def like_action(post_id, action):
#     '''ROute for liking and unliking a post'''
#     post = Post.query.filter_by(id=post_id).first_or_404()
#     if action == 'like':
#         current_user.like_post(post)
#         db.session.commit()
#     if action == 'unlike':
#         current_user.unlike_post(post)
#         db.session.commit()
#     return redirect(request.referrer)
# @bp.route('/bookmark/<int:post_id>/<action>')
# @login_required
# #@check_confirmed
# def bookmark(post_id, action):
#     '''ROute for bookmarking and unbookmarking a post'''
#     post = Post.query.filter_by(id=post_id).first_or_404()
#     if action == 'save':
#         current_user.save_post(post)
#         db.session.commit()
#         flash("You have saved this post", 'success')
#     if action == 'unsave':
#         current_user.unsave_post(post)
#         db.session.commit()
#         flash('You have removed this post from your saved list', 'info')
#     return redirect(request.referrer)           



         
         
         

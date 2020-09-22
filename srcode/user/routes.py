from ..auth.decorator import admin_required
from ..essearch import add_to_index
from sqlalchemy import func
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, g
from srcode import cache, db
from .forms import MessageForm, UpdateAccountForm, PostForm, CommentForm, follow_unfollowForm, UpdateAdminAccountForm, SearchForm
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from ..models import Message, Notification, SavedPosts, User, Post, Role, PostLike, Comment
from .email import send_post_notification_email
from flask_login import current_user, login_required
import requests
from datetime import datetime
from ..user import bp
from config import Config
from flask_babel import _
from guess_language import guess_language
from ..uploads3 import save_picture
from .decorator import check_confirmed
from flask_babel import _, get_locale


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm() 
        g.user_followers = get_following(current_user.username) 
        #g.current_user_messages = view_messages() 
    g.locale = str(get_locale())  


@bp.route("/home")
@login_required
#@check_confirmed
def home():
    posts = current_user.followed_posts()
    return render_template('main/home.html', title='Home', posts=posts)
  

@bp.route("/about")
#@login_required
#@check_confirmed
@cache.cached(timeout=50)
def about():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('main/about.html',  posts=posts, title='All posts')  

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('user.home'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, 5)
    next_url = url_for('user.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * 5 else None
    prev_url = url_for('user.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('main/search.html', title=_('Search'), posts=posts,
                           next_url=next_url, total = total, prev_url=prev_url)  
    
@bp.route('/trending', methods = ['GET', 'POST'])
@cache.cached(timeout=50, key_prefix = 'trending_posts')
def get_trending():
    posts = db.session.query(Post).outerjoin(PostLike).group_by(Post.id).order_by(func.count().desc()).all() 
    #posts = Post.query.order_by(Post.likes.desc())
    return render_template('main/trending.html', posts = posts)

@bp.route('/<username>', methods=['GET'])
@login_required
def user_profile(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    form = UpdateAccountForm()
    form.username.data = user.username
    form.email.data = user.email
    form.about_me = user.bio   
    user_followers,user_following = set(user.followers), len(set(user.followed))
    no_followers =  len(user_followers)
    current_user_following = set(current_user.followed)
    exist_intersection = current_user_following.intersection(user_followers)
    no_exist_intersection = len(exist_intersection)
    exist_follows = current_user_following.isdisjoint(user_followers)
    image_file = f'https://{Config.AWS_BUCKET}.s3.amazonaws.com/profile_pics/Profile_pics/'+ str(user.image_file)
    return render_template('user/user.html', title='Your Account',
                           image_file=image_file, exist_follows=exist_follows, exist_intersection=exist_intersection, user_followers=user_followers, user_following=user_following, no_exist_intersection=no_exist_intersection, no_followers=no_followers, form=form,post=post, posts=posts, user=user)

@bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data, 'profile')
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.bio = form.bio.data
            db.session.commit()
            flash(f'Your account has been updated, {current_user.username}!', 'success')
            return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    image_file = f'https://{Config.AWS_BUCKET}.s3.amazonaws.com/profile_pics/Profile_pics/'+ str(current_user.image_file)
    current_user_messages = current_user.messages_received.order_by(
        Message.date_read.desc())
    return render_template('user/account.html', title='Account',
                           image_file=image_file, current_user_messages=current_user_messages, form=form)
@bp.route('/notifications')
@login_required
def get_notifications():
    last_notifications = request.args.get('since',0.0, type=float)
    user_notifications = current_user.notifications.filter(
    Notification.timestamp > last_notifications).order_by(Notification.timestamp.asc())
    return jsonify([{
    'name' : notif.name,
    'data' : notif.get_json(),
    'timestamp' : notif.timestamp 
    } for notif in user_notifications])
        
@bp.route('/edit_admin_profile/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = UpdateAdminAccountForm(user=user)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_profile = picture_file
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.bio = form.bio.data
        db.session.add(user)
        flash('Your profile is updated!', 'success')
        return redirect(request.referrer)
    form.email.data = user.email
    form.username.data = user.username
    form.bio = user.bio
    form.role.data = user.role_id
    form.confirmed.data = user.confirmed
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user/edit_admin_profile.html', image_file=image_file, form=form, user=user)

@bp.route("/<string:username>/post/new", methods=['GET', 'POST'])
@login_required
#@check_confirmed
def new_post(username):
    ''' Creates a new post'''
    user = User.query.filter_by(username=username).first_or_404()
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit() and form.post_image.data: 
            #post_photo = url_for('static', filename='profile_pics/' + post_file)   
            #post_photo = current_user.posts.post_image
            post_language = guess_language(form.content.data)
            if post_language == 'UNKNOWN' or len(post_language) > 7:
                post_language = ''
            
            post_file = save_picture(form.post_image.data, 'post')
            if not isinstance(post_file, list):
                post = Post(tag=form.tag.data, content=form.content.data, author=current_user, post_image =post_file, language = post_language)
                db.session.add(post)
                db.session.commit()
            for image in post_file:
                post = Post(tag=form.tag.data, content=form.content.data, author=current_user, post_image =image, language = post_language)
                db.session.add(post)
            db.session.commit()    
            flash(f'{current_user.username}, your post has been created!', 'success')
            '''send a notification email to each of the user's followers'''
            send_post_notification_email(user.followers, post=post, user=user, date_posted = post.date_posted.strftime('%a,%B,%H, %p'))
            return redirect(url_for('user.home'))
            return jsonify(data)
          
    #post_photo = url_for('static', filename='post_pics/' + save_picture(form.post_image.data, 'post'))   
    return render_template('user/create_posts.html', title='New Post', 
                           form=form, legend='New Post')

@bp.route("/post/<int:post_id>")
#@check_confirmed
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('main/posts.html', post=post)
    

@bp.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
#@check_confirmed
def update_post(post_id):
    ''' takes in a specific user_id(attached to the current user), and updates the post belonging to them''' 
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:  #Only current logged in user should be able to post
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.tag = form.tag.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('user.post', post_id=post.id))
    elif request.method == 'GET':
        form.tag.data = post.tag
        form.content.data = post.content
    return render_template('user/create_posts.html', title='Update Post',
                           form=form, legend='Update Post')


@bp.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
@check_confirmed
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@bp.route("/user/<string:username>")
@check_confirmed
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user/user_posts.html', posts=posts, user=user)



@bp.route("/post/<int:post_id>/comment/comment_id")
def comment(post_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return render_template('user/comments.html', title=comment.title, comment=comment)

@bp.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
@login_required
@check_confirmed
def create_comment(post_id):
     ''' Create the ability to comment '''
     form = CommentForm()
     if form.validate_on_submit():
          comment = Comment(title=form.title.data, content=form.content.data)
          db.session.add(comment)
          db.session.commit()
          flash(f'{current_user.username}, Your comment has been posted!', 'success')
          return redirect(url_for('home'))
     return render_template('user/create_comments.html', title='Comment', form=form, legend="Write your comment!")


@bp.route('/<action>/<string:username>', methods= ['POST'])
@login_required
#@check_confirmed
def follow_action(action, username):
    form = follow_unfollowForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first_or_404()
        if action == 'follow':
            current_user.follow(user)
            db.session.commit()
            recme2_endpoint = 'https://rec2me.com/api/event'
            recme2_params = Config.REC2ME_API_KEY
            requests.post(f'{recme2_endpoint}/{recme2_params}/?userId ={current_user.id}&itemId={user.id}')
            flash(f"Awesome! You are now following {username}!", 'success')
        elif action == 'unfollow':
            current_user.unfollow(user)
            db.session.commit()
            flash(f'You have stopped following {username}', 'info')
    return redirect(request.referrer)
           
@bp.route('/<username>/<string:action>')
@login_required
def post_notifs(username, action):
    user = User.query.filter_by(username=username)
    if action == 'yes':
        current_user.receive_notifs =  True
        db.session.commit()
        flash(f'You will be receiveing email notifications from {username}', 'success')
    elif action == 'no':
        current_user.receive_notifs = False  
        db.session.commit()    
        flash(f'You wont be receiving email notifications from {username}', 'success')  
    return redirect(request.referrer)
    
@bp.route('/<username>/followers')
@login_required
def all_followers(username):
    selected_user = User.query.filter_by(username=username).first_or_404()
    return render_template('user/followers.html', selected_user=selected_user)

@bp.route('/<string:username>/following')
@login_required
def get_following(username):   
    selected_user = User.query.filter_by(username=username).first_or_404()
    selected_user_following = set(selected_user.followed)
    return render_template('user/following.html', selected_user_following=selected_user_following, selected_user=selected_user)

@bp.route('/<string:username>/savedposts')
@login_required
def get_saved_posts(username):   
    selected_user = User.query.filter_by(username=username).first_or_404()
    user_saved_posts = SavedPosts.query.filter_by(user_id = selected_user.id).all()
    return render_template('user/savedposts.html', user_saved_posts = user_saved_posts, selected_user=selected_user)

@bp.route('/like/<int:post_id>/<action>')
@login_required
#@check_confirmed
def like_action(post_id, action):
    '''ROute for liking and unliking a post'''
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

@bp.route('/videochat')
@login_required
def videochat():
    return render_template('user/videochat.html')
    
@bp.route('/video/connect')
@login_required
def connect_video():
    username = request.get_json(force=True).get('username')
    if not username:
        abort(401)
    #Initaitve connection by getting the access key
    token = AccessToken(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_API_KEY, Config.TWILIO_SECRET_KEY, identity=username)     
    token.add_grant(VideoGrant(room='Private Video Call'))
    return {'token' : token.to_jwt().decode()}

@bp.route('/send/message/<string:recepient>', methods = ['GET','POST'])   
@login_required
def send_message(recepient):
    user = User.query.filter_by(username=recepient).first_or_404()   
    form = MessageForm()   
    if form.validate_on_submit():
        msg = Message(sender= current_user, recepient=user, body = form.message.data)
        db.session.add(msg)
        user.add_notification('unread_messages', user.new_messages())
        db.session.commit()
        flash('Your message has been sent', 'success')
        return redirect(url_for('home'))     
    user_name = user.username
    return render_template('user/send_message.html', user_name=user_name, form=form)

@bp.route('/view/messages')
@login_required
def view_messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_messages', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    current_user_messages = current_user.messages_received.order_by(
        Message.date_read.desc())
    return render_template('user/view_messages.html', current_user_messages=current_user_messages)
@bp.route('/bookmark/<int:post_id>/<action>')
@login_required
#@check_confirmed
def bookmark(post_id, action):
    '''ROute for bookmarking and unbookmarking a post'''
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'save':
        current_user.save_post(post)
        db.session.commit()
        flash("You have saved this post", 'success')
    if action == 'unsave':
        current_user.unsave_post(post)
        db.session.commit()
        flash('You have removed this post from your saved list', 'info')
    return redirect(request.referrer)           


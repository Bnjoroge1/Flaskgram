from datetime import datetime
import jwt, time
from srcode import cache, db, login_manager, manager, bcrypt
from flask_login import UserMixin
from flask import request
from config import Config, EmailConfig
from .essearch import add_to_index, remove_from_index, query_index



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

''' This is an association table that is not declared like other tables in the db schema. refer to self-referential db relationships '''
followers = db.Table('followers',
db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(
        username='admin',
        email="ad@min.com",
        password="adminpass",
        admin=True,
        confirmed=True,
        confirmed_on=datetime.datetime.now())
    )
    db.session.commit()
class SearchableMixin(object):
    '''Class that represents the SQLAlchemy objects of the Elastic Search'''
    @classmethod
    def search(cls, expression, page, per_page):
        ''' Handles the core search fuctionality.
        cls param is used to access the class objects without instatiating the objects.
        expresion == actual query,
        page and per pae arge used for pagination of the results'''
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        results = [(value, field) for value, field in enumerate(range(len(ids)))]
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(results, value = cls.id)), total
        
    @classmethod
    def before_commit(cls, session):
        '''Used to perfom certain operations before committing to the database'''
        session._changes = {
            'add' : list(session.new), 
            'update' : list(session.dirty),
            'delete' : list(session.deleted)
        }
    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None
    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)          

class User(db.Model, UserMixin):
    '''User Clas INherits from both the standard UserMixin and the Searchable Mixin for full text Search'''
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email == EmailConfig.MAIL_USERNAME:
            self.admin == True
        else:
            self.admin == False
    def ping(self):
        '''Updates the last seen datetime now'''
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    
        '''A bitwise and operation that checks the given arguments and returns a bool value'''
    @cache.memoize(10)
    def can(self, permissions):
        '''Check what a user can do'''
        return self.role is not None and \
        (self.role.permissions & permissions) == permissions
    @cache.memoize(10)
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    #__searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,index=True) 
    email = db.Column(db.String(120), unique=True, index=True)
    image_file = db.Column(db.String(20), default= "default.png")
    social = db.Column(db.String(64), unique=True) 
    phone_number = db.Column(db.Integer, unique = True)
    password = db.Column(db.String(60), unique = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy= True)
    bio =  db.Column(db.String(140), default= 'Hey there I am using this app!')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    registered_on = db.Column(db.DateTime, nullable=True)
    admin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, nullable=True, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    receive_notifs = db.Column(db.Boolean, default = False)
    
    def set_user_password(self, form_password):
        self._password = bcrypt.generate_password_hash(form_password)
        
    def check_password(self, form_password):
        return bcrypt.check_password_hash(self._password, form_password)
    '''FOllowed relationship table is used to model the relationship between the user and the users s/he has followed'''
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    @cache.memoize(10)
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        ''' Queries from the db for the posts belonging to users that current user heas followed and sorts them in a decending order by the time it was posted'''
        page = request.args.get('page', 1, type=int)
        #Getting posts from the users that the user has followed
        followed =  Post.query.join(
        followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        ''' Getting your own posts in the same timeline as those of those you have followed
        in your timeline by joining the two(union) and orders them by the day posted. '''
        own_posts =  Post.query.filter_by(user_id = self.id)
        return followed.union(own_posts).order_by(
                Post.date_posted.desc()).paginate(page=page, per_page=5) 

    '''Using jwt to validate password requests instead of itsdangerous'''
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
        {'reset_password': self.id, 'exp': time() + expires_in},
            Config.SECRET_KEY, algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, Config.SECRET_KEY,
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
             
    #Relationship column for a like and a user
    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic'
    )
  
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)
   
    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()
    @cache.memoize(10)
    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    saved = db.relationship(
            'SavedPosts',
            foreign_keys='SavedPosts.user_id',
            backref='user', lazy='dynamic'
    )
        
    def save_post(self, post):
        if not self.has_saved_post(post):
            save = SavedPosts(user_id = self.id, post_id = post.id)
            db.session.add(save)
    
    def unsave_post(self, post):
        if self.has_saved_post(post):
            SavedPosts.query.filter_by(
                user_id = self.id,
                post_id = post.id).delete()
    @cache.memoize(10)
    def has_saved_post(self, post):
        return SavedPosts.query.filter(
            SavedPosts.user_id == self.id,
            SavedPosts.post_id == post.id).count() > 0

    def number_of_saved_posts(self):
        return SavedPosts.query.filter_by(user_id = self.id).count()

    @staticmethod
    def add_self_follows():
        ''' adds a self following for each user. makes it easier to update the follower script post deployment'''
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()    

    def __repr__(self):
           return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Permission:
    '''setting a permissions model for admin access.
    Anonymous:  0b00000000 (0x00) User who is not logged in. Read-only access to the application.
    User:  0b00000111 (0x07) Basic permissions to write articles and comments and to follow other users. This is the default for new users.
    Moderator: 0b00001111 (0x0f) Adds permission to suppress comments deemed offensive or inappropriate.
    Administrator: 0b11111111 (0xff) Full access, which includes permission to change the roles of other users.        
    '''
    FOLLOW = 0x01    #Only user has access
    COMMENT = 0x02         #ONly user has access to comment
    WRITE_ARTICLES = 0x04  #Only confirmed user has access to write articles
    MODERATE_COMMENTS = 0x08    #Only the mod and admin have access to moderate comments
    ADMINISTER = 0x80       #only th admin has full access

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    @cache.memoize(10)
    def insert_roles():
        roles = {
        'User': (Permission.FOLLOW |
        Permission.COMMENT |
        Permission.WRITE_ARTICLES, True),
        'Moderator': (Permission.FOLLOW |
        Permission.COMMENT |
        Permission.WRITE_ARTICLES |
        Permission.MODERATE_COMMENTS, False),
        'Administrator': (0xff, False)
        }
        for r in roles: 
            
            role = Role.query.filter_by(name=r).first()
            if role is None:    
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return f'Role{self.roles.get(self.name)}, {self.roles.get(self.default)}'

class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))



class Post(db.Model, SearchableMixin):
    __searchable__ = ['post_body']
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    
    saved_posts = db.relationship('SavedPosts', backref='saved', lazy=True)
    language = db.Column(db.String(7))
    post_image = db.Column(db.String(30), nullable=True)
    
    def __repr__(self):
        return f"Post('{self.user_id}', '{self.date_posted}')"

class SavedPosts(db.Model):
    id  = db.Column(db.Integer, primary_key = True)
    date_saved = db.Column(db.DateTime, default = datetime.utcnow, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f"Saved Post('{self.date_saved}', '{self.id}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    
    def __repr__(self):
        return f"Comment('{self.title}', '{self.date_posted}')"

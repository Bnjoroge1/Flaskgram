from flask import Flask, request, current_app, app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_share import Share
from flask_migrate import Migrate
from flask_script import Manager
from flask_mail import Mail
from sqlalchemy import MetaData
import logging, os, requests
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_bootstrap import Bootstrap
from config import CloudinaryConfig, Config, EmailConfig, PusherConfig
from flask_turbolinks import turbolinks
import redis
from pusher import Pusher
from rq import Queue
from flask_moment import Moment
from flask_babel import Babel, _
from flask_discussion import Discussion
from elasticsearch import Elasticsearch
#Set db path
basedir = os.path.abspath(os.path.dirname(__file__))

#app = Flask(__name__)

#Configure secret and api_key

#Instantiate Database, migrations, bcrypt and share classes
db = SQLAlchemy() 
discussion = Discussion()    
bcrypt = Bcrypt()
share = Share()
migrate = Migrate()
bootstrap = Bootstrap()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = _('You need to login first to access this page')
#COnfigur Blue Prints

# db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))



#turbolink = turbolinks()
manager = Manager()
mail = Mail()
r = redis.Redis()
q = Queue(connection=r)
moment = Moment()
babel = Babel()
MAX_FILE_LENGTH = Config.MAX_FILE_lENGTH

# if not app.debug:
#          if Config.MAIL_SERVER:
#               auth = None
#          if Config.MAIL_USERNAME or Config.MAIL_PASSWORD:
#               auth = (Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
#          secure = None
#          if Config.MAIL_USE_TLS: 
#                secure = ()
#          mail_handler = SMTPHandler(
#             mailhost=(Config.MAIL_SERVER, Config.MAIL_PORT,
#             fromaddr='no-reply@' + Config.MAIL_SERVER,
#             toaddrs=['mangucounsrec@gmail.com'], subject='Microblog Failure',
#             credentials=auth, secure=secure)
#          mail_handler.setLevel(logging.ERROR)
#          app.logger.addHandler(mail_handler)
def create_current_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    share.init_app(app)
    bcrypt.init_app(app)
    discussion.init_app(app)
    #turbolink.init_app(app)
    try:
        app.elasticsearch = Elasticsearch([Config.ELASTIC_SEARCH_URL])
    except  ConnectionRefusedError as connection_error:
        return f'sth went wrong {connection_error}'
    from srcode.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from srcode.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from srcode.user import bp as user_bp
    app.register_blueprint(user_bp)

    from srcode.community import community as community_bp
    app.register_blueprint(community_bp)

    from srcode.auth.oauth import google_blueprint as google_bp
    app.register_blueprint(google_bp)

    from srcode.auth.oauth import facebook_blueprint as facebook_bp
    app.register_blueprint(facebook_bp)

    from srcode.auth.oauth import github_blueprint as github_bp
    app.register_blueprint(github_bp)

    from srcode.auth.oauth import twitter_blueprint as twitter_bp
    app.register_blueprint(twitter_bp)
    with app.app_context():
        db.create_all()
        
    # with app.current_app_context():
    #     if db.engine.url.drivername == 'sqlite':
    #         migrate.init_app(app, db, render_as_batch=True)
    #     else:
    #         migrate.init_app(app, db)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/srcode.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flaskgram startup')
    return app

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(Config.LANGUAGES)

from srcode import models
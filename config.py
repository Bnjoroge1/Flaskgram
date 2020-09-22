import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
from urllib.parse import urlparse
class Config(object):
     SECRET_KEY =  os.environ.get('SECRET_KEY')
     SQLALCHEMY_TRACK_MODIFICATIONS = False
     SERVER_NAME = os.environ.get('SERVER_NAME')
     AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', None)
     AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY', None)
     AWS_BUCKET = os.environ.get('AWS_BUCKET', None)
     FLASKS3_ONLY_MODIFIED = True
     S3_LOCATION = os.environ.get('S3_LOCATION')
     S3_BUCKET_LOCATION = f'https://{AWS_BUCKET}.s3.{S3_LOCATION}.amazonaws.com/'
     safaricom_consumer_key = os.environ.get('safaricom_consumer_key', None)
     safaricom_consumer_secret = os.environ.get('safaricom_consumer_secret', default=None)
     POSTS_PER_PAGE = os.environ.get('POSTS_PER_PAGE')
     ELASTIC_SEARCH_URL = os.environ.get('ELASTIC_SEARCH_URL') or 'http://127.0.0.1:9200'
     stream_api_key = os.environ.get('stream_api_key', None)
     stream_secret_key = os.environ.get('stream_secret_key', None)
     TWILIO_ACCOUNT_SID =  os.environ.get('TWILIO_ACCOUNT_SID')
     TWILIO_API_KEY = os.environ.get('TWILIO_API_KEY')
     TWILIO_SECRET_KEY = os.environ.get('TWILIO_SECRET_KEY')
     GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration")
     REC2ME_API_KEY = os.environ.get('REC2ME_API_KEY', None)
     OAUTH_CREDENTIALS = {
    'facebook': {
        'id': os.environ.get('FACEBOOK_ID'),
        'secret': os.environ.get('FACEBOOK_SECRET_KEY')
    },
    'twitter': {
        'id': os.environ.get('TWITTER_API_KEY'),
        'secret': os.environ.get('TWITTER_API_SECRET_KEY'),
        'Bearer_Token' : os.environ.get('TWITTER_BEARER_TOKEN')
    },
    'google' : {
        'client_id' : os.environ.get('GOOGLE_CLIENT_ID'),
        'client_secret' : os.environ.get('GOOGLE_CLIENT_SECRET'),
        'OAUTHLIB_RELAX_TOKEN' : True
    },
    'github': {
        'client_id' : os.environ.get('GITHUB_CLIENT_ID'),
        'client_secret' : os.environ.get('GITHUB_CLIENT_SECRET')
    }
}
     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') 
     SQLALCHEMY_POOL_SIZE=20
     SQLALCHEMY_POOL_TIMEOUT=300
     RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_COPY_SITE_KEY') or 'not-available'
     RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')  or 'not-available'
     stripe_publishable_key = os.environ.get('STRIPE_PUBLISHABLE_KEY')
     stripe_secret_key = os.environ.get('STRIPE_SECRET_KEY')
     stripe_product_id = os.environ.get('STRIPE_PRODUCT_ID')
     domain_url = os.environ.get('domain_url')
     LANGUAGES = ['en','sw', 'fr']
     MAX_FILE_lENGTH = os.environ.get('MAX_FILE_LENGTH')
class EmailConfig(object):
     #Gmail settings and config
     MAIL_SERVER = os.environ.get('MAIL_SERVER')
     MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
     MAIL_USE_TLS = True
     WTF_CSRF_ENABLED = True

     #Gmail Authentication
     DEFAULT_MAIL_SENDER = os.environ.get('DEFAULT_MAIL_SENDER')
     MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
     MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
     #ADMINS = os.environ.get('ADMINS')  
     PASSWORD_SALT = os.environ.get('PASSWORD_SALT')   

class CloudinaryConfig(object):
    cloud_name = os.environ.get('cloud_name')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

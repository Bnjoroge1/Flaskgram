from config import Config
import requests
from requests.auth import HTTPBasicAuth
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.twitter import make_twitter_blueprint


#Safaricom Daraja API Integrations
consumer_key = Config.safaricom_consumer_key
consumer_secret = Config.safaricom_consumer_secret

#Make request to generate access token
def get_access_token():
     
     api_endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
     response = requests.get(api_endpoint, auth= HTTPBasicAuth(consumer_key,consumer_secret)).json()
     return response['access_token']


#Google Login
google_blueprint = make_google_blueprint(
    client_id = Config.OAUTH_CREDENTIALS['google']['client_id'],
    client_secret = Config.OAUTH_CREDENTIALS['google']['client_secret'],
    scope = [
        'openid',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email',
        ],
        redirect_to = 'google.login',
)


#Facebook Login
facebook_blueprint = make_facebook_blueprint(
    client_id = Config.OAUTH_CREDENTIALS['facebook']['id'],
    client_secret  = Config.OAUTH_CREDENTIALS['facebook']['secret'],
    scope = 'email',
    redirect_to = 'facebook.login'
)   

#GIthub Login
github_blueprint = make_github_blueprint(
    client_id = Config.OAUTH_CREDENTIALS['github']['client_id'],
    client_secret  = Config.OAUTH_CREDENTIALS['github']['client_secret'],
    scope = ['user, repo'],
    redirect_to = 'github.login'
) 
#Twiter Login
twitter_blueprint = make_twitter_blueprint(
    api_key = Config.OAUTH_CREDENTIALS['twitter']['id'],
    api_secret  = Config.OAUTH_CREDENTIALS['twitter']['secret'],
    redirect_to = 'login_twitter',
)



          
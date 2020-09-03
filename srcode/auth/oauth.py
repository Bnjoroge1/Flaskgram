from config import Config
from flask import current_app, url_for, redirect, request
from rauth import OAuth2Service, OAuth1Service
import json, requests
from srcode import app
from requests.auth import HTTPBasicAuth
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.twitter import make_twitter_blueprint
class OAuthSignIn(object):
     providers = None

     def __init__(self, provider_name):
          self.provider_name = provider_name
          credentials = Config.OAUTH_CREDENTIALS.get(self.provider_name)
          self.consumer_id = credentials['id']
          self.consumer_secret = credentials['secret']
     
     '''authorise function'''
     def authorise(self):
          pass
     ''' callback function'''
     def callback(self):
          pass

     '''returns the callback(access point after authorisation by the provider'''
     def get_callback_url(self):
          'Function that returns the callback url for a specific provider name'
          return url_for('oauth_callback', provider = self.provider_name,
          _external=True)  # external, parameter is set to True meaning it's accessed from outside
          
     @classmethod   #it returns the info about the various api providers
     def get_provider(cls, provider_name):
          '''lookup the correct OAuthSignIn instance given a provider name. This method uses introspection to find all the OAuthSignIn subclasses, and then saves an instance of each in a dictionary.'''
          
          if cls.providers is None:
               cls.providers = {}
               '''Loop through the subclassess of Oauth's base class(i.e facebook, twitter etc), instantiate that class and assign it to providers dictionary'''
          
               for provider_class in cls.__subclasses__():
                    provider = provider_class()
                    cls.providers[provider.provider_name] = provider
          
          return cls.providers[provider_name]

class FaceBookSignIn(OAuthSignIn):
     '''uses Oauth2 for authentication'''
     def __init__(self):
          super(FaceBookSignIn, self).__init__('facebook')
          self.service = OAuth2Service(
               name = 'facebook',
               client_id=self.consumer_id,
               client_secret = self.consumer_secret,
               authorize_url = 'https://graph.facebook.com/oauth/authorize',
               access_token_url = 'https://graph.facebook.com/oauth/access_token',
               base_url = 'https://graph.facebook.com/'
          )
     
     '''Code for USER AUTHENTICTION. After the redirect from the facebook route, it is responsible for authenticating the user given two parameters, the email'''
     def authorize(self):
             return redirect(self.service.get_authorize_url(
            scope= 'email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )
     
     def callback(self):
          def decode_json(payload):
               return json.loads(payload.decode('utf-8'))

          if 'code' not in request.args:
               return None, None, None
          oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )

          ''' YOu get the response from facebook and convert it to json format. Then access the id and email'''
          me = oauth_session.get('me').json()
          
          return (
               'facebook$' + me['id'],
               #me.get('email')
               # Facebook does not provide the username,
               #  so the email of the user is used instead
               me.get('email')
                )

class TwitterSignIn(OAuthSignIn):
     '''Twitter uses Oauth1 for authentication'''
     def __init__(self):
          super(TwitterSignIn, self).__init__('twitter')
          self.service = OAuth1Service(
               name = 'twitter',
               consumer_key = self.consumer_id,
               consumer_secret = self.consumer_secret,
               request_token_url = 'https://api.twitter.com/oauth/request_token',
               authorize_url = 'https://api.twitter.com/oauth/authorize',
               access_token_url = 'https://api.twitter.com/oauth/access_token',
               base_url = 'https://api.twitter.com/1.1/'
          )
     
     def authorise(self):
          ''' Twiitter's Auth process. REQUESTS FOR A TOKEN FROM THE PROVIDER AND RECEIVES A LIST OF TWO ITEMS(OAUTH_CALLBACK) AND IS THEN USED FOR THE REDIRECT'''
          request_token = self.service.get_request_token(
          params={'oauth_callback': self.get_callback_url()}
          )
          session['request_token'] = request_token
          return redirect(self.service.get_authorize_url(request_token[0]))
     
     def callback(self):
          
          '''Twitter's callback. Refer to Miguel's Google LOgin Auth'''
          request_token = session.pop('request_token')
          if 'oauth_verifier' not in request.args:
               return None, None, None
          oauth_session = self.service.get_auth_session(
               request_token[0],
               request_token[1],
               data={'oauth_verifier': request.args['oauth_verifier']}
          )
          me = oauth_session.get('account/verify_credentials.json').json()
          social_id = 'twitter$' + str(me.get('id'))
          username = me.get('screen_name')
          return social_id, username, None   # Twitter does not provide email
          
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


#FAcebook Login
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



          
# manages the callback

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app 
from google.appengine.ext.webapp import template

import atom.http_core
import gdata.gauth
import web
import threading

class Config(object):
    APP_NAME = "Board Game Platform v 0.5"
    APP_PLACE = "boardplatform.appspot.com"
    APP_ROOT = "http://boardplatform.appspot.com"
    APP_REDIRECT = APP_ROOT + "/oauth2callback"
    APP_CATCH = APP_ROOT + "/catchtoken"
    CONSUMER_KEY = '740264759676.apps.googleusercontent.com'
    CONSUMER_SECRET = 'qElHcIt4TIAV9tf4Z9JjjXAW'
    SCOPES = ['https://docs.google.com/feeds/'] 
    DEBUG = True

class Session(threading.local):
    token = gdata.gauth.OAuth2Token(client_id = Config.CONSUMER_KEY, client_secret = Config.CONSUMER_SECRET,
                                        scope = ' '.join(Config.SCOPES), user_agent=Config.APP_PLACE)
    def __init__(self) :
        token = gdata.gauth.OAuth2Token(client_id = Config.CONSUMER_KEY, client_secret = Config.CONSUMER_SECRET,
                                        scope = ' '.join(Config.SCOPES), user_agent=Config.APP_PLACE)

session = Session()

class OAuthHandler(webapp.RequestHandler):
    def __init__(self):
        """Constructor for the OAuthSample object.
    
        Takes a consumer key and consumer secret, store them in class variables,
        creates a DocsService client to be used to make calls to
        the Documents List Data API.
    
        Args:
          CONSUMER_KEY: string Domain identifying third_party web application.
          CONSUMER_SECRET: string Secret generated during registration.
        """
    def post(self):
        self.redirect( session.token.generate_authorize_url(redirect_uri=Config.APP_REDIRECT) )
        
    def get(self):
        url = atom.http_core.Uri.parse_uri(self.request.uri)
        if 'error' in url.query:
            # The user declined the authorization request.
            # Application should handle this error appropriately.
            pass
        else :
            # This is the token instantiated in the first section.
            (session.token).get_access_token(url.query)
            self.response.out.write("Should redirect you to the create map page... Now!")
            self.redirect(Config.APP_ROOT+"/create");
        
class CatchTokenHandler(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        a_t = self.request.get('access_token')
        
        if not validate_access_token(a_t):
            self.error(400)
        
        session.regenerate_id()
        session['access_token'] = a_t

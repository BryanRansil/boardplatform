


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

__author__ = 'bryan.ransil@gmail.com (Bryan Ransil)'

import sys
import os.path
import getopt
import gdata.auth
import gdata.docs.service
import gdata.data
import gdata.acl.data
import gdata.docs.data
import gdata.docs.client

class Config(object):
    APP_NAME = "Board Game Platform v 0.5"
    DEBUG = True

class LoginHandler(webapp.RequestHandler):
    def __init__(self):
        """Constructor for the OAuthSample object.
    
        Takes a consumer key and consumer secret, store them in class variables,
        creates a DocsService client to be used to make calls to
        the Documents List Data API.
    
        Args:
          consumer_key: string Domain identifying third_party web application.
          consumer_secret: string Secret generated during registration.
        """
        self.consumer_key = '740264759676.apps.googleusercontent.com'
        self.consumer_secret = 'qElHcIt4TIAV9tf4Z9JjjXAW'
        self.gd_client = gdata.docs.service.DocsService()
    
    def _PrintFeed(self, feed):
        """Prints out the contents of a feed to the console.
   
        Args:
          feed: A gdata.docs.DocumentListFeed instance.
        """
        if not feed.entry:
            print 'No entries in feed.\n'
        else:
            print 'got something!\n'

    def post(self):
        client = gdata.docs.client.DocsClient(source=Config.APP_NAME)
        client.http_client.debug = Config.DEBUG
        
        self.gd_client.SetOAuthInputParameters(
                                               gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
                                               self.consumer_key, consumer_secret=self.consumer_secret)
        
        request_token = self.gd_client.FetchOAuthRequestToken()
        self.gd_client.SetOAuthToken(request_token)
        auth_url = self.gd_client.GenerateOAuthAuthorizationURL()
        self.response.out.write('<a href='+auth_url+'>Please open this in another tab and agree</a><br>')
        
        loginurl = 'https://accounts.google.com/o/oauth2/auth?&scope=https://docs.google.com/feeds/+https://docs.googleusercontent.com/+https://spreadsheets.google.com/feeds/&state=%2Fprofile&redirect_uri=http%3A%2F%2Fboardplatform.appspot.com%2Foauth2callback&response_type=code&client_id=740264759676.apps.googleusercontent.com'
        self.response.out.write('Once you have done that, please press this link: ' +
                                '<a href=' + loginurl + '>here</a><br>')
        
        
#        feed = client.GetResources()
 #       for entry in feed.entry:
  #=          print resource.resource_id.text, resource.GetResourceType()
        
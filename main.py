#!/usr/bin/env python
#
# Copyright 2011 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
__author__ = 'bryan.ransil@gmail.com (Bryan Ransil)'

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app 

import os.path
import gdata.data
import gdata.acl.data
import gdata.docs.client
import gdata.docs.data
import gdata.sample_util

import login
import oauth2

def CreateClient():
  """Create a Documents List Client."""
  client = gdata.docs.client.DocsClient(source=Config.APP_NAME)
  client.http_client.debug = Config.DEBUG
  # Authenticate the user with CLientLogin, OAuth, or AuthSub.
  try:
    gdata.sample_util.authorize_client(
        client,
        service=client.auth_service,
        source=client.source,
        scopes=client.auth_scopes
    )
  except gdata.client.BadAuthentication:
    exit('Invalid user credentials given.')
  except gdata.client.Error:
    exit('Login Error')
  return client

def CreateEmptyMap():
    """Goal: Create one or more maps in a collection"""
    client = CreateClient()
    col = gdata.docs.data.Resource(type='folder', title='You are AWESOME!')
    col = client.CreateResource(col)
    print 'Created collection:', col.title.text, col.resource_id.text
  
  
class MainHandler(webapp.RequestHandler):
    def get(self):
        # Set the cross origin resource sharing header to allow AJAX
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        #CreateEmptyMap();
        # Create a client class which will make HTTP requests with Google Docs server. 
        
        self.response.out.write('Hello World!')
        self.response.out.write(""" <form action='login' method='post' name ='login'>
            <input type = "hidden" name = "type" value="addMap" />
            <input type="submit" value="Hello Back!"/></form> """)
		
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/login', login.LoginHandler),
                                          ('/oauth2callback', oauth2.OAuthHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

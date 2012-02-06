
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app 

import os.path
import gdata.data
import gdata.acl.data
import gdata.docs.client
import gdata.docs.data


def CreateEmptyMap():
    """Goal: Create one or more maps in a collection"""
    client = CreateClient()
    col = gdata.docs.data.Resource(type='folder', title='You are AWESOME!')
    col = client.CreateResource(col)
    print 'Created collection:', col.title.text, col.resource_id.text
  
  
class MapHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Present")

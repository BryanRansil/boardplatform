
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app 

import os.path
import gdata.data
import gdata.docs.client
import gdata.docs.data
from gdata.docs.data import Resource

import oauth2


def CreateEmptyMap():
    """Goal: Create one or more maps in a collection"""
    
    col = gdata.docs.data.Resource(type='folder', title='You are AWESOME!')
    col = client.CreateResource(col)
    print 'Created collection:', col.title.text, col.resource_id.text
  
  
class MapHandler(webapp.RequestHandler):    
    def get(self):
        # Access the Google Documents List API.
        client = gdata.docs.client.DocsClient(source=oauth2.Config.APP_PLACE)
        client.ssl = True
        # This is the token instantiated in the first section.
        client = (oauth2.session.token).authorize(client)
        self.response.out.write("Creation Page<br>  ")
        documents_feed = client.get_all_resources()
        download_doc_feed = client.get_resources()

        for entry in documents_feed :
            if entry.title.text == "PC Screen" :
                #download_doc_feed.download_resource(entry)
                link = entry.get_resumable_edit_media_link()
                self.response.out.write(link.href)
                content = entry.content
                self.response.out.write(content.src)
                self.redirect(content)
                
                #self.response.out.write(link.ToString())#self.redirect(link);
                break
        #exper = docs_client.create_resource() needed an entry object, but haven't been able to find how to make one...
        
        
        #Creation code
        #col = Resource('folder', 'Map')
        #map = client.create_resource(col)
        #layer1 = Resource(type='drawing', title='Layer1')
        #client.create_resource(layer1, collection=map)
        #layer2 = Resource(type='drawing', title='Layer2')
        #client.create_resource(layer2, collection=map)
        
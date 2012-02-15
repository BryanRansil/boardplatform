
from __future__ import with_statement
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app 
from google.appengine.ext import db
from google.appengine.api import files
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore

import urllib
import urllib2

import os.path
import gdata.data
import gdata.docs.client
import gdata.docs.data
from gdata.docs.data import Resource

import oauth2

class downloadHandler(blobstore_handlers.BlobstoreDownloadHandler):   
    def importImage(self):
        file_name = files.blobstore.create(mime_type='image/png')
           # Open the file and write to it
            
        with files.open(file_name, 'a') as f:
            f.write('data')
    
        # Finalize the file. Do this before attempting to read it.
        files.finalize(file_name)
    
        # Get the file's blob key
        blob_key = files.blobstore.get_blob_key(file_name)
        blob_info = blobstore.BlobInfo.get(blob_key)
        
        self.send_blob(blob_info)

def CreateEmptyMap():
    """Goal: Create one or more maps in a collection"""
    
    col = gdata.docs.data.Resource(type='folder', title='You are AWESOME!')
    col = client.CreateResource(col)
  
  
class MapHandler(webapp.RequestHandler): 
    mydownloadHandler = downloadHandler()   
    def get(self):
        # Access the Google Documents List API.
        client = gdata.docs.client.DocsClient(source=oauth2.Config.APP_PLACE)
        client.ssl = True
        # This is the token instantiated in the first section.
        client = (oauth2.session.token).authorize(client)
        #self.response.out.write("Creation Page<br>  ")      
        
        #circle = gdata.data.MediaSource(content_type="image/png", file_name="PCScreen.png")
        #client.update_resource(layer1entry, media=circle)
        documents_feed = client.get_all_resources()
        download_doc_feed = client.get_resources()

        mapb = True
        l1b = True
        l2b = True
        content = client.download_resource_to_memory(documents_feed[0])
        
        for entry in documents_feed :
            if False :
                print "Fundamental logic is flawed"
            elif entry.title.text == 'Map' :
                mapb = False
                map = entry
            elif entry.title.text == "Layer1" :
                l1b = False
                layer1entry = entry
                link = entry.get_resumable_edit_media_link()
                content = entry.content
            elif entry.title.text == "Layer2" :
                l2b = False
                layer2entry = entry
            #elif entry.title.text == 'PC Screen' : #testing purposes
                #download_doc_feed.download_resource(entry)
                #
                
                #entry.title.text = 'Test on PC' This pair worked to rename it...
                #entry = client.Update(entry)
                
                #self.response.out.write(link.href).
                #self.response.out.write("<br>\n")
                
                #content = client._get_content(entry.content, auth_token = oauth2.session.token)
            
        
        self.response.out.write("<div id = 'left' style = 'position:absolute;left:0px;top:0px;width:15%'>")
        if mapb :
            self.response.out.write("In mapb!")
            col = Resource('folder', 'Map')
            map = client.create_resource(col)
        if l1b :
            self.response.out.write("In l1b!")
            layer1 = Resource(type='drawing', title='Layer1')
            layer1entry = client.create_resource(layer1, collection=map)
        if l2b :
            self.response.out.write("In l2b!")
            layer2 = Resource(type='drawing', title='Layer2')
            layer2entry = client.create_resource(layer2, collection=map)
            
            
        self.response.out.write('Left Buttons!<br>')
        self.response.out.write("<button type='button'>Create Box</button>")
        self.response.out.write("<button type='button'>Color</button>")
        self.response.out.write("</div>")
        self.response.out.write("<div id = 'center' style = 'position:absolute;top:0px;left:15%;width:70%'>")
        self.response.out.write('Main Drawing Area!')
        self.response.out.write("<div style = 'background-color:grey'>")
        self.response.out.write("<img id = 'incoming' src = '" + content.src + "'>" )
        
        #f = open("PCScreen.png")
        #file_size = os.path.getsize(f.name)
        #uploader = gdata.client.ResumableUploader(client, f, 'image/png', file_size)
        
        #new_entry = uploader.UploadFile('/feeds/upload/create-session/default/private/full', entry=layer1entry)
        #self.redirect(link);

        tag = entry.etag
        params = urllib.urlencode({
            'GData-Version' : 3.0,
            'If-Match' : tag,
            'Authorization' : oauth2.Config.APP_PLACE,
            'Content-Length' : 0,
            'Content-Type' : 'image/png',
            'Slug' : 'test.png'
        })
 #       urllib2.urlopen(link.href, params).read()
        
        self.response.out.write("</div>")
        
        self.response.out.write("<div style = 'position:relative;right:0%;top:-15px;background-color:black'>")
        #self.mydownloadHandler.importImage()
        self.response.out.write("</div>")
        
        self.response.out.write("<div id = 'right' style = 'position:absolute;right:0px;top:0px;width:15%'>")
        self.response.out.write('Right Options!<br>')
        self.response.out.write("<button type='button'>Edit Hidden Layer</button>")
        self.response.out.write("<button type='button'>Show Selected</button>")
        self.response.out.write("</div>")
     
class Map(db.Model):
    layer = db.StringProperty(required=True)
    title = db.StringProperty()
    image = db.BlobProperty()
        
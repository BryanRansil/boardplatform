
from __future__ import with_statement
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app 
from google.appengine.ext import db
from google.appengine.api import files
from google.appengine.api import urlfetch
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template

import gdata.data
import gdata.docs.client
import gdata.docs.data
from gdata.docs.data import Resource
import gdata.service
from svgfig.interactive import *
from django.utils import simplejson
import sys

import httplib, urllib, urllib2

import oauth2
import createmap

CHUNK_SIZE = 10485760

class ShapeHandler(webapp.RequestHandler):
    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.methods = ShapeHandlerMethods();
        
    def get(self):
        s = SVG("rect", x=10, y=10, width=60, height=60, id='star')
        
    def post(self):
        func = None
        action = self.request.get('action')
        if action:
            if action[0] == '_':
                self.error(403) # access denied
                return
            else:
                func = getattr(self.methods, action, None)

        if not func:
            self.error(404) # file not found
            return

        args = ()
        while True:
            key = 'arg%d' % len(args)
            val = self.request.get(key)
            if val:
                args += (simplejson.loads(val),)
            else:
                break
        result = func(*args)
        #self.response.out.write(simplejson.dumps(result))
        self.response.out.write(result)

class ShapeHandlerMethods:
    #Put a rect on the drawing layer1
    def DrawRect(self, *args):
        client = gdata.docs.client.DocsClient(source=oauth2.Config.APP_PLACE)
        client.ssl = True
            # This is the token instantiated in the oauth section.
        client = (oauth2.session.token).authorize(client)
        folders_feed = client.get_all_resources(uri='/feeds/default/private/full/-/folder')
        
        x = args[0]
        y = args[1]
        width = args[2]
        height = args[3]
        #Grab layer1
        for entry in folders_feed :
            if entry.title.text == 'Map' :
                map = entry
                break
        
        mapfeed = client.get_all_resources(uri=map.content.src)
        for entry in mapfeed:
            if entry.title.text == "Layer1" :
                l1b = False
                layer1entry = entry
                link = entry.get_resumable_edit_media_link()
                
        #Optional: download layer1 as an SVG
        content = client.download_resource_to_memory(layer1entry)
        oldcontent = content
        #Replace it's content with our content
        
        layer = '<svg version="1.1" width="800" height="600"><g id="box_0"><rect x="' + str(x) + '" y="' + str(y) + '" width="' + str(width) + '" height="' + str(height) + '" fill="blue" stroke="blue" stroke-width="4"></rect></g></svg>'
        #SVG("rect", x=10, y=10, width=60, height=60, id='star')
        #Stated that strings lack the attribue "_become_child" 
        #g.save("tmp.svg")
        #Reupload
        layer1entry.title = 'Updated title'
        
        #return (layer1entry.get_elements())[24].to_string() + (layer1entry.get_elements())[25].to_string()
        #response = client.put(link, layer1entry.to_string())
        #data = urllib.urlencode(layer)
        #conn = httplib.HTTPConnection(link)
        #headers = {"GData-Version" : 3, "Authorization" : client, "If-Match" : "*",
        #           "Content-Length" : 480000, "Content-Type" : "img/svg", 
        #           "X-Upload-Content-Length" : 480000, "X-Upload-Content-Type" : "img/svg" }
        #req = conn.request("POST", "", headers, data)
        
        file_name = files.blobstore.create(mime_type='application/octet-stream')
        
        with files.open(file_name, 'a') as f:
            f.write(layer)
        
        files.finalize(file_name)
        
        blob_key = files.blobstore.get_blob_key(file_name)
        
        #Blob has been uploaded. Now using the resumable uploader
        
        blob_info = blobstore.BlobInfo.get(blob_key)
        image = blob_info.open()
        file_size = blob_info.size
        
        #uploader = gdata.client.ResumableUploader(client, image, blob_info.content_type, file_size,
        #                                          chunk_size = CHUNK_SIZE, desired_class="StringProperty")
        #new_entry = uploader.UploadFile('/feeds/upload/create-session/default/private/full', 
        #                                entry = layer1entry)
        #updatedlayer1 = client.Update(layer1entry, media_source = ms)
        return "Hizy"

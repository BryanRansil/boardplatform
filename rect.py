
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

from atom import data
import gdata.data
import gdata.docs.client
import gdata.docs.data
from gdata.docs.data import Resource
import gdata.service
from svgfig.interactive import *
import sys
import simplejson

import httplib, urllib, urllib2

import oauth2
import createmap
import md5
import uuid
from urlparse import urlparse

CHUNK_SIZE = 10485760

class ShapeHandler(webapp.RequestHandler):
    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.methods = ShapeHandlerMethods();
        
    def get(self):
       self.response.out.write("Hellox!")
 
    def post(self):
        func = None
        action = self.request.get("action")
	if action:
            if action == '_':
                self.error(403) # access denied
                return
            elif action != 'DrawRect':
            	self.error(404) # file not found
            	return
	jsonstring = urllib.unquote(self.request.body) #simplejson.loads(self.request.body) #result = self.methods.DrawRect(*body) #parse this!
	reduced = jsonstring[:len(jsonstring)-1]
	loaded = simplejson.loads(reduced)
	returnval = self.methods.DrawRect(loaded['rect'][0])
	self.response.out.write(returnval)
        #self.response.out.write(simplejson.dumps(result))
        #self.response.out.write(result)

class ShapeHandlerMethods:
    #Put a rect on the drawing layer1
    def DrawRect(self, *args):
	#Part 1: get our arguments
	a = args[0]
	y = a['y']
	x = a['x']
	width = a['width']
	height = a['height']

	#part two: getting the references 
        client = gdata.docs.client.DocsClient(source=oauth2.Config.APP_PLACE)
        client.ssl = True
         # This is the token instantiated in the oauth section.
        client = (oauth2.session.token).authorize(client)
        folders_feed = client.get_all_resources(uri='/feeds/default/private/full/-/folder')
         
        #Grab layer1
        for entry in folders_feed :
            if entry.title.text == 'Map' :
                map = entry
                break
        
        mapfeed = client.get_all_resources(uri=map.content.src)
        for entry in mapfeed:
            if entry.title.text == "Layer1" :
                layer1entry = entry
            if entry.title.text == "Layer2" :
                layer2entry = entry
                link = entry.get_resumable_edit_media_link()
                
        #Optional: download layer1 as an SVG
        content = client.download_resource_to_memory(layer1entry)
        oldcontent = content
        #Replace it's content with our content
        
        #layer = layer1entry.content.src
        layer = '<svg xmlns:ns0="http://www.w3.org/2005/Atom" width="800" height="600"><g id="box_0"><rect x="' + str(x) + '" y="' + str(y) + '" width="' + str(width) + '" height="' + str(height) + '" fill="blue" stroke="blue" stroke-width="4"></rect></g></svg>'
        length = len(layer)
	#SVG("rect", x=10, y=10, width=60, height=60, id='star')
        #Stated that strings lack the attribue "_become_child" 
        #g.save("tmp.svg")
        #Reupload
        #layer2entry.content.src = layer1entry.content.src
        #client.update(layer2entry)
        #return (layer1entry.get_elements())[24].to_string() + (layer1entry.get_elements())[25].to_string()
        #response = client.put(link, layer1entry.to_string())
        
        href = "https://docs.google.com/feeds" + (link.href)[51:] #/feeds/upload/create-session/default/private/full/"
        myHeaders = {"GData-Version" : 3, "Content-Length" : length,
                     "Content-Type" : "image/svg+xml", "Authorization" : oauth2.session.token.access_token}
                   #"X-Upload-Content-Length" : 1000, "X-Upload-Content-Type" : "application/atom+xml" }
        
        payload2 = '<?xml version="1.0" encoding="UTF-8"?>' + '<entry xmlns="http://www.w3.org/2005/Atom" xmlns:docs="http://schemas.google.com/docs/2007">' + '<title>Legal Contract</title>' + '</entry>'
        #'<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">' + '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">  <circle cx="100" cy="50" r="40" stroke="black"  stroke-width="2" fill="red" /></svg>'
        try :
            result = urlfetch.fetch(url = "https://docs.google.com/feeds/upload/create-session/default/private/full",
                                    payload = payload2, #'<?xml version="1.0" encoding="utf-8"?><atom:entry xmlns:atom="http://www.w3.org/2005/Atom" xmlns:scope ="http://schemas.google.com/acl/2007:scope" xmlns:apps="http://schemas.google.com/apps/2006"></atom:entry>',
                                #payload = layer,
                                    method = urlfetch.POST,
                                    headers = myHeaders)
        except urllib2.URLError, e:
            return e
        return result.content#return link.href#result.status_code #+ " + " + href #<google.appengine.api.urlfetch._URLFetchResult object at 0xaf38d507abe08bf8>
        #conn = httplib.HTTPConnection(link.href)
        #conn.connect()
        #headers = {"Host" : "docs.google.com", "GData-Version" : 3, "Authorization" : oauth2.session.token,
        #           "If-Match" : "*", "Content-Length" : 0, 
        #           "X-Upload-Content-Length" : 1000, "X-Upload-Content-Type" : "img/svg" }
        #req = conn.request("PUT", layer, "", headers)
        #response = conn.getresponse()
        
        #req = urllib2.Request(layer2entry.content.src)
        #opennedim = urllib2.urlopen(req)
        
        #file_name = files.blobstore.create(mime_type='application/octet-stream')
        
        #with files.open(file_name, 'a') as f:
         #   f.write(opennedim)
        
        #files.finalize(file_name)
        
        #blob_key = files.blobstore.get_blob_key(file_name)
        
        #Blob has been uploaded. Now using the resumable uploader
        
        #blob_info = blobstore.BlobInfo.get(blob_key)
        #image = blob_info.open()
        #file_size = blob_info.size
        
        
        #uploader = gdata.client.ResumableUploader(client, opennedim, "img/svg", file_size,
         #                                         chunk_size = CHUNK_SIZE)
        #new_entry = uploader.UploadFile('/feeds/upload/create-session/default/private/full', 
         #                               entry = layer2entry)
        #updatedlayer = client.Update(layer2entry, media_source = ms)
        #return "Got Through!"

        #return req


from __future__ import with_statement
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app 
from google.appengine.ext import db
from google.appengine.api import files
from google.appengine.api import urlfetch

import gdata.data
import gdata.docs.client
import gdata.docs.data
from gdata.docs.data import Resource

import oauth2
  
class MapHandler(webapp.RequestHandler):  
         
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
        layer1entry = documents_feed[0]
        
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
            elif entry.title.text == "Layer2" :
                l2b = False
                layer2entry = entry
            #elif entry.title.text == 'PC Screen' : #testing purposes, never got this working
        
        if mapb :
            #self.response.out.write("In mapb!") always triggers
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
            
        
        self.writeJavascript('incoming', layer1entry.content.src) 
        self.response.out.write('<body>\n')
        self.writeLeft()
        
        self.response.out.write("<div id = 'center' style = 'position:absolute;top:0px;left:15%;width:70%'>\n")
        self.response.out.write(' Main Drawing Area!\n')
        self.response.out.write(" <div style = 'background-color:grey'>\n")
        self.response.out.write(" <img id = 'incoming' alt = '" + layer1entry.content.src + "' src = '" + layer1entry.content.src + "'> \n")#+ "' onclick='content(" + '"incoming"' + ")'>\n" )
        
        #uploader = gdata.client.ResumableUploader(client, f, 'image/png', file_size)
        
        #new_entry = uploader.UploadFile('/feeds/upload/create-session/default/private/full', entry=layer1entry)

        
        self.response.out.write(" </div>")
        self.response.out.write(" <div style = 'position:relative;right:0%;top:-15px;background-color:black'>")
        self.response.out.write(" </div>\n")
        self.response.out.write("</div>\n\n")
        
        self.writeRight()
        
    def writeJavascript(self, id, image):
        self.response.out.write("<script lang='javascript'>\n")
        self.response.out.write("var interval = self.setInterval('content(" + '"incoming"' + ")', 1000);\n")
        self.response.out.write("function content(id) {\n")
        self.response.out.write("  document.getElementById(id).src = document.getElementById(id).alt;\n")#google processes this additional input +" + " + '"' + "?rand=" + '"' + " + Math.random();\n")
        self.response.out.write("}\n")
        self.response.out.write("</script>\n\n")
    
    def writeLeft(self):
        self.response.out.write("<div id = 'left' style = 'position:absolute;left:0px;top:0px;width:15%'>\n")
        self.response.out.write(' Left Buttons!<br>\n')
        self.response.out.write(" <button type='button'>Create Box</button>\n")
        self.response.out.write(" <button type='button'>Color</button>\n")
        self.response.out.write("</div>\n\n")
        
    def writeRight(self):
        self.response.out.write("<div id = 'right' style = 'position:absolute;right:0px;top:0px;width:15%'>\n")
        self.response.out.write(' Right Options!<br>\n')
        self.response.out.write(" <button type='button'>Edit Hidden Layer</button>\n")
        self.response.out.write(" <button type='button'>Show Selected</button>\n")
        self.response.out.write("</div>\n\n")
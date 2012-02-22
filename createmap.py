
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
import gdata.service
from svgfig.interactive import *
import sys

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
        documents_feed = client.get_all_resources(uri='/feeds/default/private/full/-/folder')
        download_doc_feed = client.get_resources()

        mapb = True
        for entry in documents_feed :
            if entry.title.text == 'Map' :
                mapb = False
                map = entry
                break
        
        if mapb :
            #self.response.out.write("In mapb!") always triggers
            col = Resource('folder', 'Map')
            map = client.create_resource(col)
        
        mapfeed = client.get_all_resources(uri=map.content.src)
        l1b = True
        l2b = True
        for entry in mapfeed:
            if entry.title.text == "Layer1" :
                l1b = False
                layer1entry = entry
                link = entry.get_resumable_edit_media_link()
            elif entry.title.text == "Layer2" :
                l2b = False
                layer2entry = entry
            #elif entry.title.text == 'PC Screen' : #testing purposes, never got this working
        
        
        if l1b :
            self.response.out.write("In l1b!")
            layer1 = Resource(type='drawing', title='Layer1')
            layer1entry = client.create_resource(layer1, collection=map)
        if l2b :
            self.response.out.write("In l2b!")
            layer2 = Resource(type='drawing', title='Layer2')
            layer2entry = client.create_resource(layer2, collection=map)
            
        #self.response.out.write(layer1entry.to_string())
        #uploader = gdata.client.ResumableUploader(client, layer1entry.content, 'image/png', length, desired_class=gdata.docs.data.DocsEntry)
        #layer1entry = uploader('/feeds/upload/create-session/default/private/full', layer1entry)
        
        #ms = gdata.data.MediaSource()
        #ms.set_file_handle(layer1entry.filename, "image/png")
        
        #response_handle = self.request('GET', layer1entry.content.src)
        #layer1MediaSrc = (gdata.MediaSource(response_handle, response_handle.getheader(
        #    'Content-Type'), response_handle.getheader('Content-Length')))
        #layer2entry= client.Update(layer2entry, media_source=layer1MediaSrc)
        #self.writeJavascript('incoming', layer1entry.content.src) 
        self.writeJavascript()
        self.response.out.write('<body>\n')
        self.writeLeft()
        
        self.response.out.write("<div id = 'center' style = 'position:absolute;top:0px;left:10%;width:80%'>\n")
        self.response.out.write(" <div style = 'position:absolute;top:0px;max-width:80%'>\n")
        self.response.out.write(" <img id = 'incoming2' alt = '" + layer2entry.content.src + "' src = '" + layer2entry.content.src + "'> \n")#+ "' onclick='content(" + '"incoming"' + ")'>\n" )
        #self.response.out.write(layer2entry.content.to_string());
        #uploader = gdata.client.ResumableUploader(client, layer2entry.filename, 'image/png', layer2entry.content)
        
        #new_entry = uploader.UploadFile('/feeds/upload/create-session/default/private/full', entry=layer1entry)

        
        self.response.out.write(" </div>")
        self.response.out.write(" <div style = 'position:absolute;top:0px;max-width:80%'>\n")
        self.response.out.write(" <img id = 'incoming' alt = '" + layer1entry.content.src + "' src = '" + layer1entry.content.src )
        self.response.out.write( "'  > \n")#self.response.out.write( layer1MediaContent.file_size )
        self.response.out.write(" </div>\n")
        self.response.out.write(" <div id = 'drawSpace'>\n")
        self.response.out.write(" <img id = 'here' alt = '' src = '' width = incoming.width height = incoming.height>\n")
        #s = SVG("rect", x=10, y=10, width=60, height=60, id='star')
        #self.response.out.write(s.xml())
        self.response.out.write(" </div>\n")
        
        self.response.out.write("</div>\n\n")
        
        self.writeRight()
        
        
    def writeJavascript(self):
        self.response.out.write("<head>")
        self.response.out.write(" <script type='text/javascript' src = 'static/js/basic.js'></script>\n" )
        self.response.out.write(" <script type='text/javascript' src='static/js/jquery.js'></script>\n")
        self.response.out.write(" <script type='text/javascript'>\n")
        self.response.out.write('  $(document).ready(function(){\n  $(document).mousemove(function(e){ \n')
        self.response.out.write('    var position = $("div#center").position();\n')
        self.response.out.write('    var x = e.pageX - position.left;\n')
        self.response.out.write('    var y = e.pageY - position.top;\n')
        #self.response.out.write('    $("span").text("X: " + x + ", Y: " + y);\n')
        #self.response.out.write('    $("span").text("X: " + e.pageX + ", Y: " + e.pageY);\n')
        self.response.out.write('  });\n')
        self.response.out.write('  });\n') 
        
        self.response.out.write('  $(function(){\n   $("img").click(function(e) {\n')
        self.response.out.write('    var position = $("div#center").position();\n')
        self.response.out.write('    var x = e.pageX - position.left;\n')
        self.response.out.write('    var y = e.pageY - position.top;\n')
        self.response.out.write('   alert( "X: " + x + ", Y: " + y );')
        #self.response.out.write('   $("span").text("X: " + x + ", Y: " + y);\n')
        self.response.out.write('  });\n')
        self.response.out.write('  });\n') 
        self.response.out.write(" </script>\n")
        self.response.out.write("</head>")
        #self.response.out.write("var intervali1 = self.setInterval('interaction(" + '"drawSpace"' + ")', 1000);\n")
        #self.response.out.write("function interaction(id, type) {\n" 
        #                      + "  document.getElementById(id).innerHTML = " + s.xml + ";\n"
        #                      + "  " 
        #                      + "}\n")
        #self.response.out.write("</script>\n\n")
    
    def writeLeft(self):
        self.response.out.write("<div id = 'left' style = 'position:absolute;left:0px;top:0px;width:10%'>\n")
        self.response.out.write(' Left Buttons!<br>\n')
        self.response.out.write(" <button type='button'>Create Box</button>\n")
        self.response.out.write(" <button type='button'>Color</button>\n")
        self.response.out.write("   <button>Change Content</button>\n")
        self.response.out.write("   <span id='theplace'>\n")
        self.response.out.write("   </span>\n")
        self.response.out.write("</div>\n\n")
        
    def writeRight(self):
        self.response.out.write("<div id = 'right' style = 'position:absolute;right:0px;top:0px;width:10%'>\n")
        self.response.out.write(' Right Options!<br>\n')
        self.response.out.write(" <button type='button'>Edit Hidden Layer</button>\n")
        self.response.out.write(" <button type='button'>Show Selected</button>\n")
        self.response.out.write("</div>\n\n")
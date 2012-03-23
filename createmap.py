
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

from string import Template

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
            layer1 = Resource(type='drawing', title='Layer1')
            layer1entry = client.create_resource(layer1, collection=map)
        if l2b :
            layer2 = Resource(type='drawing', title='Layer2')
            layer2entry = client.create_resource(layer2, collection=map)
        
	#Putting this info together...
	#1. Import the template
	importedfile = templ() 
	temp = Template(importedfile)

	#2. Generate what we want to substute in
	layer1sub = " <img id = 'incoming' alt = '" + layer1entry.content.src + "' src = '" + layer1entry.content.src +"'>"

	#3. get the substituted version
	output = temp.substitute(layer1 = layer1sub)

	#4. print out the result
	self.response.out.write(output)

def templ() :
	thebody = """<head>
<script type='text/javascript' src='/static/js/jquery.js'></script>
<script type='text/javascript' src='/static/js/jquery/jquery.svg.js'></script>
<script type='text/javascript' src='/static/js/json2.js'></script>
<script type='text/javascript' src='/static/js/basic.js'></script>

<style type='text/css'>
@import '/static/js/jquery/jquery.svg.css';
</style>

</head>

<body>

<div id = 'top' style = 'position:absolute;top:0px;left:0px;height:100%;width:100%'>
   <div id = 'layer1' style = 'position:absolute;top:0px;width:100%'>
   $layer1
   </div>
   <div id = 'layer2' style = 'position:absolute;top:0px;width:100%'>
   </div>
   <div id = "drawSpace" style = 'position:absolute;top:0px;width:800px;height:600px;border-style:double;border-width:5px;margin-left:auto;margin-right:auto;'>
   </div>
</div>

<div id='bottom' style = 'position:absolute;top:610px;left:0px;width:100%'>
   <form id ='color'>
      <input type='radio' name='color' value='red'>Red</input>
      <input type='radio' name='color' value='yellow' CHECKED>Yellow</input>
      <input type='radio' name='color' value='blue'>Blue</input>
   </form>
   <button type='button'>Edit Hidden Layer</button>
   <button type='button'>Show Selected</button>
"""
	return thebody
    

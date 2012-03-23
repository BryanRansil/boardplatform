
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
            layer1 = Resource(type='drawing', title='Layer1')
            layer1entry = client.create_resource(layer1, collection=map)
        if l2b :
            layer2 = Resource(type='drawing', title='Layer2')
            layer2entry = client.create_resource(layer2, collection=map)
            
        self.writeJavascript()
        self.response.out.write('<body>\n')
        
        self.response.out.write("<div id = 'top' style = 'position:absolute;top:0px;left:0px;height:100%;width:100%'>\n")
        self.response.out.write(" <div style = 'position:absolute;top:0px;width:100%'>\n")
        #self.response.out.write(" <img id = " + '"incoming2"' + " alt = '" + layer2entry.content.src + "' src = '" + layer2entry.content.src +"'>")
        self.response.out.write(" </div>")
        self.response.out.write(" <div style = 'position:absolute;top:0px;width:100%'>\n")
        #self.response.out.write(" <img id = " + '"incoming"' + " alt = '" + layer1entry.content.src + "' src = '" + layer1entry.content.src +"'>")
        #self.response.out.write( layer1MediaContent.file_size )
        self.response.out.write(" </div>\n")
        self.response.out.write(" <div id = 'drawSpace' style = 'position:absolute;top:0px;width:800px;height:600px;border-style:double;border-width:5px;margin-left:auto;margin-right:auto;'>\n")
        self.response.out.write(" </div>\n")
        self.response.out.write("   <span id='theplace'>\n")
        self.response.out.write("       " + layer1entry.content.to_string() + "\n")
        self.response.out.write("   </span>\n")
        self.response.out.write(" </div>\n")
        
        self.response.out.write("</div>\n\n")
        
        self.writeBottom()
        
    def writeJavascript(self):
        self.response.out.write("<head>")
        #libraries
        self.response.out.write(" <script type='text/javascript' src = '/static/js/basic.js'></script>\n" )
        self.response.out.write(" <script type='text/javascript' src='/static/js/jquery.js'></script>\n")
        self.response.out.write(' <style type="text/css">@import "/static/js/jquery/jquery.svg.css";</style>\n')
        self.response.out.write(" <script type='text/javascript' src='http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js'></script>\n")
        self.response.out.write(' <script type="text/javascript" src="/static/js/jquery/jquery.svg.js"></script>\n')
        self.response.out.write('<script type="text/javascript" src="./static/js/json2.js"></script>\n')
               #start of actual script
        self.response.out.write(" <script type='text/javascript'>\n")
        
        #globals
        self.response.out.write(" var posx = -1; \n var posy = -1;\n")
        self.response.out.write(" var pos1x = -1; \n var pos1y = -1;\n")
        self.response.out.write(" var holding = null;\n var boxCount = 0;")
        self.response.out.write(" var leftWidth = 100; \n var topAdjust = 150;")
        
        #move
        self.response.out.write(' $(document).ready(function(){\n    $(document).mousemove(function(e){ \n')
        self.response.out.write('    posx = e.pageX - leftWidth;\n     posy = e.pageY - topAdjust;\n')
        self.response.out.write('    });\n')
        self.response.out.write('  });\n') 
        
        #mouse down
        self.response.out.write(' $(document).ready(\n')
        self.response.out.write('    function(){    $("#drawSpace").mousedown(function(e) {\n')
        self.response.out.write('      pos1x = e.pageX - leftWidth;\n')
        self.response.out.write('      pos1y = e.pageY-topAdjust;\n')
        self.response.out.write("      var size = document.getElementById('drawSpace').lastChild.childNodes.length;\n var string = '';\n")
        self.response.out.write('      for (var i = size - 1; i >= 0; i--) {\n')
        self.response.out.write("         el = document.getElementById('drawSpace').lastChild.childNodes[i]; \n")
        self.response.out.write("         box = document.getElementById('drawSpace').lastChild.childNodes[i].firstChild; \n")
        self.response.out.write('         if((box.x.animVal.value < posx) && (box.x.animVal.value + box.width.animVal.value > posx) \n&& (box.y.animVal.value < posy) && (box.y.animVal.value + box.height.animVal.value > posy)) { //assuming rectangles for now\n')
        self.response.out.write('            holding = el;\n')
        self.response.out.write('            i = -1;\n')
        self.response.out.write('         } else { holding = null; }\n')
        self.response.out.write('    }\n')
        self.response.out.write('   });\n')
        self.response.out.write('  })\n') 
        
        #mouse up
        self.response.out.write(" function release() {\n")
        self.response.out.write("      if (holding == null) drawShape(); else {\n")
        self.response.out.write("         svg = $('#drawSpace').svg('get');\n")
        self.response.out.write("         el = svg.getElementById(holding.id);\n")
        self.response.out.write("         x = el.firstChild.x.animVal.value;\n")
        self.response.out.write("         y = el.firstChild.y.animVal.value;\n")
        self.response.out.write("         width = el.firstChild.width.animVal.value;\n")
        self.response.out.write("         height = el.firstChild.height.animVal.value;\n")
        self.response.out.write("         svg.remove(el);\n")
        self.response.out.write("         var group = svg.group(null, holding.id);\n")
        self.response.out.write("         svg.rect(group, posx + (x - pos1x), posy + (y - pos1y), width, height, {fill: 'yellow', stroke: 'navy', strokeWidth: 2});\n")
        self.response.out.write("      }\n")
        self.response.out.write(" }\n")

        #Ajax Setup
        self.response.out.write("function InstallFunction(obj, name) {\n")
        self.response.out.write("        obj[name] = function() { Request(name, arguments); }\n")
        self.response.out.write("    }\n")
        self.response.out.write("\n")
        self.response.out.write("var server = {};\n")
        self.response.out.write("InstallFunction(server, 'DrawRect');\n")
        self.response.out.write("    \n")
        
        #Ajax Request
        self.response.out.write("function Request(function_name, opt_argv) {\n")
        self.response.out.write("    //if we don't have any arguments, make a list to work on\n")
        #self.response.out.write("            alert('In the request fxn!');\n");
        self.response.out.write("    if (!opt_argv)\n")
        self.response.out.write("        opt_argv = new Array();\n")
        self.response.out.write("    \n")
        self.response.out.write("    //parse the args for a success function\n")
        self.response.out.write("    var callback = null;\n")
        self.response.out.write("    var len = opt_argv.length;\n")
        self.response.out.write("    if (len > 0 && typeof opt_argv[len-1] == 'function') {\n")
        self.response.out.write("        callback = opt_argv[len-1];\n")
        self.response.out.write("        opt_argv.length--;\n")
        self.response.out.write("    }\n")
        self.response.out.write("    var async = (callback != null);\n")
        self.response.out.write("    \n")
        self.response.out.write("    //Get the action\n")
        self.response.out.write("    var query = 'action=' + encodeURIComponent(function_name);\n")
        self.response.out.write("    //Get the arguments\n")
        self.response.out.write("    for (var i = 0; i < opt_argv.length; i++) {\n")
        self.response.out.write("        var key = 'arg' + i;\n")
        self.response.out.write("        var val = JSON.stringify(opt_argv[i]);\n")
        self.response.out.write("        query += '&' + key + '=' + encodeURIComponent(val);\n")
        self.response.out.write("    }\n")
        self.response.out.write("    query += '&time=' + new Date().getTime(); //timestamp!\n")
        self.response.out.write("    \n")
        self.response.out.write("    //google says this may need to be made cross-browser-compatible\n")
        self.response.out.write("    var req = new XMLHttpRequest();\n")
        self.response.out.write("    \n")
        self.response.out.write("    //the part of my server I want this to go to\n")
        self.response.out.write("    req.open('POST', '/rect', async);\n")
        self.response.out.write("    \n")
        self.response.out.write("    //the request body!\n")
        self.response.out.write("    if (async) {\n")
        self.response.out.write("        req.onreadystatechange = function() {\n")
        self.response.out.write("        if(req.readyState == 4 && req.status == 200) {\n")
        self.response.out.write("            var response = null;\n")
	self.response.out.write("                try {\n")
        self.response.out.write("                    response = JSON.parse(req.responseText);\n")
        self.response.out.write("                } catch (e) {\n")
        self.response.out.write("                    response = req.responseText;\n")
        self.response.out.write("                    alert('Caught! ' + response);\n");
        self.response.out.write("                }\n")
        self.response.out.write("            callback(opt_argv);\n")
        self.response.out.write("            }\n")
        self.response.out.write("        }\n")
        self.response.out.write("    }\n")
        self.response.out.write("\n")
        self.response.out.write("  // Make the actual request\n")
        self.response.out.write("            alert('Making request!');\n") 
        self.response.out.write("  req.send(query);\n")
        self.response.out.write("}\n")

        #Drawing a rectangle once the server responds
        self.response.out.write(" function onDrawRectSuccess(response) {")
        self.response.out.write("            var svg = $('#drawSpace').svg('get');\n")
        self.response.out.write("            var group = svg.group(null, 'box_' + boxCount);\n")
        self.response.out.write("            var x = response[0];\n")
        self.response.out.write("            var y = response[1];\n")
        self.response.out.write("            var width = response[2];\n")
        self.response.out.write("            var height = response[3];\n")
        #self.response.out.write("            alert('Before the svg.rect command! x = ' + x + ' y = ' + y + ' width = ' + width + ' height = ' + height);\n")
        self.response.out.write("            svg.rect(group, x, y, width, height, {fill: 'yellow', stroke: 'navy', strokeWidth: 2});\n");
        #self.response.out.write("            alert('Past the svg.rect command!');\n")
        self.response.out.write("            boxCount++;\n }\n");
        
        #drawing a rect in the old way
        self.response.out.write(" function drawShape() {\n")
        self.response.out.write("    var shape = this.id;\n    ;\n var svg = $('#drawSpace').svg('get');\n")
        self.response.out.write("    var x = 0; \n    var y = 0; \n    var width = 0; \n    var height = 0;\n")
        self.response.out.write("    if (pos1x > posx) {\n      x = posx;\n      width = pos1x - posx;\n    " + 
                                "} else { \n      x = pos1x;\n      width = posx - pos1x;\n    }\n")
        self.response.out.write("    if (pos1y > posy) {\n      y = posy;\n      height = pos1y - posy;\n    " + 
                                "} else { \n      y = pos1y;\n      height = posy - pos1y;\n    }\n")#$('span').text(document.getElementById('drawSpace').firstChild.childNodes.length);") #
        self.response.out.write("    server.DrawRect(x,y,width,height,onDrawRectSuccess);\n");
        self.response.out.write(" }")
        
        #apparently need this to establish the SVG
        self.response.out.write(" function drawInitial(svg) {\n")
        self.response.out.write("    $('span').text();\n")
        self.response.out.write(" }\n")
        #Bindings
        self.response.out.write(' $(function() {')
        self.response.out.write("    $('#drawSpace').svg(drawInitial);\n")
        #self.response.out.write("    $('#drawSpace').svg('get').;\n")
        self.response.out.write('    $("#drawSpace").mouseup(release);\n') 
        self.response.out.write(" }\n );\n")
        
        self.response.out.write(" </script>\n") 

	self.response.out.write("</head>")

    def writeBottom(self):
        self.response.out.write("<div id = 'left' style = 'position:absolute;top:610px;left:0px;width:100%'>\n")
        self.response.out.write(' Bottom!<br>\n')
        self.response.out.write(" <form id ='color'> \n" +
                                "   <input type='radio' name='color' value='red'>Red</input> \n" +
                                "   <input type='radio' name='color' value='yellow' CHECKED>Yellow</input> \n" +
                                "   <input type='radio' name='color' value='blue'>Blue</input> \n" +
                                "</form>\n")
        self.response.out.write(" <button type='button'>Edit Hidden Layer</button>\n")
        self.response.out.write(" <button type='button'>Show Selected</button>\n")
        self.response.out.write("</div>\n\n")

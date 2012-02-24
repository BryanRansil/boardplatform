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
import createmap

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("<head>")
        self.response.out.write('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"></script>\n')
        self.response.out.write('<script type="text/javascript" src="/static/js/jquery/jquery.svg.js"></script>\n')
        self.response.out.write('<script type="text/javascript">\n')
        self.response.out.write(" var posx = -1; \n var posy = -1;\n")
        self.response.out.write(" var pos1x = -1; \n var pos1y = -1;\n")
        self.response.out.write(" var holding = null;\n var boxCount = 0;")
        
        #move
        self.response.out.write(' $(document).ready(function(){\n    $(document).mousemove(function(e){ \n')
        self.response.out.write('    posx = e.pageX;\n     posy = e.pageY;\n')
        self.response.out.write('    });\n')
        self.response.out.write('  });\n') 
        
        #mouse down
        self.response.out.write(' $(document).ready(\n')
        self.response.out.write('    function(){    $("#svgbasics").mousedown(function(e) {\n')
        self.response.out.write('      pos1x = e.pageX;\n')
        self.response.out.write('      pos1y = e.pageY;\n')
        self.response.out.write("      var size = document.getElementById('svgbasics').firstChild.childNodes.length; var string = '';\n")
        self.response.out.write('      for (var i = 0; i < size; i++) {\n')
        self.response.out.write('         el = document.getElementById("svgbasics").firstChild.childNodes[i]; \n')
        self.response.out.write('         box = document.getElementById("svgbasics").firstChild.childNodes[i].firstChild; \n')
        #self.response.out.write('         string = string + "(box.x.animVal.value < posx) = " + (box.x.animVal.value < posx) + ' +
        #                            '", box.x.animVal.value + box.width.animVal.value > posx: " + (box.x.animVal.value + box.width.animVal.value > posx) + ' + 
        #                            '", (box.y.animVal.value < posy): " + (box.y.animVal.value < posy) + "; (box.y.animVal.value + box.height.animVal.value > posy): " + (box.y.animVal.value + box.height.animVal.value > posy) + ", ely: " + box.y.animVal.value + "; y-pos: " + posy + ", y+height: " + (box.y.animVal.value+box.height.animVal.value) + ".          ";\n')
        self.response.out.write('         if((box.x.animVal.value < posx) && (box.x.animVal.value + box.width.animVal.value > posx) \n&& (box.y.animVal.value < posy) && (box.y.animVal.value + box.height.animVal.value > posy)) { //assuming rectangles for now\n')
        self.response.out.write('            holding = el;\n')
        self.response.out.write('            i = size;\n')
        
        self.response.out.write('         } else { holding = null; }\n')
        self.response.out.write('      }\n $("span").text(string);\n')
        self.response.out.write('    });\n')
        self.response.out.write('  });\n') 
        
        #mouse up
        self.response.out.write(" function release() {\n")
        self.response.out.write("      if (holding == null) drawShape(); else {\n")
        #self.response.out.write('            alert(" activate!");\n')
        self.response.out.write("         svg = $('#svgbasics').svg('get');\n")
        self.response.out.write("         el = svg.getElementById(holding.id);\n")
        self.response.out.write("         width = el.firstChild.width.animVal.value;\n")
        self.response.out.write("         height = el.firstChild.height.animVal.value;\n")
        self.response.out.write("         svg.remove(el);\n")
        self.response.out.write("         var group = svg.group(null, holding.id);\n")
        self.response.out.write("         svg.rect(group, posx, posy, width, height, {fill: 'yellow', stroke: 'navy', strokeWidth: 2});\n")
        self.response.out.write("      }\n")
        self.response.out.write(" }\n")
        

        self.response.out.write(" function drawShape() {\n    var shape = this.id;\n    var svg = $('#svgbasics').svg('get');\n")
        self.response.out.write("    var x = 0; \n    var y = 0; \n    var width = 0; \n    var height = 0;\n")
        self.response.out.write("    if (pos1x > posx) {\n      x = posx;\n      width = pos1x - posx;\n    " + 
                                "} else { \n      x = pos1x;\n      width = posx - pos1x;\n    }\n")
        self.response.out.write("    if (pos1y > posy) {\n      y = posy;\n      height = pos1y - posy;\n    " + 
                                "} else { \n      y = pos1y;\n      height = posy - pos1y;\n    }\n")#$('span').text(document.getElementById('svgbasics').firstChild.childNodes.length);") #
        self.response.out.write("    var group = svg.group(null, 'box_' + boxCount);\n")
        self.response.out.write("    svg.rect(group, x, y, width, height, {fill: 'yellow', stroke: 'navy', strokeWidth: 2});\n")
        self.response.out.write("    boxCount++;\n")
        self.response.out.write(" }")
        
        self.response.out.write(' $(function() {')
        self.response.out.write("    $('#svgbasics').svg({onLoad: drawInitial});\n")
        self.response.out.write('    $("#svgbasics").mouseup(release);\n') 
        self.response.out.write(" }\n );\n")
        
        self.response.out.write(" function drawInitial(svg) {\n")
        self.response.out.write("    $('span').text(document.getElementById('svgbasics').childNodes.length);\n")
        self.response.out.write(" }\n")
        self.response.out.write(" </script>\n")
        
        self.response.out.write("</head>")
        
        # Set the cross origin resource sharing header to allow AJAX
        #self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.out.write("<body>")
        # Create a client class which will make HTTP requests with Google Docs server. 
        self.response.out.write('Welcome to the Board Game Platform\n')
        self.response.out.write('<button id="activate">Reveal!</button>\n')
        self.response.out.write('<span></span>\n')
        self.response.out.write('<div id="svgbasics"></div>')
        self.response.out.write(""" <form action='oauth2callback' method='post' name ='oauth2'>
            <input type = "hidden" name = "type" value="login" />
            <input type="submit" value="Enter!"/></form> \n""")
        self.response.out.write('<div id="svgbasics"></div>')
        self.response.out.write("</body>")

		
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/oauth2callback', oauth2.OAuthHandler),
                                          ('/catchtoken', oauth2.CatchTokenHandler),
                                          #('/newrect', rect.ShapeHandler),
                                          ('/create', createmap.MapHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

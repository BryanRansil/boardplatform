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
import rect

def templ ():
        templ = """<head>
        <script type="text/javascript" src="/static/js/jquery.js"></script>
        <script type="text/javascript" src="/static/js/jquery/jquery.svg.js"></script>
        <script type="text/javascript">
         var posx = -1;
	 var posy = -1;
         var pos1x = -1;
	 var pos1y = -1;
         var holding = null; 
	 var boxCount = 0;
         var topAdjustment = 55;
	 var leftAdjustment = 5;
       
	//move 
         $(document).ready(function(){
            $(document).mousemove(function(e){ 
            posx = e.pageX - leftAdjustment;
            posy = e.pageY-topAdjustment;
            });
          });
        
	//mouse down
         $(document).ready(
            function(){    $("#svgbasics").mousedown(function(e) {
              pos1x = e.pageX - leftAdjustment;
              pos1y = e.pageY-topAdjustment;
              var size = document.getElementById('svgbasics').firstChild.childNodes.length; var string = '';
              for (var i = size - 1; i >= 0; i--) {
                 el = document.getElementById("svgbasics").firstChild.childNodes[i]; 
                 box = document.getElementById("svgbasics").firstChild.childNodes[i].firstChild;
                 if((box.x.animVal.value < posx) && (box.x.animVal.value + box.width.animVal.value > posx) \n&& (box.y.animVal.value < posy) && (box.y.animVal.value + box.height.animVal.value > posy)) { //assuming rectangles for now
                    holding = el;
                    i = -1;
        
                 } else { holding = null; }
            }});}); 
        
        //mouse up
         function release() {
              if (holding == null) drawShape(); else {
        //            alert(" activate!");
                 svg = $('#svgbasics').svg('get');
                 el = svg.getElementById(holding.id);
                 width = el.firstChild.width.animVal.value;
                 height = el.firstChild.height.animVal.value;
                 svg.remove(el);
                 var group = svg.group(null, holding.id);
                 svg.rect(group, posx, posy, width, height, {fill: 'yellow', stroke: 'navy', strokeWidth: 2});
              }
         }

         function drawShape() {
            var shape = this.id;
            var svg = $('#svgbasics').svg('get');
            var x = 0;
            var y = 0; 
            var width = 0;
	    var height = 0;
            if (pos1x > posx) {
	      	x = posx;
		width = pos1x - posx; 
            } else {
	        x = pos1x;
                width = posx - pos1x;
            }
            if (pos1y > posy) {
                y = posy;
                height = pos1y - posy;
            } else { 
	        y = pos1y;\n
	    	height = posy - pos1y;
	    }
            var group = svg.group(null, 'box_' + boxCount);
            svg.rect(group, x, y, width, height, {fill: 'blue', stroke: 'blue', strokeWidth: 4});
            boxCount++;
         }
        
         $(function() {
            $('#svgbasics').svg({onLoad: drawInitial});
            $("#svgbasics").mouseup(release);
         }
	 );
        
         function drawInitial(svg) {
           $('span').text(document.getElementById('svgbasics').childNodes.length);
         }
         </script>
        
        </head>
        
        <body>
        Welcome to the Board Game Platform
        <span></span>
        <form action='oauth2callback' method='post' name ='oauth2'>
            <input type = "hidden" name = "type" value="login" />
            <input type="submit" value="Enter!"/></form>
        <div id="svgbasics" style="border-style:double;height:400px;border-width:5px"></div>
        </body>"""
        return templ

class MainHandler(webapp.RequestHandler):
    def get(self):
	imported = templ()
	self.response.out.write(imported)
		
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/oauth2callback', oauth2.OAuthHandler),
                                          ('/catchtoken', oauth2.CatchTokenHandler),
                                          ('/rect', rect.ShapeHandler),
                                          ('/create', createmap.MapHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

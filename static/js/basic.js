//if there are javascript problems, the site that I originally got this from said this script tag should be ...scr" + "ipt>"... but this stopped html from being loaded (therefore placing it at the end of the document allowed the HTML to be loaded)
//var interval = self.setInterval('content("incoming', 1000);
//var interval2 = self.setInterval('content("incoming2', 1000);

 //globals
 var posx = -1; 
 var posy = -1;
 var pos1x = -1; 
 var pos1y = -1;
 var holding = null;
 var boxCount = 0;
 var leftWidth = 0; 
 var topAdjust = 0;
function content(id) {
  document.getElementById(id).src = document.getElementById(id).alt;
}

function circle() {
    $("#drawSpace").append("<rect id=star2 x=" + 20 + " y=" + 10 + " width=" + 60 + " height=" + 60 + " stroke=black fill=none />");
}

function moveRect(posx, posy) {
    svg = $('#drawSpace').svg('get');
    el = svg.getElementById(holding.id);
    x = el.firstChild.x.animVal.value;
    y = el.firstChild.y.animVal.value;
    width = el.firstChild.width.animVal.value;
    height = el.firstChild.height.animVal.value;
    svg.remove(el);
    var group = svg.group(null, holding.id);
    svg.rect(group, posx-(width/2), posy, width, height, {fill: 'yellow', stroke: 'navy', strokeWidth: 2});
    
}

//move
 $(document).ready(function(){
    $(document).mousemove(function(e){ 
    posx = e.pageX - leftWidth;
    posy = e.pageY - topAdjust;
    if (holding != null) {
	//we want to change the position of our element	
	moveRect(posx, posy);
    } 
    });
  }); 
        
//mouse down
$(document).ready(
    function(){    
      $("#drawSpace").mousedown(
         function(e) {
            pos1x = e.pageX - leftWidth;
            pos1y = e.pageY-topAdjust;
            var size = document.getElementById('drawSpace').lastChild.childNodes.length;
            var string = '';
            for (var i = size - 1; i >= 0; i--) {
                el = document.getElementById('drawSpace').lastChild.childNodes[i]; 
         	box = document.getElementById('drawSpace').lastChild.childNodes[i].firstChild; 
         	if((box.x.animVal.value < posx) && (box.x.animVal.value + box.width.animVal.value > posx) 
              		&& (box.y.animVal.value < posy) && (box.y.animVal.value + box.height.animVal.value > posy)) { //assuming rectangles for now\n')
            		holding = el;
            		i = -1;
         	} else { holding = null; }
    	   }
   	});
  }
); 
        
      //  #mouse up
 function release() {
      if (holding == null) drawShape(); 
      else {
	holding = null;
      }
 }

      //  #Ajax Setup
function InstallFunction(obj, name) {
        obj[name] = function() { Request(name, arguments); }
    }

var server = {};
InstallFunction(server, 'DrawRect');
        
       // #Ajax Request
function Request(function_name, opt_argv) {
    //if we don't have any arguments, make a list to work on\
    if (!opt_argv)
        opt_argv = new Array();

    //parse the args for a success function
    var callback = null;
    var len = opt_argv.length;
    if (len > 0 && typeof opt_argv[len-1] == 'function') {
        callback = opt_argv[len-1];
        opt_argv.length--;
    }
    var async = (callback != null);
    
    //Get the action
    var JSONObject = { "rect" : [
	{ "x" : opt_argv[0],
	  "y" : opt_argv[1],
	  "width" : opt_argv[2],
	  "height" : opt_argv[3]
	}
      ] 
    };
    /*var query = 'action=' + encodeURIComponent(function_name);
    //Get the arguments
    for (var i = 0; i < opt_argv.length; i++) {
        var key = 'arg' + i;
        var val = JSON.stringify(opt_argv[i]);
        query += '&' + key + '=' + encodeURIComponent(val);
    }
    query += '&time=' + new Date().getTime(); //timestamp!
   */ 
/*
	//V1: sends an object form and gets no response from the server
	= {
			"x" : opt_argv[0],
			"y" : opt_argv[1],
			"width" : opt_argv[2],
			"height" : opt_argv[3],
			"time" : new Date().getTime()
		};
    //V2: not recognized
    if (function_name == "DrawRect") {
        query += '"x":"' + opt_argv[0] + '",';
        query += '"y":"' + opt_argv[0] + '",';
        query += '"width":"' + opt_argv[0] + '",';
	query += '"height":"' + opt_argv[3] + '",';
	query += '"time":"' + new Date().getTime() + '"';
    }

*/
    //google says this may need to be made cross-browser-compatible
    var req = new XMLHttpRequest();
    
    //the part of my server I want this to go to
    req.open('POST', 'http://boardplatform.appspot.com/rect', async);
    req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); 	
	alert(JSONObject);    
    
    //the request body!
    if (async) {
        req.onreadystatechange = function() {
        if(req.readyState == 4 && req.status == 200) {
            var response = null;
                try {
                    response = JSON.parse(req.responseText);
                } catch (e) {
                    response = req.responseText;
                }
                //alert('Caught! ' + req.responseText);
            callback(opt_argv);
            }
        }
    }

  // Make the actual request\
  req.send(JSONObject);
}

 //Drawing a rectangle once the server responds
 function onDrawRectSuccess(response) {
   var svg = $('#drawSpace').svg('get');
   var group = svg.group(null, 'box_' + boxCount);
   var x = response[0];
   var y = response[1];
   var width = response[2];
   var height = response[3];
   svg.rect(group, x, y, width, height, {fill: 'yellow', stroke: 'navy', strokeWidth: 2});
   boxCount++;
 }
        
        //drawing a rect in the old way
 function drawShape() {
    var shape = this.id;
    var svg = $('#drawSpace').svg('get');
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
       y = pos1y; 
       height = posy - pos1y;
    }
    server.DrawRect(x,y,width,height,onDrawRectSuccess);
 }
        
 //apparently need this to establish the SVG
 function drawInitial(svg) {
    hello = "Hi!";
 }
 //Bindings
 $(function() {
    $('#drawSpace').svg(drawInitial);
    //don't know what this is supposed to do: $('#drawSpace').svg('get');
    $("#drawSpace").mouseup(release); 
   }
 );
        


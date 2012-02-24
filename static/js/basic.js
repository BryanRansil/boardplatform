//if there are javascript problems, the site that I originally got this from said this script tag should be ...scr" + "ipt>"... but this stopped html from being loaded (therefore placing it at the end of the document allowed the HTML to be loaded)
var interval = self.setInterval('content("incoming")', 1000);
var interval2 = self.setInterval('content("incoming2")', 1000);
function content(id) {
  document.getElementById(id).src = document.getElementById(id).alt;
}

/*function onClick() {
  document.getElementById("theplace").innerHTML = "HI!";
};

function newShape(x, y, width, height) {
  var xmlHttp = new XMLHttpRequest();
  alert("Setting response handler");
  var responseHandler = function() {
  if (xmlHttp.readyState == 4)
    alert("Success");
  }
  xmlHttp.onreadystatechange = responseHandler;
  alert("get command");
  xmlHttp.open("GET","/newrect",true);
  xmlHttp.send(null);
}*/

function circle() {
    $("#svgfig").append('<rect id="star2" x="20" y="10" width="60" height="60" stroke="black" fill="none" />\n');
}

/*function thePaper(){
  return paper;
}*/

/*$(document).ready(function(){
  $("img").click(function(e){
      var position = $("div#center").position();
      var x = e.pageX - position.left;
      var y = e.pageY - position.top;
      alert("Hello!");
      //$("span").append("X: " + x + ", Y: " + y);
      //$("svgfig").append('<rect id="star" x="20" y="10" width="60" height="60" stroke="black" fill="none" />\n');
      //$("svgfig").append('<rect id="star" x="20" y="10" width="60" height="60" stroke="black" fill="none" />');
    });
});*/
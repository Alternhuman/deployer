var connectedSockets = []

var ws;
function createSocket(url, callback){
    //console.log(url);
    if(connectedSockets.indexOf(url) > -1){
        //console.log("Returning")
        callback();
        return;
    }
    //console.log("Creating socket");
    connectedSockets.push(url);

    var loc = window.location;
    var uri = loc.protocol == "https:" ? "wss:" : "ws:";
    uri += "//" + "localhost:1370" + "/ws/";

    uri = "wss://"+url+":1370/ws/"
    ws = new WebSocket("wss://localhost:1370/ws/");

    ws.onmessage = function(evt) {
        var msg = JSON.parse(evt.data);
        if($("#"+msg.identifier).length < 1){
            createOutput(msg.ip, msg.identifier, msg.command);
        }
        addOutput(msg.ip, msg.identifier, msg.message, "stdout", msg.stop);
    };
    //console.log($.cookie("user"));
    ws.onopen=function(evt){
        ws.send($.cookie("user"));
        //console.log("Calling callback");
        callback();
    };
}

var tabs = [];

function createTabs(host){
    if(!(host in tabs)){
        var identifier = "tab"+(Object.keys(tabs).length);
        $("ul.nav-tabs").append("<li><a href='#"+identifier+"'>"+host+"</a></li>");

        $("#window").append("<div id='"+identifier+"' style='display:none'></div>");
        tabs[host] = $(identifier);
        parseTabs();
    }
    
}


function createOutput(host, identifier, command){
    $tab = tabs[host];
    //console.log(tabs);
    $("#"+$tab.selector).append("<div id='"+identifier+"' class='col-xs-6'><div class='panel panel-primary'><div class='panel-heading'>"+command+"</div><div class='panel-body output'></div></div></div>");

}
//TODO: http://stackoverflow.com/a/12034334/2628463


function escapeHtml(string) {
    var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
  };
return String(string).replace(/[&<>"'\/]/g, function (s) {
  return entityMap[s];
});
}
function addOutput(host, identifier, message, stream, stop){
    $tab = tabs[host];
    if (stop == true){
        $("#"+$tab.selector).find("#"+identifier).find(".panel").removeClass("panel-primary").addClass("panel-default");
    }else{
        console.log("message"+message);
        $("#"+$tab.selector).find("#"+identifier).find(".panel-body").append("<p class='"+stream+"'>"+escapeHtml(message)+"</p>")
        //console.log("Output");
        $("#"+$tab.selector).find("#"+identifier);
    }
}

function parseTabs() {
    $("ul.nav-tabs").each(function() {

        var $active, $content, $links = $(this).find('a');

        // If the location.hash matches one of the links, use that as the active tab.
        // If no match is found, use the first link as the initial active tab.
        $active = $($links.filter('[href="' + location.hash + '"]')[0] || $links[0]);
        /*if($active == undefined){
            console.log("Returning");
            return;
        }*/
        //$active.addClass('active');
        if ($active[0] === undefined)
            return
       
        $content = $($active[0].hash);

        // Hide the remaining content
        $links.not($active).each(function() {
            $(this.hash).hide();
        });

        /*$links.each(function(){
            $(this.hash).hide();
        });*/

        $(this).unbind('click');
        // Bind the click event handler
        $(this).on('click', 'a', function(e) {
            //console.log("Clicked");
            $("ul.nav-tabs li.active").removeClass('active');
            $(this).closest('li').addClass('active');
            // Make the old tab inactive.
            $active.removeClass('active');
            $content.hide();

            // Update the variables with the new link and content
            $active = $(this);
            $content = $(this.hash);
            //console.log($content)
            // Make the tab active.
            $active.addClass('active');
            $content.show();

            // Prevent the anchor's default click action
            e.preventDefault();
        });
    });
};

$(document).ready(function(){
    parseTabs();
});
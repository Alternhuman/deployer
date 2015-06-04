var connectedSockets = []
var newConnections=0;

function newConnection(){
    newConnections++;
    $badge = $("span.badge.logger-badge");
    $badge.text(newConnections);
    if(!$badge.hasClass("active")){
        $badge.show();
    }
}

function resetConnectionsCounter(){
    newConnections=0;
    $("span.badge.logger-badge").hide();
}

$(document).ready(function(){
    $(".logger-link").on('click', function(){
        resetConnectionsCounter();
    });
});


function createSocket(url, callback){
    //The socket is only created once
    if(connectedSockets.indexOf(url) > -1){
        callback();
        return;
    }
    
    connectedSockets.push(url);

    var loc = window.location;
    var uri = loc.protocol == "https:" ? "wss:" : "ws:"; //HTTPS detection
    uri += "//" +url+":1370" + "/ws/logger/";
    var ws;
    
    ws = new WebSocket(uri);

    ws.onmessage = function(evt) {
        var msg = JSON.parse(evt.data);
        //If it is the first output received, the output frame is created
        console.log(msg)
        if(msg.shell == true){
            appendShellOutput(msg.message, msg.ip, msg.stream_name, msg.stop);
        }else{
            if($("#"+msg.identifier).length < 1){
                createOutput(msg.ip, msg.identifier, msg.command);
                newConnection();
            }
                
            addOutput(msg.ip, msg.identifier, msg.message, msg.stream_name, msg.stop);
        }
    };
    
    ws.onopen=function(evt){
        //The authentication is based on the HMAC message stored in the cookie
        ws.send(JSON.stringify({register:$.cookie("user")}));
        if(callback != undefined)
            callback();
    };

    ws.onerror= function(evt){
        //
    };

    return ws;
}

var tabs = [];

function createTabs(host){
    if(!(host in tabs)){
        var identifier = "tab"+(Object.keys(tabs).length);
        $("ul.nav-tabs").append("<li><a href='#"+identifier+"'>"+host+"</a></li>");

        $("#window").append("<div id='"+identifier+"' style='display:none'></div>");
        tabs[host] = $(identifier);
        parseTabs("ul.nav-tabs");
    }
}


function createOutput(host, identifier, command){
    $tab = tabs[host];
    
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
    if (stop == true)
        //If the stop flag is true, no more input is appended and the style of the panel is modified
        $("#"+$tab.selector).find("#"+identifier).find(".panel").removeClass("panel-primary").addClass("panel-default");
    else
        $("#"+$tab.selector).find("#"+identifier).find(".panel-body").append("<p class='"+stream+"'>"+escapeHtml(message)+"</p>");
    
}

function parseTabs(selector) {
    $(selector).each(function() {

        var $active, $content, $links = $(this).find('a');

        // If the location.hash matches one of the links, use that as the active tab.
        // If no match is found, use the first link as the initial active tab.
        $active = $($links.filter('[href="' + location.hash + '"]')[0] || $links[0]);
        
        //$active.addClass('active');
        if ($active[0] === undefined)
            return
       
        $content = $($active[0].hash);

        // Hide the remaining content
        $links.not($active).each(function() {
            $(this.hash).hide();
        });

        $(this).unbind('click');
        // Bind the click event handler
        $(this).on('click', 'a', function(e) {
            
            $(selector+" li.active").removeClass('active');
            $(this).closest('li').addClass('active');
            // Make the old tab inactive.
            $active.removeClass('active');
            $content.hide();

            // Update the variables with the new link and content
            $active = $(this);
            $content = $(this.hash);
            
            // Make the tab active.
            $active.addClass('active');
            $content.show();

            // Prevent the anchor's default click action
            e.preventDefault();
        });
    });
};

$(document).ready(function(){
    parseTabs("ul.nav-tabs");
});
var ws;
function createSocket(){
    var loc = window.location;
    var uri = loc.protocol == "https:" ? "wss:" : "ws:";
    uri += "//" + "localhost:1370" + "/ws/";
    ws = new WebSocket("wss://localhost:1370/ws/");

    ws.onmessage = function(evt) {
        console.log(evt.data) 
    };
    console.log($.cookie("user"));
    ws.onopen=function(evt){
        ws.send($.cookie("user"));
    }
}

$(document).ready(function() {
    $("ul.tabs").each(function() {
        var $active, $content, $links = $(this).find('a');

        // If the location.hash matches one of the links, use that as the active tab.
        // If no match is found, use the first link as the initial active tab.
        $active = $($links.filter('[href="' + location.hash + '"]')[0] || $links[0]);
        $active.addClass('active');

        $content = $($active[0].hash);

        // Hide the remaining content
        $links.not($active).each(function() {
            $(this.hash).hide();
        });

        // Bind the click event handler
        $(this).on('click', 'a', function(e) {
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
            //e.preventDefault();
        });
    });

	createSocket();
});
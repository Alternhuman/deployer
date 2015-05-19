'use strict'

function nodo(info){
    var cadena = "<div class='node not-chosen'>";
    cadena += "<p class='ip'>"+info+"</p>";
    cadena += "<input class='deploy' type='checkbox'></input>"
    cadena += "</div>";
    return cadena;
}



$(document).ready(function() {

    var loc = window.location;
    var uri = loc.protocol == "https:" ? "wss:" : "ws:";
    uri += "//" + loc.host + loc.pathname + "ws/nodes";
    var ws = new WebSocket(uri);

    ws.onmessage = function(evt) {
        var parsed_data = JSON.parse(evt.data)
        $("#listanodos").html("");
        if (parsed_data["Nodes"]) {
            $("#count").html(parsed_data["Nodes"].length);

            for (var node in parsed_data["Nodes"]) {
                $("#listanodos").append(nodo(parsed_data["Nodes"][node]));
            }
        } 
    };

    $("#listanodos").on('click', "input[type=checkbox]", function(){
        $(this).closest(".node").toggleClass("chosen").toggleClass("not-chosen");
    });
    
    $("#list").delegate('.delete-buton', 'click', function(){
        var index = $(this).parent().index();
        
        $(this).parent().fadeOut(400, function(){
            $(this).remove();
            files_to_upload.splice(index, 1);
        });
    });

    $('#list').delegate('input[name=polo]', 'click', function(){
        if($(this).is(':checked')){
            $(this).siblings('input[name=idpolo]').prop('disabled', false);
            $(this).siblings('.polo.alert-warning').show(400);
        }else{
            $(this).siblings('input[name=idpolo]').prop('disabled', true);
            $(this).siblings('.polo.alert-warning').hide(400);
        }
    });

    $('#list').delegate('input[name=tomcat]', 'click', function(){
        if($(this).is(':checked')){
            $(this).siblings('.warning.alert-warning').show(400);
            $(this).siblings('input[name=folder]').prop('disabled', true);
            $(this).siblings('input[name=folder]').prop('placeholder', 'Default Tomcat directory');
        }else{
            $(this).siblings('.warning.alert-warning').hide(400);
            $(this).siblings('input[name=folder]').prop('disabled', false);
            $(this).siblings('input[name=folder]').prop('placeholder', 'Deployment folder');
        }
    });
});

//http://hayageek.com/drag-and-drop-file-upload-jquery/

function sendFileToServer(formData, status) {

    var uploadURL = "/upload"; //Upload URL
    var extraData = {}; //Extra Data.
    var jqXHR = $.ajax({
        xhr: function() {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                xhrobj.upload.addEventListener('progress', function(event) {
                    var percent = 0;
                    var position = event.loaded || event.position;
                    var total = event.total;
                    if (event.lengthComputable) {
                        percent = Math.ceil(position / total * 100);
                    }

                    status.setProgress(percent);
                }, false);
            }
            return xhrobj;
        },
        url: uploadURL,
        type: "POST",
        contentType: false,
        processData: false,
        cache: false,
        data: formData,
        beforeSend:function(data){
            $(".alert.alert-success").hide();
        },
        success: function(data) {
            status.setProgress(100);
            $(".alert.alert-success").show();
            $(".alert.alert-success").text("File upload done");
        }
    });
}

function createStatusbar(obj){
    this.obj = $(obj);
    this.setProgress = function(progress){
        obj.attr("aria-valuenow", progress);
        obj.css("width",progress + "%");
        obj.html(progress + "%");
    }
}

function handleFileUpload(files, obj) {
    for (var i = 0; i < files.length; i++) {

        files[i].command = $(".upload-item").eq(i).find("input[name=command]").val();
        //files[i].folder = $(".upload-item").eq(i).find("input[name=folder]").val();
        files[i].polo = $(".upload-item").eq(i).find("input[name=polo]").is(':checked');
        if(files[i].polo){
            files[i].identifier = $(".upload-item").eq(i).find("input[name=idpolo").val();
        }
        
        if($(".upload-item").eq(i).find("input[name=tomcat]").is(':checked')){
            files[i].tomcat = true
            
        }else{
            files[i].tomcat = false      
            files[i].folder = $(".upload-item").eq(i).find("input[name=folder]").val();
        }

        
        files[i].overwrite = $(".upload-item").eq(i).find("input[name=overwrite]").is(':checked');
        
        
        var fd = new FormData();
        fd.append('file', files[i].file);
        fd.append('command', files[i].command);
        fd.append('folder', files[i].folder);
        if(files[i].tomcat === true)
            fd.append('tomcat', files[i].tomcat);
        fd.append('overwrite', files[i].overwrite);
        var cadena = "";
        var ips = $(".chosen").children(".ip")
        var j = i;

        if(ips.length > 0){
            ips.each(function(index){

                cadena += $(this).html() + ",";
                var ip = $(this).html();

                createSocket(ip, function(){

                    if(index >= ips.length - 1){

                        fd.append('nodes', cadena);
                        //console.log($(".progress-bar").eq(j), j);
                        var status = new createStatusbar($(".progress-bar").eq(j));
                        createTabs(ip);
                        sendFileToServer(fd, status);
                    }
                });
            });
            
        }
    }
}

var fileCount = 0;

function addToList(file){
    var filename = file.name;

    var other= '<li class="list-group-item upload-item"><button style="width:10%;" class="btn btn-danger delete-buton pull-right"><div class="glyphicon glyphicon-remove"></div></button>'
    var header_filename = '<p class="list-group-item-header">'+filename+'</p><div style="width:85%;" class="progress"><div role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="min-width: 2em;" class="progress-bar"></div></div>'
    var buttons = '<input type="text" name="command" placeholder="Command" maxlength="300"/><br/><input type="text" placeholder="Deployment folder" name="folder" maxlength="300"/><br/><label list-group-item-text="list-group-item-text" for="polo">Deploy in Polo?</label><input type="checkbox" value="polo" name="polo"/><input type="text" name="idpolo" placeholder="Identifier" maxlength="40" disabled="true"/><p class="alert alert-warning polo" style="display:none;">The service will be registered permanently. Use the language-specific binding to perform a temporary registry on execution time.</p>'
    var labels = '<br></br><label list-group-item-text="list-group-item-text" for="tomcat">Deploy in Tomcat?</label><input type="checkbox" value="tomcat" name="tomcat"/><p class="alert alert-warning warning" style="display:none;">The service will be installed on the Tomcat deployment directory after validating the format of the archive. If no instance of Tomcat is installed on the server, it won\'t be installed.</p>'
    labels += '<br></br><label list-group-item-text="list-group-item-text" for="overwrite">Overwrite file if it exists?</label><input type="checkbox" value="overwrite" name="overwrite" checked/></li>'
    var str = "<li class='list-group-item upload-item'>"
    str += '<p class="list-group-item-header">'+filename+'</p>';
    str += '<div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="min-width: 2em;">0%</div></div>'
    str += '<input class="pull-right" type="checkbox" value="polo" name="polo"></input><label class="pull-right list-group-item-text" for="polo">Deploy in polo?</label><input type="text" name="command" placeholder="Command" maxlength="300"></input>';
    str +='<br></br><input type="text" placeholder="Deployment folder" name="folder" maxlength="300"></input><button class="btn btn-danger delete-buton pull-right">Delete</button>'
    str += "</li>"

    str = other + header_filename + buttons + labels;
    $("#list").append(str);
}

var files_to_upload;

$(document).ready(function() {

    files_to_upload = new Array();

    var obj = $("#dragandrophandler");
    obj.on('dragenter', function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).css('border', '2px solid #0B85A1');
    });
    obj.on('dragover', function(e) {
        e.stopPropagation();
        e.preventDefault();
    });
    obj.on('drop', function(e) {

        $(this).css('border', '2px dotted #0B85A1');
        e.preventDefault();
        var files = e.originalEvent.dataTransfer.files;
        for (var i = 0; i < files.length; i++) {
            files_to_upload.push({file: files[i]});
            fileCount++;
            addToList(files[i]);
        }
    });

    $(document).on('dragenter', function(e) {
        e.stopPropagation();
        e.preventDefault();
    });
    $(document).on('dragover', function(e) {
        e.stopPropagation();
        e.preventDefault();
        obj.css('border', '2px dotted #0B85A1');
    });
    $(document).on('drop', function(e) {
        e.stopPropagation();
        e.preventDefault();
    });

    $("#uploadbutton").on('click', function(e){
        handleFileUpload(files_to_upload, obj);
    });
/*});


$(document).ready(function() {*/
    //from http://www.jacklmoore.com/notes/jquery-tabs/
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
});
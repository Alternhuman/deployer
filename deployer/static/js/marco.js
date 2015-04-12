'use strict'

function nodo(info){
    var cadena = "<div class='node not-chosen'>";
    cadena += "<p class='hostname'>Hostname</p>"
    cadena += "<p class='ip'>"+info+"</p>";
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

        if (parsed_data["Nodes"]) {
            $("#count").html(parsed_data["Nodes"].length);

            for (var node in parsed_data["Nodes"]) {
                $("#listanodos").append(nodo(parsed_data["Nodes"][node]));
            }
        } 
    };

    $("#listanodos").delegate('.node','click', function(){
        $(this).toggleClass("chosen").toggleClass("not-chosen");
    });
    
    $("#list").delegate('.delete-buton', 'click', function(){
        var index = $(this).parent().index();
        
        $(this).parent().fadeOut(400, function(){
            $(this).remove();
            files_to_upload.splice(index, 1);
        });
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
        success: function(data) {
            status.setProgress(100);
            $("#list").append("File upload Done<br>");
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
        files[i].folder = $(".upload-item").eq(i).find("input[name=folder]").val();
        
        var fd = new FormData();
        fd.append('file', files[i].file);
        fd.append('command', files[i].command);
        fd.append('folder', files[i].folder);
        
        var cadena = "";
        var ips = $(".chosen").children(".ip")
        
        if(ips.length > 0){
            ips.each(function(index){
                cadena += $(this).html() + ",";
            });
            fd.append('nodes', cadena);
            var status = new createStatusbar($(".progress-bar").eq(i));
            sendFileToServer(fd, status);
        }
    }
}

var fileCount = 0;

function addToList(file){
    var filename = file.name;
    var str = "<li class='list-group-item upload-item'>"
    str += '<p class="list-group-item-header">'+filename+'</p>';
    str += '<div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="min-width: 2em;">0%</div></div>'
    //$("#list").append("<li class='list-group-item'>"+filename+"<input class='pull-right' type='checkbox' value='stahp"+fileCount+"' name='stahp"+fileCount+"' id='stahp"+fileCount+"'></input><label class='pull-right list-group-item-text' for='stahp"+fileCount+"'>Stahp</label></li>");
    str += '<input class="pull-right" type="checkbox" value="polo" name="polo"></input><label class="pull-right list-group-item-text" for="polo">Deploy in polo?</label><input type="text" name="command" placeholder="Command" maxlength="300"></input>';
    str +='<br></br><input type="text" placeholder="Deployment folder" name="folder" maxlength="300"></input><button class="btn btn-danger delete-buton pull-right">Delete</button>'
    str += "</li>"
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
});

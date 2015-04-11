'use strict'

function nodo(info){
    var cadena = "<div class='node not-chosen'>";
    cadena += "<p class='hostname'>Hostname</p>"
    cadena += "<p>"+info+"</p>";
    cadena += "</div>";
    return cadena + cadena + cadena + cadena;
}

$(document).ready(function() {

    var loc = window.location;
    var uri = loc.protocol == "https:" ? "wss:" : "ws:";
    uri += "//" + loc.host + loc.pathname + "ws/nodes";
    var ws = new WebSocket(uri);

    ws.onmessage = function(evt) {

        var parsed_data = JSON.parse(evt.data)

        if (parsed_data["Nodes"]) {

            $("#count").html(parsed_data["Nodes"].length)

            for (var node in parsed_data["Nodes"]) {
                $("#listanodos").append(nodo(parsed_data["Nodes"][node]))
            }
        } 
    };

    $("#listanodos").delegate('.node','click', function(){
        $(this).toggleClass("chosen").toggleClass("not-chosen");
    });
});



//http://hayageek.com/drag-and-drop-file-upload-jquery/
function sendFileToServer2(formData, status) {
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
                    //Set progress
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

    status.setAbort(jqXHR);
}
function sendFileToServer(formData) {
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
                    //Set progress
                    //status.setProgress(percent);
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
            //status.setProgress(100);

            $("#list").append("File upload Done<br>");
        }
    });

    //status.setAbort(jqXHR);
}

/*var rowCount = 0;

function createStatusbar(obj) {
    rowCount++;
    var row = "odd";
    if (rowCount % 2 == 0) row = "even";
    this.statusbar = $("<div class='statusbar " + row + "'></div>");
    this.filename = $("<div class='filename'></div>").appendTo(this.statusbar);
    this.size = $("<div class='filesize'></div>").appendTo(this.statusbar);
    this.progressBar = $("<div class='progressBar'><div></div></div>").appendTo(this.statusbar);
    this.abort = $("<div class='abort'>Abort</div>").appendTo(this.statusbar);
    obj.after(this.statusbar);

    this.setFileNameSize = function(name, size) {
        var sizeStr = "";
        var sizeKB = size / 1024;
        if (parseInt(sizeKB) > 1024) {
            var sizeMB = sizeKB / 1024;
            sizeStr = sizeMB.toFixed(2) + " MB";
        } else {
            sizeStr = sizeKB.toFixed(2) + " KB";
        }

        this.filename.html(name);
        this.size.html(sizeStr);
    }
    this.setProgress = function(progress) {
        var progressBarWidth = progress * this.progressBar.width() / 100;
        this.progressBar.find('div').animate({
            width: progressBarWidth
        }, 10).html(progress + "% ");
        if (parseInt(progress) >= 100) {
            this.abort.hide();
        }
    }
    this.setAbort = function(jqxhr) {
        var sb = this.statusbar;
        this.abort.click(function() {
            jqxhr.abort();
            sb.hide();
        });
    }
}*/

function handleFileUpload(files, obj) {
    for (var i = 0; i < files.length; i++) {

        files[i].command = $(".upload-item").eq(i).find("input[name=command]").val();

        var fd = new FormData();
        fd.append('file', files[i].file);
        fd.append('command', files[i].command);

        //var status = new createStatusbar(obj); //Using this we can set progress.
        //status.setFileNameSize(files[i].name, files[i].size);
        sendFileToServer(fd);

    }
}

var fileCount = 0;

function addToList(file){
    var filename = file.name;
    var str = "<li class='list-group-item upload-item'>"
    str += '<p class="list-group-item-header">'+filename+'</p>';
    //$("#list").append("<li class='list-group-item'>"+filename+"<input class='pull-right' type='checkbox' value='stahp"+fileCount+"' name='stahp"+fileCount+"' id='stahp"+fileCount+"'></input><label class='pull-right list-group-item-text' for='stahp"+fileCount+"'>Stahp</label></li>");
    str += '<input class="pull-right" type="checkbox" value="polo" name="polo"></input><label class="pull-right list-group-item-text" for="polo">Deploy in polo?</label><input type="text" name="command" placeholder="Command" maxlength="300"></input>';
    str +='<br></br><input type="text" placeholder="Deployment folder" maxlength="300"></input><button class="pull-right">Delete</button>'
    str += "</li>"
    $("#list").append(str);
}

$(document).ready(function() {

    var files_to_upload = new Array();

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

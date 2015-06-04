function processCommand(input){
	var hosts = [];
	$(".doexecute").each(function(index, element){
		hosts[hosts.length] = $(element).text();
	});
	sendInput(input, hosts);
}


function sendInput(input, hosts){
	
}

var shellTabs = {};

function createShellTab(ip){
	
    var identifier = "tab"+(Object.keys(shellTabs).length);

    $("#shellwindow").append("<div id='"+identifier+"' class='col-xs-6'><div class='panel panel-primary'><div class='panel-heading'><span class='ipaddr doexecute'>"+ip+"</span><input class='pull-right executecheckbox' type='checkbox' name='execute' checked></input></div><div class='panel-body output'></div></div></div>");
    
    shellTabs[ip] = $("#"+identifier);

}

function createShell(ip){
	createShellTab(ip);
}

$(document).ready(function(){
	$("#command input").attr("placeholder", "$"+$("span.username").text()+">");

	$("#command input").on('keyup', function(e){
		
		if(e.which == 13){
			e.preventDefault();
			var command = $(this).val();
			$(this).val("");
			processCommand(command);
			
		}
	});

	$("#shellwindow").on('click', ".executecheckbox", function(){
		$panel = $(this).closest(".panel");
		$node = $(this).siblings(".ipaddr").first();
		console.log($(this).siblings())
		if($(this).is(":checked")){
			$panel.removeClass("panel-default").addClass("panel-primary");
			$node.addClass("doexecute");
		}else{
			$panel.removeClass("panel-primary").addClass("panel-default");
			$node.removeClass("doexecute");
		}
	});
});
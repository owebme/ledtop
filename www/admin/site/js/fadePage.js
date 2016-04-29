$(document).ready(function() {
	
	$("#content").css("display", "none");

    $("#content").fadeIn(800);
    
	$("a").click(function(event){
		event.preventDefault();
		linkLocation = this.href;
		
		if ($(this).attr("href") == "#"){}
		else if ($(this).attr("onclick")){}
		else if ($(this).attr("class") == "fancybox"){}
		else if ($(this).attr("class") == "zoom fancybox"){}		
		else {$("#content").fadeOut(500, redirectPage);}
		
	});
		
	function redirectPage() {
		window.location = linkLocation;
	}
	
});

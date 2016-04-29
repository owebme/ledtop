$(document).ready(function(){
	
	$("div.jSboxBanner").each(function(){
		var banner = $(this);
		var repeat = $(banner).attr("data-repeat");
		if (repeat != "off"){repeat = parseInt(repeat);}
		var img1_speed = parseInt($(banner).attr("data-img1-speed"));
		var img2_speed = parseInt($(banner).attr("data-img2-speed"));		
		if (repeat != "off"){
			showjSboxBanner(banner, repeat);
		}
	});
	
	var interval="";
	function showjSboxBanner(banner, repeat){
		var img1_speed = parseInt($(banner).attr("data-img1-speed"));
		var img2_speed = parseInt($(banner).attr("data-img2-speed"));
		var img1_cordX = parseInt($(banner).attr("data-img1-cordX"));
		var img2_cordX = parseInt($(banner).attr("data-img2-cordX"));		
		setTimeout(function(){
			$(banner).find(".jSboxBanner-text2").fadeIn(2000);
			$(banner).find(".jSboxBanner-text2_bg").fadeIn(2000);
		}, 1000);
		setTimeout(function(){
			$(banner).find(".jSboxBanner-text3").fadeIn(1000);
			$(banner).find(".jSboxBanner-text3_bg").fadeIn(1000);
		}, 300);
		$(banner).find(".jSboxBanner-img1").animate({"left": img1_cordX+"px"}, img1_speed, "easeInOutSine");
		var pause = parseInt(img1_speed-200);
		if (pause < 0) {pause = 0;}
		if (img2_speed > 0){
			setTimeout(function(){
				$(banner).find(".jSboxBanner-img2").animate({"left": img2_cordX+"px", opacity: "1"}, img2_speed, "easeOutQuart");
			}, pause);
		}
		else {
			$(banner).find(".jSboxBanner-img2").css({"left": img2_cordX+"px", opacity: "1"});
		}
		clearInterval(interval);
		setTimeout(function(){
			$(banner).find("blink").hide();
			interval = setInterval(function(){$(banner).find("blink").toggle();}, 500);
		}, parseInt(img1_speed/2));
		if (repeat > (img1_speed+img2_speed) && repeat > 0 && repeat != "off"){
			setTimeout(function(){
				var width = parseInt($(banner).width());
				var height = parseInt($(banner).height());
				$(banner).find("div.jSboxBanner-text2").fadeOut(400, "swing");
				$(banner).find("div.jSboxBanner-text3").fadeOut(400, "swing");
				$(banner).find("div.jSboxBanner-text2_bg").fadeOut(400, "swing");
				$(banner).find("div.jSboxBanner-text3_bg").fadeOut(400, "swing");
				if (width > height){$(banner).find("img.jSboxBanner-img1").css({"left": (width*0.54)+"px"});}
				else {$(banner).find("img.jSboxBanner-img1").css({"left": width+"px"});}
				$(banner).find("img.jSboxBanner-img2").css({"left": "-100px", opacity: "0"});
				setTimeout(function(){
					showjSboxBanner(banner, repeat);
				}, 600);
			}, (repeat+img1_speed+img2_speed));
		}		
	}
	
});
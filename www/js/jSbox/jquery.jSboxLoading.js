(function($) {

    $.fn.loadingProduct = function(load) {
		var container = $(this);
		if (load == "white"){
			var windowH = $(window).height();
			var scrollTop = window.pageYOffset ? window.pageYOffset : document.body.scrollTop;
			if ($(container).length){
				var width = $(container).outerWidth();
				var height = $(container).outerHeight();
				var top = $(container).offset().top;
				var scroll="";
				if (top > scrollTop){scroll = parseInt((windowH-top+scrollTop)/2);}
				else {scroll = (windowH/2)+(scrollTop-top)-120;}
				if (scroll < 200){scroll = 200;}
				$(container).after('<div id="ajax-loading" style="width:'+width+'px; height:'+height+'px"><div style="top:'+scroll+'px;"></div></div>');
				$(container).fadeOut(0);
			}
			else {
				if ($("div.no_result").length){
					var width = $("div.no_result").outerWidth();
					var height = 400;
					var top = $("div.no_result").offset().top;
					var scroll="";
					if (top > scrollTop){scroll = parseInt((windowH-top+scrollTop)/2);}
					else {scroll = (windowH/2)+(scrollTop-top)-120;}
					if (scroll < 200){scroll = 200;}
					$("div.no_result").after('<div id="ajax-loading" style="width:'+width+'px; height:'+height+'px"><div style="top:'+scroll+'px;"></div></div>');
					$("div.no_result").fadeOut(0);				
				}
			}
		}
		else {
			$("body").append('<div id="processing"><div><span id="pmessage">Подождите, идет обработка запроса...</span></div></div>');
			$("body div#processing").fadeIn(200);		
		}
	}
	
    $.fn.loadingProductEnd = function(load) {
		var container = $(this);
		if (load == "white"){
			$("#ajax-loading").remove();
			$(container).fadeIn(0);
			$(container).find("img").each(function(key, item){
				$(item).delay(50*key).fadeTo(800, 1);
			});
		}
		else {
			$("body div#processing").fadeOut(400, function(){
				$(this).remove();
			});			
		}
	}

})(jQuery);
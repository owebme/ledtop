(function($) {	
	$.fn.jSboxBasketStatus = function(){
		$.ajax({
			url: '/cgi-bin/basket_ajax.cgi',
			type: "POST",
			data: "load",
			success : function(obj) {
				$("div.basket div.container").empty().append(obj);
			}
		});
	}	

    $.fn.jSboxAddBasket = function(opt) {
		opt = jQuery.extend({
			width : 433,
			speed : 0,
			theme : "gray",
			border : true,
			borderWidth : 6,
			image : false,
			window: true
				}, opt);	
	
		$(this).live('click', function(e){
			if (!opt.window){
				var rand = parseInt(Math.random()*1000);
				var cordX = e.pageX-10;
				var cordY = e.pageY+25;
				$("div#jSbox-message").fadeOut(150);
				$("body").append('<div class="jSbox-'+rand+'" style="top:'+cordY+'px; left:'+cordX+'px;" id="jSbox-message"><i id="jSbox-corner"></i>Товар добавлен <a href="/basket/">в корзину</a></div>');
				
				return false;
			}
			else {		
				var jSbox="";
				var widthBox = opt.width;
				var scrollTop = window.pageYOffset ? window.pageYOffset : document.body.scrollTop;
				var marginLeft = -(widthBox/2);
				var id = $(this).attr("p_id");
				var img="";
				if (opt.image){
					$("div.foto").find("img").each(function(){
						if ($(this).attr("p_id") == id) {
							img = '<img src="'+$(this).attr("src")+'" alt=""><div style="clear:both"></div>';
						}
					});
				}
				var content = '<h3></h3>'+img+'<a href="/basket/" class="submit">Перейти в корзину</a><a href="#!" class="submit jSbox-close">Продолжить покупки</a>';
				var height="";
				if (opt.height){height = "height:"+opt.height+"px; overflow:hidden;";}			
				if (opt.border){
					jSbox += '<div id="jSbox-popup" class="border '+opt.theme+'" style="margin-left:'+marginLeft+'px">';
					jSbox += '<div id="jSbox-wrap" style="width:'+widthBox+'px; margin:'+opt.borderWidth+'px; '+height+'">';		
				} else {
					jSbox += '<div id="jSbox-popup" class="'+opt.theme+'" style="margin-left:'+marginLeft+'px">';
					jSbox += '<div id="jSbox-wrap" style="width:'+widthBox+'px; '+height+'">';
				}
				jSbox += '<div id="jSbox-container" class="add_basket">';
				jSbox += content;
				jSbox += '</div></div></div>';

				var windowH = $(window).height();			
				var marginTopAjax = (windowH-40)/2;
				var marginLeftAjax = -(40/2);
				$("body").append('<div id="jSbox-overlay"></div>'+jSbox);

				var heightBox = $("div#jSbox-popup").height();
				
				$("div#jSbox-popup").css({'top':'50%','margin-top':-(heightBox/2)+'px'});
					
				window.setTimeout(function(){
					$("div#jSbox-overlay").fadeIn(100);
					$("div#jSbox-popup").addClass("animate2").css({"position": "fixed", "display": "block", "opacity": "0"});
					$("div#jSbox-popup").addClass("bounceIn");
					window.setTimeout(function(){
						$("div#jSbox-popup").removeClass("animate2").removeClass("bounceIn").css({"opacity": "1"});
					}, 1000);
				}, opt.speed);
				
				return false;
			}
		});

		$("div#jSbox-overlay, a.submit.jSbox-close").live('click', function(){
			$().jSboxClose();
			return false;
		});
		
		$(document).keydown(function(e){
			if (e.which == 27){
				$().jSboxClose();
				return false;
			}
		});	
    }
	
	$.fn.jSboxClose = function() {
		$("div#jSbox").html($("div#jSbox-container").html());		
		$("div#jSbox-overlay").fadeOut(200);
		$("div#jSbox-popup").fadeOut(200, function(){
			$("div#jSbox-popup").remove();
			$("div#jSbox-overlay").remove();
		});
	}
	
	$().jSboxBasketStatus();

})(jQuery);
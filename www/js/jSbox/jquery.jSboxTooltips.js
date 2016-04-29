(function($) {
    $.fn.SimpleTooltip = function(target_items, name) {
		$(this).live("hover", function(){
			$('.tool2del').remove();
			$(target_items).each(function(i){
				if ($(this).attr('oldtitle') && !$(this).attr('title')) $(this).attr('title', $(this).attr('oldtitle'));
				if ($(this).attr('title') != ""){
					$("body").append("<div class='"+name+" tool2del' id='"+name+i+"'><p>"+($(this).attr('alt')?"<span>"+$(this).attr('alt')+"</span>":"")+$(this).attr('title')+"</p></div>");
					var my_tooltip = $("#"+name+i);
					$(this).attr('oldtitle', $(this).attr('title')).removeAttr("title").mouseover(function(){
							my_tooltip.css({opacity:0.9, display:"none"}).fadeIn(150);
					}).mousemove(function(kmouse){
								if (new String (document.location.href).search (/checkout2.inc.php|delhowmuch/) > -1) {
									my_tooltip.css({left:kmouse.pageX - 160 
													+ Math.max(0, 160 - kmouse.pageX)//left offset
													- Math.max(0,  160 + 10 + kmouse.pageX - $(window).width())//right offset
												, top:kmouse.pageY-50});
												
								} else if (new String (document.location.href).search (/regedit|register|checkout|guru/) > -1) {
									my_tooltip.css({left:kmouse.pageX - 160 
													+ Math.max(0, 160 - kmouse.pageX)//left offset
													- Math.max(0,  160 + 10 + kmouse.pageX - $(window).width())//right offset
												, top:kmouse.pageY+20});
								} else {
									my_tooltip.css({left:kmouse.pageX + 15 
												, top:kmouse.pageY+15});
								}
					}).mouseout(function(){
							my_tooltip.fadeOut(150);
					});
				}
			});
		});		
	}
	
})(jQuery);	
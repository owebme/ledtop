(function($) {
    $.fn.jSboxViewProduct = function() {
	
		$(this).live("click", function(){			
			var el = $(this);
			var view = $(el).parent().attr("class");
			$(el).parent().parent().find("a").removeClass("active");
			$(el).addClass("active");
			$.cookie('view_products', view, {expires: 1, path: '/'});
			$("ul.products").animate({opacity: "0.2"}, 150, function(){
				$("ul.products").removeClass("view1").removeClass("view2").removeClass("view3");
				$("ul.products").addClass(view);
				$("ul.products").animate({opacity: "1"}, 150);
			});
			
			return false;
		});
	}		

})(jQuery);
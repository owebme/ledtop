(function($) {
	$.fn.jSboxCompareStatus = function(opt) {
		opt = jQuery.extend({
			theme : "white"
				}, opt);	
	
		var compare = $.cookie("compare_products");
		var count="";
		if (compare){
			var reg	= /(\d+)/g;
			count = compare.match(reg);
			count = count.length;
			if (count > 0){
				$("body").append('<div class="compare_products '+opt.theme+'"></div>');
				var msg="";
				if (count == 1){msg = 'Добавлен к сравнению <span>'+count+'</span> товар';}
				else {msg = '<a href="/products/compare">Перейти</a> к сравнению <span>'+count+'</span> товаров';}
				$("div.compare_products").html(msg);
				$(window).load(function(){
					$("div.compare_products").animate({"bottom":"-1px"}, 400);
				});
			}
		}	
	}

    $.fn.jSboxAddCompare = function(opt) {
		opt = jQuery.extend({
			theme : "white"
				}, opt);
	
		$(this).live("click", function(){
			var el = $(this);
			var p_id = $(this).attr("p_id");
			var scrollTop = window.pageYOffset ? window.pageYOffset : document.body.scrollTop;
			var count="";
			var compared = $.cookie("compare_products");
			if (compared){
				var reg	= /(\d+)/g;
				count = compared.match(reg);
				count = count.length+1;
				$.cookie('compare_products', compared+''+p_id+'|', {expires: 1, path: '/'});
			}
			else {
				$.cookie('compare_products', p_id+'|', {expires: 1, path: '/'});
			}
			if ($("div.compare_products").length){
				count = parseInt($("div.compare_products span").html());
				count = count+1;
			}
			if (count < 3 || count == ""){
				var bottom = ($(window).height() - ($(el).offset().top-scrollTop))+5;
				var right = ($(window).width() - $(el).offset().left)-110;
				var msg="";
				if (count == ""){
					msg = 'Добавлен к сравнению <span>1</span> товар';
					$("body").append('<div style="bottom:'+bottom+'px; right:'+right+'px;" class="compare_products hide '+opt.theme+'">'+msg+'</div>');
					$("div.compare_products").fadeIn(200);
					$("div.compare_products").animate({"bottom":"-1px", "right":"0px"}, 600);			
				}
				else {
					msg = '<a href="/products/compare">Перейти</a> к сравнению <span>'+count+'</span> товаров';
					$("div.compare_products").html(msg);
				}
			}
			else if (count > 2){
				$("div.compare_products span").html(count);
			}
			if (count > 1){
				var bottom = $(window).height() - ($(el).offset().top-scrollTop);
				var right = $(window).width() - $(el).offset().left;
				$(el).css("position", "fixed");
				$(el).css("bottom", bottom+"px");
				$(el).css("right", right+"px");
				$(el).css("z-index", "99");
				$(el).animate({"bottom":"0px", "right":"50px", "opacity":"0"}, 600, function(){
					$(el).remove();
				});			
			}
			else {
				$(el).fadeOut(200, function(){
					$(el).remove();
				});		
			}
		});
	}
		
})(jQuery);
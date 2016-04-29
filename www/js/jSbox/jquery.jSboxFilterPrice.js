$(function() {
	if ($("div.filter_price select").length){
		var cat_alias = $.cookie('filter_price_cat');
		alias = window.location.href;
		alias = alias.replace(/(.*?)\/catalog\/(.*?)/,"$2");
		alias = alias.replace(/#(.+?)$/,"");
		alias = alias.replace(/\/page(.*)/,"");
		if (cat_alias != alias){
			$("div.filter_price select").val("0");
			$.cookie('filter_price', null, {path: '/'});
			$.cookie('filter_price_pointer', null, {path: '/'});
			$.cookie('filter_price_cat', null, {path: '/'});
		}
		else if (cat_alias == alias){
			var filter = $.cookie('filter_price');
			var ponter = $.cookie('filter_price_pointer');
			$("div.filter_price select").val(ponter+"_"+filter);
		}
	}
    jSboxFilterPrice = function() {
		var opt = "white";
		var ajax_pages = false;
		var re = /(.*?)#!/;
		if (re.test($("div.pages a").attr("href"))){ajax_pages = true;}
		var filter = String($("div.filter_price select").val());
		if (filter != "0"){
			var pointer = filter.replace(/(\w+)_(\d+)/,"$1");
			filter = filter.replace(/(\w+)_(\d+)/,"$2");
			alias = window.location.href;
			alias = alias.replace(/#(.+?)$/,"");
			alias = alias.replace(/^http:(.+?)\/catalog\//,"");
			brand_alias = alias.replace(/(.+?)\/brands\//,"");
			alias = alias.replace(/\/brands\/(.+?)$/,"");
			if (brand_alias == alias){brand_alias="";}
			$.cookie('filter_price', filter, {expires: 1, path: '/'});
			$.cookie('filter_price_pointer', pointer, {expires: 1, path: '/'});
			$.cookie('filter_price_cat', alias.replace(/\/page(.*)/,""), {expires: 1, path: '/'});
			if ($("div.sort_products").length){
				$.cookie('sort_products', 'p_price ASC', {expires: 1, path: '/'});
				$("div.sort_products i").remove();
				$("div.sort_products a").attr("id", "");
				$("div.sort_products a.price").attr("id", "active").attr("sort", "p_price ASC");
				$("div.sort_products a.price").after('<i class="up"> &uarr;</i>');
				$("div.sort_products a.update").attr("sort", "");
			}
			$("ul.products").loadingProduct(opt);
			$("ul.products").fadeOut(200);
			var params = new Object();
			params.filter_price = filter;
			params.filter_price_pointer = pointer;
			params.cat_alias = alias;
			params.page_cat = "1";
			params.brand_alias = brand_alias;
			$.post('/cgi-bin/product_ajax.cgi', params, function(data){
				if (data != ""){
					$("ul.products").after(data);
					$("ul.products:first").remove();
					if ($("div.no_result").length){
						$("div.no_result").after(data);
						$("div.no_result:first").remove();
						$("div.no_result").fadeIn(400);
						$("div.pages").fadeOut(0);
					}
					if (!$("div.pages-double").length){
						$("div.pages").fadeOut(0);
					}
					if ($("div.pages-top").length || $("div.pages-bottom").length){
						if (ajax_pages){
							$("div.pages a").each(function(){
								var num = $(this).html();
								if (isNum(num)){$(this).attr("href", "#!page_"+num);}
								else {$(this).attr("href", "#!page_all");}
							});
						}
						$("div.pages.top").replaceWith($("div.pages-top").html());
						$("div.pages.bottom").replaceWith($("div.pages-bottom").html());
						$("div.pages-double").remove();
						$("div.pages.top").fadeIn(0);
						$("div.pages.bottom").fadeIn(0);
						if ($("div.pages.wide").length){
							var wrapper = $("div.pages div.container");
							var wrapper_top = $("div.pages.top div.container");
							var wrapper_bottom = $("div.pages.bottom div.container");
							var scrollable = $("div.pages div.container div.width");
							var count_page = $("div.pages.bottom div.container div.width").children("a").length;
							var sizeWidth = parseInt(count_page-9)*24+(9*17)+2;
							$(scrollable).css("width", sizeWidth+"px");
							var inactiveMargin = 80;					
							var wrapperWidth = wrapper.width();
							var wrapperHeight = wrapper.height();
							var scrollableWidth = scrollable.outerWidth() + 2*inactiveMargin;
							wrapper_top.scrollLeft(0);
							wrapper_bottom.scrollLeft(0);
							if ($("div.pages.top").length){
								wrapper_top.mousemove(function(e){
									lastTarget = e.target;
									var wrapperOffset = wrapper_top.offset();		
									var left = (e.pageX - wrapperOffset.left) * (scrollableWidth - wrapperWidth) / wrapperWidth - inactiveMargin;
									if (left < 0){
										left = 0;
									}
									wrapper_top.scrollLeft(left);
									wrapper_bottom.scrollLeft(left);
								});	
							}
							if ($("div.pages.bottom").length){
								wrapper_bottom.mousemove(function(e){
									lastTarget = e.target;
									var wrapperOffset = wrapper_bottom.offset();		
									var left = (e.pageX - wrapperOffset.left) * (scrollableWidth - wrapperWidth) / wrapperWidth - inactiveMargin;
									if (left < 0){
										left = 0;
									}
									wrapper_bottom.scrollLeft(left);
									wrapper_top.scrollLeft(left);
								});
							}
						}						
					}
					if ($("ul.products li img").length){
						if ($("div.raiting_star").length){$().ProductRaiting();}
						if (opt == "white") {
							$("ul.products").fadeOut(0);
							$("ul.products img").css("opacity", "0");
						}
						var nmb = $("ul.products li").length;
						var cnt = 0;
						$("ul.products li img").each(function(){
							var el = $(this);
							var src = $(el).attr("src");
							$(el).attr("src", src+"?"+Math.random());
							$(el).load(function(){
							cnt++;
								if (cnt == nmb){
									$("ul.products").loadingProductEnd(opt);
								}
							});			
						});
					}
					else {
						if (opt == "white"){
							$("#ajax-loading").remove();
						}
						else {
							$("body div#processing").fadeOut(400, function(){
								$(this).remove();
							});			
						}
					}
				}		
			});
		}
		
		function isNum(input) {
			var regexp = /^[A-Za-z0-9]+$/;
			return regexp.test(input);
		}		
		
	}		

});
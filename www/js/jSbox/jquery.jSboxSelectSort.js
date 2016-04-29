(function($) {
    $.fn.jSboxSelectSort = function(opt) {
		opt = jQuery.extend({
			load : "white"
				}, opt);	
				
		$(this).live("click", function(){
			var el = $(this);
			var sort = $(el).attr("class");
			if ($("ul.products li img").length){
				$("div.sort_products i").remove();
				if ($(el).attr("class") == "price"){
					if ($(el).attr("sort") == "p_price DESC" || $(el).attr("sort") == ""){
						$(el).attr("sort", "p_price ASC");
						$(el).after('<i class="up"> &uarr;</i>');
						$.cookie('sort_products', 'p_price ASC', {expires: 1, path: '/'});
					}
					else if ($(el).attr("sort") == "p_price ASC"){
						$(el).attr("sort", "p_price DESC");
						$(el).after('<i class="down"> &darr;</i>');
						$.cookie('sort_products', 'p_price DESC', {expires: 1, path: '/'});
					}
					$("div.sort_products a.update").attr("sort", "");
				}
				else if ($(el).attr("class") == "update"){
					if ($(el).attr("sort") == "p_date_add DESC"){
						$(el).attr("sort", "p_date_add ASC");
						$(el).after('<i class="up"> &uarr;</i>');
						$.cookie('sort_products', 'p_date_add ASC', {expires: 1, path: '/'});
					}
					else if ($(el).attr("sort") == "p_date_add ASC" || $(el).attr("sort") == ""){
						$(el).attr("sort", "p_date_add DESC");
						$(el).after('<i class="down"> &darr;</i>');
						$.cookie('sort_products', 'p_date_add DESC', {expires: 1, path: '/'});
					}
					$("div.sort_products a.price").attr("sort", "");
				}
				$("ul.products").loadingProduct(opt.load);
				$("div.sort_products a").attr("id", "");
				$(el).attr("id", "active");
				$("ul.products").fadeOut(200);
				alias = window.location.href;
				alias = alias.replace(/#(.+?)$/,"");
				alias = alias.replace(/^http:(.+?)\/catalog\//,"");
				brand_alias = alias.replace(/(.+?)\/brands\//,"");
				alias = alias.replace(/\/brands\/(.+?)$/,"");
				if (brand_alias == alias){brand_alias="";}	
				var page="";
				if ($("div.pages:first a.current").length){
					if ($("div.pages:first a.current").html() == "Все товары"){page = "all";}
					else {page = $("div.pages:first a.current").html()}
				}
				var params = new Object();
				params.sort = $(el).attr("sort");
				params.cat_alias = alias;
				params.page_cat = page;
				params.brand_alias = brand_alias;
				$.post('/cgi-bin/product_ajax.cgi', params, function(data){
					if (data != ""){	
						$("ul.products").after(data);
						$("ul.products:first").remove();
						if ($("div.raiting_star").length){$().ProductRaiting();}
						if (opt.load == "white") {
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
									$("ul.products").loadingProductEnd(opt.load);
								}
							});			
						});
					}		
				});
			}
			return false;
		});
	}		

})(jQuery);
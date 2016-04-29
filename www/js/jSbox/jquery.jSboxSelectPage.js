(function($) {
    $.fn.jSboxSelectPage = function(opt) {
		opt = jQuery.extend({
			load : "white",
			active : true
				}, opt);	
				
		var alias = window.location.href;				

		if (opt.active){
			var isCtrl = false;
			var isCmd = false;
			$(document).keyup(function(e) {
				if(e.which == 17) isCtrl=false;
				if(e.which == 91) isCmd=false;
			}).keydown(function(e) {
				if(e.which == 17) isCtrl=true;
				if(e.which == 91) isCmd=true;
				if(e.which == 39 && (isCtrl || isCmd)) {
					SelectPageRight();
					e.preventDefault();			
				}
				if(e.which == 37 && (isCtrl || isCmd)) {
					SelectPageLeft();
					e.preventDefault();			
				}		
			});
		
			$(this).live('click', function(){
				var el = $(this);
				if ($(el).attr("class") != "current" && !$("div#content div#ajax-loading").length){
					var page = $(this).html();
					SelectPage(page, $(this));
				}
				//return false;
			});

			$("div.pages a").each(function(){
				var num = $(this).html();
				if (isNum(num)){$(this).attr("href", "#!page_"+num);}
				else {$(this).attr("href", "#!page_all");}
			});
			
			var rand="";
			$("div.pages.wide").live("mouseenter", function(e){
				rand = parseInt(Math.random()*1000);
				var cordX = $(this).offset().left;
				var cordY = $(this).offset().top+37;
				$("div#jSbox-message").fadeOut(150);
				$("body").append('<div class="jSbox-'+rand+'" style="top:'+cordY+'px; left:'+cordX+'px; font-family:Trebuchet MS !important; opacity:0.95;" id="jSbox-message"><i id="jSbox-corner"></i>Смена страниц <b>Ctrl</b> + <b style="position:relative; top:-1px;">&rarr;</b> и <b>Ctrl</b> + <b style="position:relative; top:-1px;">&larr;</b></div>');	
				$("div.jSbox-"+rand).fadeIn(300);
			});		
			$("div.pages.wide").live("mouseleave", function(e){
				$("div.jSbox-"+rand).fadeOut(400, function(){
					$(this).remove();
				});
			});	
		}
		else {
			if ($("div.pages.wide").length){
				var page_num = parseInt($("div.pages.wide a.current").html());
				if (isNum(page_num)){
					var left="";
					if (page_num > 9){left = parseInt(page_num-9)*24+(9*17-25);}
					if (left < 0){left = 0;}
					$("div.pages.top div.container").scrollLeft(left);
					$("div.pages.bottom div.container").scrollLeft(left);
				}
			}		
		}
		
		var page_num = alias.replace(/(.+?)#!page_/,"");
		var el="";
		if (page_num == "all" || isNum(page_num)){
			if (page_num == "all"){el = $("div.pages a.viewall");}
			else {el = $("div.pages a:nth-child("+page_num+")");}			
			SelectPage(page_num, el);
			if ($("div.pages.wide").length && isNum(page_num)){
				window.setTimeout(function(){
				var left="";
				if (page_num > 9){left = parseInt(page_num-9)*24+(9*17-25);}
				if (left < 0){left = 0;}
				$("div.pages.top div.container").scrollLeft(left);
				$("div.pages.bottom div.container").scrollLeft(left);
				}, 200);
			}
		}
		
		function SelectPage(num, elem) {
			var el = elem;
			var parent_cl = $(el).parent().attr("class");
			if ($(el).parent().parent().parent().attr("class") == "pages wide bottom"){
				parent_cl = "pages bottom";
			}
			var page = num;
			$("div.pages a").removeClass("current");
			$("div.pages a").each(function(){
				if ($(this).html() == $(el).html()){
					$(this).addClass("current");
				}
			});
			$("ul.products").loadingProduct(opt.load);

			if ($(el).attr("class") == "viewall current"){page = "all";}
			var cat_alias="";
			if ($("div.pages").length) {cat_alias = $("div.pages").attr("data-alias");}
			else {cat_alias = alias.replace(/(.+?)\/catalog\/(.+?)#!(.*)/, "$2");}
			var params = new Object();
			params.cat_alias = cat_alias;
			params.page_cat = page;
			params.brand_alias = $("div.pages").attr("data-brand-alias");		
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
								if (parent_cl == "pages bottom"){
									$.scrollTo({top:$("div#content").offset().top, left:0}, 600, function(){
										$("ul.products").loadingProductEnd(opt.load);
									});
								}
								else {
									$("ul.products").loadingProductEnd(opt.load);
								}
							}
						});			
					});
				}
			});
		}
		
		function SelectPageRight() {
			var page=""; var el="";
			var count_page = parseInt($("div.pages.bottom a").size()-1);
			$("div.pages a").each(function(){
				if ($(this).attr("class") == "current"){
					page = parseInt($(this).html());
					el = $(this).next();
				}
			});
			if ((page+1) <= count_page && !$("div#content div#ajax-loading").length){
				if ($("div.pages.wide").length){
					var left="";
					if (page < 10){left = parseInt(page*17);}
					else {left = parseInt(page-9)*24-1+(9*17);}
					if (left < 0){
						left = 0;
					}
					$("div.pages.top div.container").scrollLeft(left);
					$("div.pages.bottom div.container").scrollLeft(left);
				}
				SelectPage((page+1), el);
			}
		}

		function SelectPageLeft() {
			var page=""; var el="";
			var count_page = parseInt($("div.pages.bottom a").size()-1);				
			$("div.pages a").each(function(){
				if ($(this).attr("class") == "current"){
					page = parseInt($(this).html());
					el = $(this).prev();
				}
			});
			if ((page-1) != "0" && !$("div#content div#ajax-loading").length){
				if ($("div.pages.wide").length){
					var left="";
					page = page-1;
					if (page < 10){left = parseInt(page*17)-17;}
					else {left = parseInt(page-9)*24+(9*17-25);}
					if (left < 0){
						left = 0;
					}
					$("div.pages.top div.container").scrollLeft(left);
					$("div.pages.bottom div.container").scrollLeft(left);
				}				
				SelectPage((page-1), el);
			}	
		}		
		
		function isNum(input) {
			var regexp = /^[A-Za-z0-9]+$/;
			return regexp.test(input);
		}	
		
	}

})(jQuery);
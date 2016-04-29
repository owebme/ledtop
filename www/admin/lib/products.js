var dirs_catalog = '/cgi-bin/admin/modules';

$(document).ready(function(){

	$("div#sheettop li.first a").attr("href", $("div#main_menu div#products a").attr("href"));

	// Обработка f5, ctrl+f5 и Esc
	var isCtrl = false;
	var isCmd = false;
	$(document).keyup(function(e) {
		if(e.which == 17) isCtrl=false;
		if(e.which == 91) isCmd=false;
	}).keydown(function(e) {
		if(e.which == 17) isCtrl=true;
		if(e.which == 91) isCmd=true;
		if(e.which == 116 && (isCtrl || isCmd) || e.which == 116) {
			if (getUrlVars()["par"] == "new"){return true;}
			else if (!getUrlVars()["num_edit"]){
				location.replace($("div#main_menu div#products a").attr("href"));
				e.preventDefault();
			}
			else {
				return true;
			}
		}
		else if (e.which == 27){
			if (getUrlVars()["par"] == "new"){
				if (confirm('Отменить создание товара?')) {
					location.replace($("div#main_menu div#products a").attr("href"));
					e.preventDefault();
				} else {
					return false;
				}
			}
		}
		else if (e.which == 81 && (isCtrl || isCmd)){
		var cat_show = $("div#category_products ul li a.show_cat.active").attr("cat_show");
		$(".main_button:first").removeClass("active");
			advAJAX.post({
				url: (dirs_catalog+'/products_ajax.cgi'),
				cat_resort: cat_show,
				onLoading: function(obj) {
				$("div#allProducts").load("/admin/js/ajax_load.html");
				}, 
				onSuccess : function(obj) {
					$("div#allProducts").animate({opacity:"hide"}, 200, function(){
						$(this).empty().append(obj.responseText);	
						$(this).animate({opacity:"show"}, 200, function(){
							sortProduct("#product_foto");
							move_product_foto();
							lamp_product();
							del_product();
							rename_product();
							edit_price();
						});
					});
				}
			});
			e.preventDefault();
		}
	});
	
	$("table#page_new input").keydown(function(e){
		if (e.which == 13){
			e.preventDefault();	
			return false;
		}		
	});
	
	if (isNaN($("#product_foto").html())){
		sortProduct("#product_foto");
	}
	else if (isNaN($("#product_list").html())){
		sortProduct("#product_list");
	}
	
	$("div.prev_img").each(function(){
		var el = $(this);
		var heightDiv = parseInt($(el).height());
		var heightImg = parseInt($(el).find("img").height());
		if (heightImg < heightDiv && $(el).find("img").attr("style") != ""){
			var def = (heightDiv-heightImg)/2;
			$(el).find("img").css("marginTop", def+"px");
		}
	});
	
	$("ul.gallery_product li div.foto").each(function(){
		var el = $(this);
		var heightDiv = parseInt($(el).height());
		var heightImg = parseInt($(el).find("img").height());
		if (heightImg < heightDiv && $(el).find("img").attr("style") != ""){
			var def = (heightDiv-heightImg)/2;
			$(el).find("img").css("marginTop", def+"px");
		}
	});	
	
	// Быстрый поиск по каталогу
	
	if (!getUrlVars()["par"] && !getUrlVars()["settings"] && !getUrlVars()["num_edit"]){
		$.ajax({
			url: dirs_catalog+'/products_ajax.cgi?autocomplete=load',
			dataType: 'json'
		}).done(function (source) {

			var countriesArray = $.map(source, function (value, key) { return { value: value, data: key }; }),
				countries = $.map(source, function (value) { return value; });

			$('input#word_search').autocomplete({
				lookup: countriesArray,
				onSelect: function (suggestion) {
					var id = suggestion.data.replace(/(.+?)\[(.+?)\]/g, '$1');
					id = id-1000;
					location.replace("/cgi-bin/admin/engine/index.cgi?adm_act=products&num_edit="+id);
				}
			});
			
		});	
	}
	
	$("input#word_search").focus(function(){
		if (!$("div#catalog.wide").length){
			if ($(this).parent().parent().attr("class") == "search_catalog introjs-showElement"){
				$("div.introjs-helperLayer").css("width", "404px");
			}
			$(this).animate({"width": "350px"}, 400);
		}
	});
	
	$().ContextMenu();

	$("ul#product_foto li").live('mouseover', function(){
		$("a.product_clone").fadeOut(150, function(){
			$(this).remove();
		});
	});
	
	$("a.product_clone").live('click', function(){
		var id = $(this).attr("data-id");
		if (!$("ul#product_foto li.clone").length){
			$("div#allProducts ul li").each(function(){
				var el = $(this);
				if ($(el).attr("p_id") == id){
					var pos = $(el).attr("p_pos");
					var item = $(el).html();
					$(el).after('<li class="clone">'+item+'</li>');
					$(el).next("li").find("div.foto").append("<span></span>");
				}
			});
			$("div#allProducts").addClass("loading");
			$("div#allProducts ul li").css("opacity", "0.5");
			$("ul#product_foto").sortable("disable");
			$(this).fadeOut(150, function(){
				$(this).remove();
			});
			var params = new Object();
			params.product_clone = id;
			$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
				if (data != ""){
					if ($("ul#product_foto li").attr("p_pos") != ""){
						var pos = parseInt($("ul#product_foto li:first").attr("p_pos"));
						$("ul#product_foto li").each(function(){
							$(this).attr("p_pos", pos);
							pos = pos+1;
						});
					}
					$("ul#product_foto li").animate({"opacity": "1"}, 200, function(){
						$("ul#product_foto li.clone a:first").attr("href", "?adm_act=products&num_edit="+data);
						$("ul#product_foto li.clone a.move_left").attr("id_move", data);
						$("ul#product_foto li.clone a.move_right").attr("id_move", data);
						$("ul#product_foto li.clone a.product_del").attr("del_id", data);
						$("ul#product_foto li.clone").attr("p_id", data).removeClass("clone").find("div.foto").children("span").remove();
						var products = $("div#allProducts").html();
						$("div#allProducts").empty().append(products);
						if ($("ul#product_foto li").attr("p_pos") != ""){
							if (isNaN($("#product_foto").html())){
								sortProduct("#product_foto");
							}
							else if (isNaN($("#product_list").html())){
								sortProduct("#product_list");
							}	
							move_product();
							move_product_foto();						
						}
						lamp_product();
						del_product();
						rename_product();
						edit_price();
						edit_price_list();
						$().ContextMenu();
						$("ul#product_foto li").mouseout(function(){
							$("div#allProducts").removeClass("loading");
						});
					});
				}
			});
		}
		return false;
	});	
		
});

	jQuery.fn.ContextMenu = function() {
		$("ul#product_foto li").bind('contextmenu', function(e){
			if (e.button === 2){
				$("a.product_clone").remove();
				var pCoordX = e.pageX+15;
				var pCoordY = e.pageY+12;
				var top = $(this).offset().top;
				var left = $(this).offset().left;
				var def_left = parseInt(pCoordX-left);
				var def_top = parseInt(pCoordY-top);
				if (def_left > 120){pCoordX = pCoordX-80;}
				if (def_top > 100){pCoordY = pCoordY-40;}
				var id = $(this).attr("p_id");
				$("body").append('<a class="product_clone" data-id="'+id+'" href="#">Создать копию</a>');
				$("a.product_clone").css({'left':pCoordX, 'top':pCoordY, 'z-index':10000}).fadeIn(150);
				e.preventDefault();
			}
		});	
	}

	function getUrlVars() {
		var vars = {};
		var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
			vars[key] = value;
		});
		return vars;
	}

	function sortProduct(type){
	
		if ($("a.cat_show_all").attr("sort") == "active" && $("a.cat_show_all").parent().parent().attr("class") == "main_button"){
	
			var count_product = $(type+" li").size();
			
			$(type).sortable({
				revert: 200,
				start: function(event, ui){
					  $(type).attr("move_id", ui.helper.attr("p_id"));
					  var move_id = $(type).attr("move_id");
					  for (i=1; i < count_product+1; i++){
						if ($(type+" li:nth-child("+i+")").attr("p_id") == move_id){
							pos_old = i;
						}
					  }
					  $(type).attr("p_pos", pos_old);
				},
				stop: function(){
					if ($("div#category_products ul li div.moved").html() != "Перемещен"){
						$(type).sortable("disable");
						var pos_new="";
						var move_id = $(type).attr("move_id");
						for (i=1; i < count_product+1; i++){
							if ($(type+" li:nth-child("+i+")").attr("p_id") == move_id){
								pos_new = i;
							}			
						}
						var pos_old = parseInt($(type).attr("p_pos"));
						if (pos_new != pos_old){
							var pos_step ="";
							var params = new Object();
							if (pos_new > pos_old){
								pos_step = pos_new-pos_old;
								params.product_pos_step_right = pos_step;
							}
							else if (pos_old > pos_new){
								pos_step = pos_old-pos_new;
								params.product_pos_step_left = pos_step;					
							}				
							params.product_move = move_id;					
							params.product_cat_id = $(type).attr("id_cat");
							$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
								if (data != ""){
									$(type+" li[move_id="+$(type).attr("move_id")+"]").attr("p_pos", data);
									$(type).sortable("enable");
								}
							});
						}
						else {
							$(type).sortable("enable");
						}
					}
					else if ($("div#category_products ul li div.moved").html() == "Перемещен"){
						var params = new Object();
						params.product_moved_cat = p_id;					
						params.product_cat_id = cat_id;				
						$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
							if (data != ""){
								$("#product_foto").sortable("enable");
							}
						});				
					}
				}
			});
			
			var p_id ="";
			var cat_id="";
			$("div#category_products ul li").droppable({
				accept: "ul#product_foto li",
				hoverClass: "hover",
				drop: function(event, ui){
					$("#product_foto").sortable("disable");
					var el = ui.draggable;
					var elem = $(this);
					p_id = $(el).attr("p_id");
					$(elem).append('<div class="moved">Перемещен</div>');
					cat_id = $("div#category_products ul li div.moved:last").prev("a").attr("cat_show");
					if (isNaN(cat_id)){cat_id = $(elem).children("a").attr("cat_show");}
					$(el).fadeOut(200, function(){
						$(el).remove();
						$("div#category_products ul li div.moved:last").fadeIn(400, function(){
							window.setTimeout(function(){
								$("div#category_products ul li div.moved:last").fadeOut(400, function(){
									$("div.moved").remove();
								});
							}, 800);
						});					
					});
				}
			});		
		}
	}	

$(function(){
$("ul#product_foto li").live('mouseover mouseout', function(e){
	if( e.type == 'mouseover' ){
		var id = $(this).attr('p_id');
		$("a.move_left").each(function(){
			if( $(this).attr('id_move') == id) $(this).fadeIn(0);
		});
		$("a.move_right").each(function(){
			if( $(this).attr('id_move') == id) $(this).fadeIn(0);
		});
		$("a.product_del").each(function(){
			if( $(this).attr('del_id') == id) $(this).fadeIn(0);
		});			
	} else if( e.type == 'mouseout' ){
        $("a.move_left").stop(true, true);	
        $("a.move_right").stop(true, true);	
        $("a.product_del").stop(true, true);		
		$("a.move_left").each(function(){
			if( $(this).attr('id_move') != id) $(this).fadeOut(0);
		});
		$("a.move_right").each(function(){
			if( $(this).attr('id_move') != id) $(this).fadeOut(0);
		});	
		$("a.product_del").each(function(){
			if( $(this).attr('del_id') != id) $(this).fadeOut(0);
		});			
	}
});	
});	


$(function(){

	// Поиск по каталогу

	$("input#search").live("click", function(){
		var el = $(this);
		var word = $("input#word_search").val();
		if (word != "" && word != "Поиск:"){
			$(el).addClass("active");
			$(".main_button:first").removeClass("active");
			$("div#category_products a").removeClass("active");	
			$("div#allProducts").append('<div class="clear"></div>');
			var sizeBlock = parseInt($("div#allProducts").height());
			if (!$("div#allProducts ul").length){sizeBlock = 400;}
			$("div#allProducts").css("height", sizeBlock+"px");		
			$("div#allProducts").empty().append('<div id="ajax_loading"></div>');
			$("div.pages").remove();
			
			var params = new Object();
			params.search_word = word;
			$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
				if (data != ""){
					if (data == "no"){
						$("div#allProducts").html('<div id="allProducts"><div class="message">Ничего не найдено, попробуйте поменять поисковый запрос.</div></div>');
						$(el).removeClass("active");
					}
					else {
						$("div#allProducts").replaceWith(data);
						imgProductLoader();
						var size = parseInt($("div#allProducts ul").height()+56);
						if ($("div#allProducts ul#product_foto").length && size < 400){
							size = 400;
						}
						else if ($("div#allProducts ul#product_list").length && size < 464){
							size = 464;
						}
						$("div#allProducts").animate({"height":size+"px"}, 400);
						$(el).removeClass("active");
						simple_tooltip("ul#product_list li a#p_name","tooltip_foto");
						lamp_product();
						del_product();
						rename_product();
						edit_price();
						edit_price_list();
						$().PagesScroll();
					}
				}
			});
		}
		else {
			alert("Введите слово для поиска");
			return false;
		}
		return false;
	});
	

$("a.cat_show_all").live("click", function(){
	var el = $(this);
	$("div#category_products a").removeClass("active");		
	$(el).parent().parent().addClass("active");
	$("div#main_menu div#products a").attr("href", "/cgi-bin/admin/engine/index.cgi?adm_act=products");
	$("div#allProducts").append('<div class="clear"></div>');
	var sizeBlock = parseInt($("div#allProducts").height());
	if (!$("div#allProducts ul").length){sizeBlock = 400;}
	$("div#allProducts").css("height", sizeBlock+"px");		
	$("div#allProducts").empty().append('<div id="ajax_loading"></div>');
	$("div.pages").remove();
	
	var params = new Object();
	params.cat_show_all = "all";
	params.cat_current = "all";
	if ($("div.main_button.foto.active").length){
		params.cat_show_all_foto = "load";
	}
	else if ($("div.main_button.list.active").length){
		params.cat_show_all_list = "load";
	}	
	$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
		if (data != ""){
			$("div#allProducts").replaceWith(data);
			imgProductLoader();
			var size = parseInt($("div#allProducts ul").height()+56);
			if ($("div#allProducts ul#product_foto").length && size < 400){
				size = 400;
			}
			else if ($("div#allProducts ul#product_list").length && size < 464){
				size = 464;
			}
			$("div#allProducts").animate({"height":size+"px"}, 400);
			simple_tooltip("ul#product_list li a#p_name","tooltip_foto");
			lamp_product();
			del_product();
			rename_product();
			edit_price();
			edit_price_list();
			$().PagesScroll();
			$().ContextMenu();
		}
	});

	return false;
});


$("div.select_category select").change(function(){
	var cat_show = $(this).val();
	$(".main_button:first").removeClass("active");
	$("div#category_products a").removeClass("active");
	$("div#category_products a").each(function(){
		var el = $(this);
		if ($(el).attr("cat_show") == cat_show){
			$(el).addClass("active");
		}
	});
	ChangeCategory($(this).val());
});

$("a.show_cat").live("click", function(){
	var el = $(this);
	cat_show = $(el).attr("cat_show");
	$(".main_button:first").removeClass("active");
	$("div#category_products a").removeClass("active");
	$(el).addClass("active");
	ChangeCategory(cat_show);
	return false;
});

function ChangeCategory(id){
	var cat_show = id;	
	$("div#main_menu div#products a").attr("href", "/cgi-bin/admin/engine/index.cgi?adm_act=products&cat_show="+cat_show);
	$("div#allProducts").append('<div class="clear"></div>');
	var sizeBlock = parseInt($("div#allProducts ul").height());
	if (!$("div#allProducts ul").length){sizeBlock = 400;}
	if ($("div#allProducts ul#product_foto").length && sizeBlock < 400){
		sizeBlock = 400;
	}
	else if ($("div#allProducts ul#product_list").length && sizeBlock < 464){
		sizeBlock = 464;
	}	
	$("div#allProducts").css("height", sizeBlock+"px");		
	$("div#allProducts").empty().append('<div id="ajax_loading"></div>');
	$("div.pages").remove();
	
	var params = new Object();
	params.cat_show_ajax = cat_show;
	params.cat_current = cat_show;
	$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
		if (data != ""){
			$("div#allProducts").replaceWith(data);
			imgProductLoader();
			var size = parseInt($("div#allProducts ul").height()+56);
			if ($("div#allProducts ul#product_foto").length && size < 400){
				size = 400;
			}
			else if ($("div#allProducts ul#product_list").length && size < 464){
				size = 464;
			}
			$("div#allProducts").animate({"height":size+"px"}, 400);
			if (isNaN($("#product_foto").html())){
				sortProduct("#product_foto");
			}
			else if (isNaN($("#product_list").html())){
				sortProduct("#product_list");
			}				
			simple_tooltip("ul#product_list li a#p_name","tooltip_foto");
			move_product();
			move_product_foto();
			lamp_product();
			del_product();
			rename_product();
			edit_price();
			edit_price_list();
			$().PagesScroll();
			$().ContextMenu();
		}
	});
}


$("a.show_foto").live("click", function(){
	var el = $(this);
	var reg1 = /active/;
	var reg2 = /introjs-showElement/;
	var cl = $(el).parent().parent().attr("class");
	if (!cl.match(reg1) && !cl.match(reg2)){
		$(".main_button.hits").removeClass("active");
		$("a.show_list").parent().parent().removeClass("active");		
		$(el).parent().parent().addClass("active");
		$("div#allProducts").append('<div class="clear"></div>');
		var sizeBlock = parseInt($("div#allProducts").height());
		if (!$("div#allProducts ul").length){sizeBlock = 400;}
		$("div#allProducts").css("height", sizeBlock+"px");
		var current = $("div.pages a#current").attr("id_page");
		if (current == undefined){current="";}
		$("div#allProducts").empty().append('<div id="ajax_loading"></div>');

		var params = new Object();
		if ($("a.cat_show_all").parent().parent().attr("class") == "main_button active"){
			params.cat_show_all = "all";
			params.curent_page = current;
			params.cat_show_all_foto = "load";
		}
		else {
			params.show_foto = $("div#category_products a.show_cat.active").attr("cat_show");
			params.show_foto_page = current;
		}
		$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
			if (data != ""){
				$("div#allProducts").css("opacity", "0").empty().append(data);
				imgProductLoader();
				var size = parseInt($("div#allProducts ul").height()+56);
				if ($("div#allProducts ul#product_foto").length && size < 400){
					size = 400;
				}
				$("div#allProducts").animate({"height":size+"px"}, 400, function(){
					$("div#allProducts").animate({"opacity":"1"}, 200);			
				});
				sortProduct("#product_foto");
				move_product_foto();
				rename_product();
				lamp_product();
				del_product();	
				edit_price();
				$().ContextMenu();
			}
		});
	}
	
	return false;
});



$("a.show_list").live("click", function(){
	var el = $(this);
	var reg1 = /active/;
	var reg2 = /introjs-showElement/;
	var cl = $(el).parent().parent().attr("class");
	if (!cl.match(reg1) && !cl.match(reg2)){
		$(".main_button.hits").removeClass("active");
		$("a.show_foto").parent().parent().removeClass("active");		
		$(el).parent().parent().addClass("active");
		$("div#allProducts").append('<div class="clear"></div>');
		var sizeBlock = parseInt($("div#allProducts").height());
		if (!$("div#allProducts ul").length){sizeBlock = 400;}
		$("div#allProducts").css("height", sizeBlock+"px");
		var current = $("div.pages a#current").attr("id_page");
		if (current == undefined){current="";}
		$("div#allProducts").empty().append('<div id="ajax_loading"></div>');

		var params = new Object();
		if ($("a.cat_show_all").parent().parent().attr("class") == "main_button active"){
			params.cat_show_all = "all";
			params.curent_page = current;
			params.cat_show_all_list = "load";
		}
		else {
			params.show_list = $("div#category_products a.show_cat.active").attr("cat_show");
			params.show_list_page = current;
		}
		$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
			if (data != ""){
				$("div#allProducts").css("opacity", "0").empty().append(data);
				var size = parseInt($("div#allProducts ul").height()+56);
				if ($("div#allProducts ul#product_list").length && size < 464){
					size = 464;
				}	
				$("div#allProducts").animate({"height":size+"px"}, 400, function(){
					$("div#allProducts").animate({"opacity":"1"}, 200);			
				});
				sortProduct("#product_list");
				simple_tooltip("ul#product_list li a#p_name","tooltip_foto");	
				move_product();
				lamp_product();
				del_product();	
				edit_price_list();
			}
		});
	}
	
	return false;
});

jQuery.fn.PagesScroll = function() {
	if ($("div.pages.wide").length){
		var wrapper = $("div.pages.wide div.container");
		var scrollable = $("div.pages.wide div.container div.width");
		var count_page = $("div.pages.wide div.container div.width").children("a").length;
		var sizeWidth = parseInt(count_page*38);
		$(scrollable).css("width", sizeWidth+"px");
		var inactiveMargin = 80;					
		var wrapperWidth = wrapper.width();
		var wrapperHeight = wrapper.height();
		var scrollableWidth = scrollable.outerWidth() + 2*inactiveMargin;
		wrapper.mousemove(function(e){
			lastTarget = e.target;
			var wrapperOffset = wrapper.offset();		
			var left = (e.pageX -  wrapperOffset.left) * (scrollableWidth - wrapperWidth) / wrapperWidth - inactiveMargin;
			if (left < 0){
				left = 0;
			}
			wrapper.scrollLeft(left);
		});	
	}
}

$().PagesScroll();

$("a.page_cat, a.page").live('click', function(){
	var id_cat = $(this).attr("id_category");
	var current = $(this).attr("id_page");
	$("div.pages a").each(function(){
		$(this).attr("id", "");
	});
	$(this).attr("id", "current");	
	SelectPage(id_cat, current, $(this).attr("class"));
	
	return false;
});

$("div.pages a.page_right").live('click', function(){
	SelectPageRight();
	return false;
});

$("div.pages a.page_left").live('click', function(){
	SelectPageLeft();	
	return false;
});

	var isCtrl = false;
	var isCmd = false;
	$(document).keyup(function(e) {
		if(e.which == 17) isCtrl=false;
		if(e.which == 91) isCmd=false;
	}).keydown(function(e) {
		if(e.which == 17) isCtrl=true;
		if(e.which == 91) isCmd=true;
		if(e.which == 39 && (isCtrl || isCmd)) {
			$("div.select_category select").blur();
			if ($("div.pages a").length){
				SelectPageRight();
				e.preventDefault();
			}
		}
		if(e.which == 37 && (isCtrl || isCmd)) {
			$("div.select_category select").blur();
			if ($("div.pages a").length){
				SelectPageLeft();
				e.preventDefault();
			}
		}
	});
	
	function SelectPageRight(){
		var id_cat = $("div.pages div.container a:first").attr("id_category");
		var count = $("div.pages div.container a").length;
		var current="";
		$("div.pages div.container a").each(function(){
			var el = $(this);
			if ($(el).attr("id") == "current"){
				current = parseInt($(el).attr("id_page"))+1;
			}
		});	
		if (current <= count){
			$("div.pages div.container a").each(function(){
				var el = $(this);
				if ($(el).attr("id_page") == current){
					$(el).attr("id", "current");
				} else {$(el).attr("id", "");}
			});	
			var left = (current*38)-38;
			$("div.pages.wide div.container").scrollLeft(left);		
			SelectPage(id_cat, current, $("div.pages div.container a:first").attr("class"));
		}
	}
	function SelectPageLeft(){
		var id_cat = $("div.pages div.container a:first").attr("id_category");
		var count = $("div.pages div.container a").length;
		var current="";
		$("div.pages div.container a").each(function(){
			var el = $(this);
			if ($(el).attr("id") == "current"){
				current = parseInt($(el).attr("id_page"))-1;
			}
		});	
		if (current > 0){
			$("div.pages div.container a").each(function(){
				var el = $(this);
				if ($(el).attr("id_page") == current){
					$(el).attr("id", "current");
				} else {$(el).attr("id", "");}
			});	
			var left = (current*38)-38;
			$("div.pages.wide div.container").scrollLeft(left);		
			SelectPage(id_cat, current, $("div.pages div.container a:first").attr("class"));
		}
	}

	function SelectPage(id, num, type){
		var id_cat = id;
		var current = num;
		var cl = type;
		$("div#allProducts").append('<div class="clear"></div>');
		var sizeBlock = parseInt($("div#allProducts").height());
		if (!$("div#allProducts ul").length){sizeBlock = 400;}
		$("div#allProducts").css("height", sizeBlock+"px");
		$("div#allProducts").empty().append('<div id="ajax_loading"></div>');
		
		var params = new Object();
		if (cl == "page"){
			params.cat_show_all = "all";
			if ($("div.main_button.foto.active").length){
				params.cat_show_all_foto = "load";
			}
			else if ($("div.main_button.list.active").length){
				params.cat_show_all_list = "load";
			}
		}
		else {params.cat_show_ajax = id_cat;}
		params.curent_page = current;
		$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
			if (data != ""){
				$("div#allProducts").css("opacity", "0").empty().append(data);
				imgProductLoader();
				var size = parseInt($("div#allProducts ul").height()+56);
				if ($("div#allProducts ul#product_foto").length && size < 400){
					size = 400;
				}
				else if ($("div#allProducts ul#product_list").length && size < 464){
					size = 464;
				}				
				$("div#allProducts").animate({"height":size+"px"}, 400, function(){
					$("div#allProducts").animate({"opacity":"1"}, 200);			
				});
				if (isNaN($("#product_foto").html())){
					sortProduct("#product_foto");
				}
				else if (isNaN($("#product_list").html())){
					sortProduct("#product_list");
				}
				simple_tooltip("ul#product_list li a#p_name","tooltip_foto");
				if (cl == "page_cat"){
					move_product();
					move_product_foto();
				}
				lamp_product();
				del_product();
				rename_product();
				edit_price();
				edit_price_list();	
				$().ContextMenu();
			}
		});
	}

	function imgProductLoader(){
		if ($("div#allProducts ul#product_foto").length){
			$("div#allProducts ul#product_foto div.foto img").css("opacity", "0");
			$("div#allProducts ul#product_foto div.foto").append("<span></span>");
			$("div#allProducts ul#product_foto div.foto img").each(function(){
				$("div#allProducts ul#product_foto div.foto img").load(function(){
					$(this).parent().children("span").remove();
					$(this).css("opacity", "1");
				});
			});
		}
	}

	function simple_tooltip(target_items, name){
		$('.tool2del').remove();
		$(target_items).each(function(i){
			if ($(this).attr('oldtitle') && !$(this).attr('title')) $(this).attr('title', $(this).attr('oldtitle'));
			$("body").append("<div class='"+name+" tool2del' id='"+name+i+"'><div class='t_foto'><img src='"+$(this).attr('title')+"' alt=''></div></div>");
			var my_tooltip = $("#"+name+i);
			$(this).attr('oldtitle', $(this).attr('title')).removeAttr("title").mouseover(function(){
					my_tooltip.css({opacity:1, display:"none"}).fadeIn(0);
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
					my_tooltip.fadeOut(0);
			});
		});
	}

	simple_tooltip("ul#product_list li a#p_name","tooltip_foto");

	
	move_product();
	move_product_foto();
	lamp_product();	
	del_product();
	rename_product();
	edit_price();
	edit_price_list();	
	move_category();

});



var move_product = function() { 

$(function(){
    $('.upper').click(move_up);
    $('.downer').click(move_down);
	 
    function move_up(eventObject){
        var curr_li = $(this).parent().parent();
        var prev_li = $(curr_li).prev();
        prev_li.insertAfter(curr_li);
				
		advAJAX.post({
			url: (dirs_catalog+'/products_ajax.cgi'),
			product_up: $(this).parent().attr("p_id"),
			product_cat_id: $(this).parent().attr("cat_id"),
			product_pos: $(this).parent().attr("p_pos")
		});			
			return false;
    }
	 
	function move_down(eventObject){
	    var curr_li = $(this).parent().parent();
	    var next_li = $(curr_li).next();
	    next_li.insertBefore(curr_li);
		advAJAX.post({
			url: (dirs_catalog+'/products_ajax.cgi'),
			product_down: $(this).parent().attr("p_id"),
			product_cat_id: $(this).parent().attr("cat_id"),
			product_pos: $(this).parent().attr("p_pos")
		});		
			return false;
    }
});

}


var move_product_foto = function() { 

$(function(){
    $('a.move_left').click(move_up_foto);
    $('a.move_right').click(move_down_foto);
	 
    function move_up_foto(eventObject){
        var curr_li = $(this).parent();
        var prev_li = $(curr_li).prev();
        prev_li.insertAfter(curr_li);
				
		advAJAX.post({
			url: (dirs_catalog+'/products_ajax.cgi'),
			product_up: $(this).parent().attr("p_id"),
			product_cat_id: $(this).parent().parent().attr("id_cat"),
			product_pos: $(this).parent().attr("p_pos")
		});			
			return false;
    }
	 
	function move_down_foto(eventObject){
	    var curr_li = $(this).parent();
	    var next_li = $(curr_li).next();
	    next_li.insertBefore(curr_li);
		advAJAX.post({
			url: (dirs_catalog+'/products_ajax.cgi'),
			product_down: $(this).parent().attr("p_id"),
			product_cat_id: $(this).parent().parent().attr("id_cat"),
			product_pos: $(this).parent().attr("p_pos")
		});		
			return false;
    }
});

}


var lamp_product = function() {
	$("a.product_lamp").click(function() {
		var el = $(this);
		var params = new Object();
		params.product_lamp = $(this).attr("lamp_id");		
		$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
		if(data == "1"){
			$(el).parent().removeClass("off");
			$(el).animate({opacity:1}, 0);
			$(el).attr("title", "Скрыть товар");				
			return false;
		} else if(data == "0"){
			$(el).parent().addClass("off");		
			$(el).animate({opacity:0.5}, 0);	
			$(el).attr("title", "Сделать активным");				
			return false;
		}});
		return false;
		});
}

var del_product = function() { 
$("a.product_del").each(function(){
		var el = $(this);
		$(this).click(function(){
		var name_product = $(this).next().html();
		if (name_product == null) {
			name_product = "?";}
		else {
			name_product = ' "'+name_product+'"';			
		}	
		if (confirm('Удалить товар'+name_product)) {
		$(this).parent().fadeOut("slow", function(){
			$(el).parent().remove();
		});
		
advAJAX.post({
url: (dirs_catalog+'/products_ajax.cgi'),
product_del: $(this).attr("del_id")
});
			return false;

		} else {
			return false;
		}
	});
});
}

var move_category = function() {
$(function(){
    $('.upper_cat').click(move_up_cat);
    $('.downer_cat').click(move_down_cat);
	 
    function move_up_cat(eventObject){
        var curr_li = $(this).parent().parent();
        var prev_li = $(curr_li).prev();
        prev_li.insertAfter(curr_li);
				
		advAJAX.post({
			url: (dirs_catalog+'/products_ajax.cgi'),
			cat_move_up: $(this).parent().attr("c_id"),
			cat_move_pid: $(this).parent().attr("c_pid"),			
			cat_move_pos: $(this).parent().attr("c_pos")			
		});			
			return false;
    }
	 
	function move_down_cat(eventObject){
	    var curr_li = $(this).parent().parent();
	    var next_li = $(curr_li).next();
	    next_li.insertBefore(curr_li);
		advAJAX.post({
			url: (dirs_catalog+'/products_ajax.cgi'),
			cat_move_down: $(this).parent().attr("c_id"),
			cat_move_pid: $(this).parent().attr("c_pid"),			
			cat_move_pos: $(this).parent().attr("c_pos")
		});		
			return false;
    }
});
}


var rename_product = function() {
	$("ul#product_foto li span.name").click(function(){
		if ($(this).attr("class") == "name  introjs-showElement"){
			var height = $(this).height()+30;
			$("div.introjs-helperLayer").css("height", height+"px");
		}
		$(this).addClass("active");	
		if($(this).attr("editing")!='1'){
			$(this).attr("editing","1");
			$(this).html('<textarea class="editor_name" id="editor'+$(this).attr("id_name")+'">'+$(this).html()+'</textarea>');
			setActionEditor_name($("#editor"+$(this).attr("id_name")));
			$(this).css("text-decoration", "none");
		}
	});	
	function setActionEditor_name(editor){
		editor.focus();
		var intervalTimer="";
		$(editor).parent().parent().hover(function(){
			clearInterval(intervalTimer);
		}, function(){
			intervalTimer = setTimeout(
			function(){
				saveNameProduct();
			}, 200);
		});
		editor.focus(function(){
			clearInterval(intervalTimer);
		});
		editor.blur(function(){
			saveNameProduct();
		});
	}	
	function saveNameProduct(){
		var el = $("ul#product_foto li span.name.active textarea");
		$(el).parent().removeClass("active");
		$(el).parent().attr("editing","");
		$(el).parent().css("text-decoration", "underline");
		if ($(el).val() !=""){
			var params = new Object();
			params.product_name_id = $(el).parent().parent().attr("p_id");
			params.product_name = $(el).val();
			$.post(dirs_catalog+'/products_ajax.cgi', params);
			$(el).parent().html($(el).val());
		}
	}
}


var edit_price = function() {
	$("ul#product_foto li span.price span.cost").click(function(){
		$(this).addClass("active");
		if($(this).attr("editing")!='1'){
			$(this).attr("editing","1");
			$(this).html('<textarea class="editor_name" id="editor'+$(this).attr("id_name")+'">'+$(this).html()+'</textarea>');
			setActionEditor_price($("#editor"+$(this).attr("id_name")));
		}
	});	
	function setActionEditor_price(editor){
		editor.focus();
		var intervalTimer="";
		$(editor).parent().parent().parent().hover(function(){
			clearInterval(intervalTimer);
		}, function(){
			intervalTimer = setTimeout(
			function(){
				savePriceProduct();
			}, 200);
		});		
		editor.focus(function(){
			clearInterval(intervalTimer);
		});
		editor.blur(function(){
			savePriceProduct();
		});
	}	
	function savePriceProduct(){
		var el = $("ul#product_foto li span.price span.cost.active textarea");
		$(el).parent().removeClass("active");
		$(el).parent().attr("editing","");
		if ($(el).val() != ""){
			var params = new Object();
			params.product_name_id = $(el).parent().parent().parent().attr("p_id");
			params.product_price = $(el).val();
			$.post(dirs_catalog+'/products_ajax.cgi', params);
			$(el).parent().html($(el).val());
		}
	}	
}

var edit_price_list = function() {
	$("ul#product_list li span.price span.cost_list").click(function(){
		$(this).parent().addClass("active");	
		if($(this).attr("editing")!='1'){
			$(this).attr("editing","1");
			$(this).html('<textarea class="editor_name" id="editor'+$(this).attr("id_name")+'">'+$(this).html()+'</textarea>');
			setActionEditor_price_list($("#editor"+$(this).attr("id_name")));
		}
	})
	
	function setActionEditor_price_list(editor){
		editor.focus();
		var intervalTimer="";
		$(editor).parent().parent().parent().hover(function(){
			clearInterval(intervalTimer);
		}, function(){
			intervalTimer = setTimeout(
			function(){
				savePriceProductList();
			}, 200);
		});		
		editor.focus(function(){
			clearInterval(intervalTimer);
		});
		editor.blur(function(){
			savePriceProductList();
		});	
	}
	function savePriceProductList(){
		var el = $("ul#product_list li span.price.active textarea");
		$(el).parent().parent().removeClass("active");	
		$(el).parent().attr("editing","");
		if ($(el).val() != ""){
			var params = new Object();
			params.product_name_id = $(el).parent().parent().parent().attr("p_id");
			params.product_price = $(el).val();
			$.post(dirs_catalog+'/products_ajax.cgi', params);
			$(el).parent().html($(el).val());
		}
	}	
}		


$(function(){

	$("a.del_foto").live('click', function(){
		var el = $(this);
		var type = $(el).parent().attr("data-image");
		$(el).parent().animate({opacity:"hide"}, 250, function(){
			var no_img = $('<img src="/admin/img/gallery_no_photo_sm.png">');
			$(el).parent().attr("style","width:220px; height:140px").empty().append(no_img);
		 });
		if ($(el).attr("id_del") && $(el).attr("size_foto")){
			advAJAX.post({
				url: (dirs_catalog+'/products_ajax.cgi'),
				del_foto: $(el).attr("id_del"),
				size_foto: $(el).attr("size_foto")
			});
		}
		else {
			if (type == "big"){
				$("input[name=imagebg_resize]").attr("value", "");
				$("input[name=imagebg_effect]").attr("value", "");
			}
			else if (type == "small"){
				$("input[name=imagesm_resize]").attr("value", "");
				$("input[name=imagesm_effect]").attr("value", "");
			}		
		}
		
		return false;
	});


var onMouseOutOpacity = 0.67;	

$('div.prev_img').opacityrollover({
mouseOutOpacity:   onMouseOutOpacity,
mouseOverOpacity:  1.0,
fadeSpeed:         'fast',
exemptionSelector: '.selected'
});

$("input.fileInput").change(function(){
	addImgBigOne(this.files, this);
});

function addImgBigOne(files, el) {
	var elem = el;
	var type_img = $(elem).attr("name");
	var resize_sm = $("input[name=auto_small]");
	var imageType = /image.*/;
	var num = 0;
	$.each(files, function(i, file) {
		if (!file.type.match(imageType)) {
			alert('Добавляемый файл "'+file.name+'" не является картинкой');
			return true;
		}
		num++;
		if (num == 1){
			var img_big = $('<img class="paste" style="max-width:220px; max-height:240px;"/>');
			alignCenterImg($(elem).parent().parent().prev().children("td").children("div.prev_img"), img_big, "big");
			img_big.get(0).file = file;
			
			var reader = new FileReader();
			reader.onload = (function(aImg) {
				return function(e) {
					aImg.attr('src', e.target.result);
				};
			})(img_big);
			
			reader.readAsDataURL(file);
			
			$(elem).parent().parent().prev().children("td").children("div.prev_img").css("overflow", "visible").append('<a class="del_foto" href="#" style="opacity: 0.67;"></a>');
			$("input[name=imagebg_resize]").attr("value", "");
			$("input[name=imagebg_effect]").attr("value", "");

			if (resize_sm.is(':checked') && type_img == "imagebg"){
				var img_sm = $('<img class="paste" style="max-width:220px; max-height:200px;"/>');
				alignCenterImg($(elem).parent().parent().next().children("td").children("div.prev_img"), img_sm, "small");
				img_sm.get(0).file = file;
				
				var reader = new FileReader();
				reader.onload = (function(aImg) {
					return function(e) {
						aImg.attr('src', e.target.result);
					};
				})(img_sm);
				
				reader.readAsDataURL(file);			

				$(elem).parent().parent().next().children("td").children("div.prev_img").css("overflow", "visible").append('<a class="del_foto" href="#" style="opacity: 0.67;"></a>');
				$("input[name=imagesm_resize]").attr("value", "");
				$("input[name=imagesm_effect]").attr("value", "");
			}
			ShowTooltipResize();
			DroppableFoto();
		}
	});
}

function alignCenterImg(el, img, type) {
	var div = el;
	var data = img;
	if (type == "big"){$(div).empty().attr("style", "width:220px; min-height:140px; max-height:240px;").append(data);}
	else if (type == "small"){$(div).empty().attr("style", "width:220px; min-height:140px; max-height:200px;").append(data);}
	$(div).prev("div").remove();
	var heightDiv = parseInt($(div).height());
	var heightImg ="";
	$(div).find("img").load(function(){
		heightImg = parseInt($(this).height());
		if (heightImg < heightDiv){
			var def = (heightDiv-heightImg)/2;
			$(div).find("img").css("marginTop", def+"px");
		}
	});
}
	
function ShowTooltipResize() {
	var ShowTooltip="";
	$("div.prev_img").hover(function(){
		var el = $(this);
		ShowTooltip = 1;
		$(el).find("div.tooltip-b").remove();
		if ($(el).find("img.paste").length && !$("div.resize_format").length){
			$(el).append('<div class="tooltip-b"><p><a href="#" class="resize_format_img">Редактировать изображение</a></p><i></i></div>');
		}
	}, function(){
		var el = $(this);
		window.setTimeout(function(){
			if ($(el).find("img.paste").length && ShowTooltip > 0){
				$(el).find("div.tooltip-b").remove();
				ShowTooltip = 0;
			}
		}, 100);
	});
	$("div.prev_img div.tooltip-b").hover(function(){
		ShowTooltip = 0;
	}, function(){
		$(this).remove();
	});
}

// Вызов окна обрезки изображения

$("a.resize_format_img").live("click", function(){
	var el = $(this).parent().parent();
	var img = $(el).parent().children("img.paste").attr("src");
	var type = $(el).parent().attr("data-image");
	var copy = $(el).parent().children("img").attr("data-url");
	if (copy){img = "http://"+location.hostname+""+copy;}
	$("div#content div.rf_overlay").remove();
	$("div#content div.resize_format").remove();
	$("div#content").append('<div class="rf_overlay"></div><div class="resize_format"><div class="ajax"></div><div class="container"><img id="photo" style="max-width:430px; max-height:320px;" src="'+img+'" alt=""></div><button data-crop="'+type+'" class="btn crop">Обрезать</button><button class="btn cancel">Отменить</button><input type="hidden" name="x1" value="" /><input type="hidden" name="y1" value="" /><input type="hidden" name="x2" value="" /><input type="hidden" name="y2" value="" /><input type="hidden" name="cropW" value="" /><input type="hidden" name="cropH" value="" /></div>');
	$("div#content div.rf_overlay").css("width", $("div#content").width()+"px").css("height", $("div#content").height()+"px");
	$("div#content div.resize_format").fadeIn(200);
	$(el).fadeOut(200, function(){
		$(this).remove();		
	});
	
	$(el).parent().addClass("active");
	$("div.resize_format").find("img").each(function(){
		var img = $(this);
		var src = $(img).attr("src");
		$(img).attr("src", src+"?"+Math.random());
		$(img).load(function(){
			var imgWidth = parseInt($("div.resize_format img").width());
			var imgHeight = parseInt($("div.resize_format img").height());
			var cordX2=""; var cordY2="";
			if (type == "big"){
				cordX2 = parseInt($("table.autoresize input.size[name=big_x]").val());
				cordY2 = parseInt($("table.autoresize input.size[name=big_y]").val());	
			}
			else if (type == "small"){
				cordX2 = parseInt($("table.autoresize input.size[name=sm_x]").val());
				cordY2 = parseInt($("table.autoresize input.size[name=sm_y]").val());	
			}
			else if (type == "lite"){
				cordX2 = parseInt($("table.autoresize input.size[name=lite_x]").val());
				cordY2 = parseInt($("table.autoresize input.size[name=lite_y]").val());	
			}
			imgCropSet(imgWidth, imgHeight, cordX2, cordY2);
			$("div.resize_format div.ajax").remove();
			$("div.resize_format div.container").animate({opacity:"1"}, 200);
		});
	});
	return false;
});

$("div#content div.rf_overlay, div.resize_format button.cancel").live("click", function(){
	$("body").find("div.imgareaselect-selection").parent().remove();
	$("div.imgareaselect-outer").remove();
	$("div#content div.rf_overlay").remove();
	$("div#content div.resize_format").fadeOut(150, function(){
		$(this).remove();
	});
	$("div.prev_img").removeClass("active");
	$("li.get_img div.foto").removeClass("active");
});

// Обрезка краев изображения

$("div.resize_format button.crop").live("click", function(){
	var type = $(this).attr("data-crop");
	var imgCrop = $('div.resize_format img#photo').attr("src");
	var cropImgX1 = $('div.resize_format input[name=x1]').val();
	var cropImgY1 = $('div.resize_format input[name=y1]').val();
	var imgCropW = $('div.resize_format input[name=cropW]').val();
	var imgCropH = $('div.resize_format input[name=cropH]').val();
	var CropImgWidth = $("div.resize_format img").width();
	var CropImgHeight = $("div.resize_format img").height();
	var div = $("div.prev_img.active");
	var foto_id="";
	if (type == "big" || type == "small"){
		foto_id = $(div).parent().parent().next().find("input.give_url_big").attr("foto_id");
	}	
	else if (type == "lite"){
		foto_id = $(div).parent().find("input.give_url_lite").attr("num_id");		
	}
	if (foto_id == ""){foto_id = "empty";}	
	var big_x = $("table.autoresize input[name=big_x]").val();
	var big_y = $("table.autoresize input[name=big_y]").val();
	var sm_x = $("table.autoresize input[name=sm_x]").val();
	var sm_y = $("table.autoresize input[name=sm_y]").val();
	var lite_x = $("table.autoresize input[name=lite_x]").val();
	var lite_y = $("table.autoresize input[name=lite_y]").val();
	
	$(div).empty().append('<div class="ajax"></div>');	
	
	var params = new Object();
	params.imgCrop = imgCrop;
	params.type_foto = type;
	params.foto_id = foto_id;
	params.cropImgX1 = cropImgX1;
	params.cropImgY1 = cropImgY1;
	params.imgCropW = imgCropW;
	params.imgCropH = imgCropH;
	params.CropImgWidth = CropImgWidth;
	params.CropImgHeight = CropImgHeight;
	params.param_big_x = big_x;
	params.param_big_y = big_y;
	params.param_sm_x = sm_x;
	params.param_sm_y = sm_y;
	params.param_lite_x = lite_x;
	params.param_lite_y = lite_y;
	$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
		if (data != ""){
			alignCenterImg(div, data, type);
			if (type == "big"){
				$("input[name=imagebg_resize]").attr("value", "no");
			}
			else if (type == "small"){
				$("input[name=imagesm_resize]").attr("value", "no");
			}
			$("div.prev_img").removeClass("active");
			DroppableFoto();
		}
	});
	$("body").find("div.imgareaselect-selection").parent().remove();
	$("div.imgareaselect-outer").remove();
	$("div#content div.rf_overlay").remove();
	$("div#content div.resize_format").remove();
});

$("ul.gallery_product input.fileInputsm").change(function(){
	addImgLiteOne(this.files, this);
});

function addImgLiteOne(files, el) {
	var elem = el;
	var imageType = /image.*/;
	var num = 0;
	$.each(files, function(i, file) {
		if (!file.type.match(imageType)) {
			alert('Добавляемый файл "'+file.name+'" не является картинкой');
			return true;
		}
		num++;
		if (num == 1){
			var img = $('<img class="paste" style="max-width:114px; max-height:90px;"/>');
			$(elem).prev("div.foto").attr("style", "width:114px; height:90px;");
			$(elem).prev("div.foto").empty().append(img);
			var heightDiv = parseInt($(elem).prev("div.foto").height());
			var heightImg ="";
			$(elem).prev("div.foto").find("img").load(function(){
				heightImg = parseInt($(this).height());
				if (heightImg < heightDiv){
					var def = (heightDiv-heightImg)/2;
					$(elem).prev("div.foto").find("img").css("marginTop", def+"px");
				}								
			});
			img.get(0).file = file;
			
			var reader = new FileReader();
			reader.onload = (function(aImg) {
				return function(e) {
					aImg.attr('src', e.target.result);
				};
			})(img);
			
			reader.readAsDataURL(file);
			
			$(elem).prev("div.foto").append('<a class="del_photo" href="#"></a>');
		}
	});
}

$("div.prev_img").live('mouseover mouseout', function(e){
	var el = $(this).parent().parent().next().children("td");
	if (e.type == 'mouseover'){
		$(el).children("input.fileInput").hide(0);			
		$(el).children("div.browse").hide(0);
		$(el).children("input.give_url_big").show(0).focus();
	}
	else if (e.type == 'mouseout'){
		$(el).children("input.give_url_big").stop(true, true);
		$(el).children("input.fileInput").show(0);			
		$(el).children("div.browse").show(0);
		$(el).children("input.give_url_big").hide(0);
	}
});


$("div.prev_img").live('mouseover', function(){
	var div = $(this);
	var el = $(this).parent().parent().next().children("td");
	document.onkeydown = hotkeys;
	function hotkeys(e) {
		if (!e) e = window.event;
		var k = e.keyCode;
		if (e.ctrlKey && k == 86 && $(div).attr("class") == "prev_img get_image") {
			window.setTimeout(function(){
				var url = $(el).children("input.give_url_big").val();
				if (url != ""){
					$(el).children("input.give_url_big").attr("value", "");
					$(div).children("div.error").remove();
					$(div).children("img").css("opacity", "0");
					$(div).show(0);
					$(div).append('<div class="ajax"></div>');
					var type_foto = $(el).children("input.give_url_big").attr("type_foto");					
					var foto_id = $(el).children("input.give_url_big").attr("foto_id");
					if (foto_id == ""){foto_id = "empty";}
					var big_x = $("table.autoresize input[name=big_x]").val();
					var big_y = $("table.autoresize input[name=big_y]").val();
					var sm_x = $("table.autoresize input[name=sm_x]").val();
					var sm_y = $("table.autoresize input[name=sm_y]").val();
					var lite_x = $("table.autoresize input[name=lite_x]").val();
					var lite_y = $("table.autoresize input[name=lite_y]").val();					
					var hdr = $("div.foto_settings input[name=hdr]").val();
					var saturation = $("div.foto_settings input[name=saturation]").val();
					var contrast = $("div.foto_settings input[name=contrast]").val();
					var normalize=""; if ($("div.foto_settings input[name=normalize]").is(':checked')){normalize ="1";} else {normalize ="0";}
					var sharpness=""; if ($("div.foto_settings input[name=sharpness]").is(':checked')){sharpness ="1";} else {sharpness ="0";}
					var resize=""; if ($("div.foto_settings input[name=resize]").is(':checked')){resize ="1";} else {resize ="0";}
					var type_resize=""; if ($("table.autoresize input[name=type_resize]").is(':checked')){type_resize ="full";} else {type_resize ="half";}
					var params = new Object();
					params.type_foto = type_foto;
					params.foto_id = foto_id;
					params.img_url = url;
					params.param_big_x = big_x;
					params.param_big_y = big_y;
					params.param_sm_x = sm_x;
					params.param_sm_y = sm_y;
					params.param_lite_x = lite_x;
					params.param_lite_y = lite_y;					
					params.param_hdr = hdr;
					params.param_normalize = normalize;
					params.param_contrast = contrast;
					params.param_saturation = saturation;
					params.param_sharpness = sharpness;
					params.param_resize = resize;
					params.param_type_resize = type_resize;
					$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
						if (data != ""){
							if (data != "error"){
								alignCenterImg(div, data, type_foto);
								if (type_foto == "big"){
									$("input[name=imagebg_resize]").attr("value", "no");
									$("input[name=imagebg_effect]").attr("value", "");
								}
								else if (type_foto == "small"){
									$("input[name=imagesm_resize]").attr("value", "no");
									$("input[name=imagesm_effect]").attr("value", "");
								}
								ShowTooltipResize();
								DroppableFoto();
							}
							else {
								var widthDiv = parseInt($(div).width());
								var heightDiv = parseInt($(div).height());
								var heightImg = parseInt($(div).children("img"));
								if (heightImg > heightDiv){heightDiv = heightImg;}
								$(div).children("div.ajax").remove();
								url = url.replace(/Вставьте ссылку Ctrl\+V/g, "");
								url = url.replace(/^\s+/,"");
								url = url.replace(/(.*)http/g, "http");
								var msg = 'Ccылка на изображение:<span>&laquo;<b>'+url+'</b>&raquo;</span> не является картинкой';
								if (url == ""){msg = 'Cсылка не имеет адреса,<br> вы вставляете пустой адрес';}
								$(div).append('<div class="error"><p style="width:'+widthDiv+'px; height:'+heightDiv+'px;">'+msg+'</p></div>');
								$(div).children("img").css("opacity", "1");
								window.setTimeout(function(){
									$(div).children("div.error").fadeOut(200, function(){
										$(this).remove();
									});
								}, 2500);
							}
						}
					});
				}
			}, 100);
		}
	}
});


$("ul.gallery_product a.del_photo").live('click', function(){
	var el = $(this);
	if ($(el).attr("id_del") && $(el).attr("size_foto")){
		var params = new Object();
		params.del_foto = $(el).attr("id_del");
		params.del_foto_num = $(el).attr("id_foto");
		params.size_foto = $(el).attr("size_foto");
		$.post(dirs_catalog+'/products_ajax.cgi', params);
	}
	$(el).prev().animate({opacity:"hide"}, 250, function(){
		$(el).parent().empty().append('<img src="/admin/img/product_gallery_no_photo.png" alt="">');
	});
	return false;
});

$("ul.gallery_product li div.foto").live('mouseover mouseout', function(e){
	var el = $(this).parent("li");
	if (e.type == 'mouseover' && $(el).attr("class") == "get_img"){
		$(el).children("input.fileInputsm").hide();			
		$(el).children("div.browse_sm").hide();
		$(el).children("input.give_url_lite").show().focus();
	}
	else if (e.type == 'mouseout' && $(el).attr("class") == "get_img"){
		$(el).children("input.give_url").stop(true, true);
		$(el).children("input.fileInputsm").show();			
		$(el).children("div.browse_sm").show();
		$(el).children("input.give_url_lite").hide();	
	}
});

$("ul.gallery_product li").live('mouseover', function(){
	var el = $(this);
	document.onkeydown = hotkeys;
	function hotkeys(e) {
		if (!e) e = window.event;
		var k = e.keyCode;
		if (e.ctrlKey && k == 86 && $(el).attr("class") == "get_img") {
			window.setTimeout(function(){
				var url = $(el).children("input.give_url_lite").val();
				if (url != ""){
					$(el).children("input.give_url_lite").attr("value", "");
					var div = $(el).children("div.foto");
					$(div).children("div.error").remove();
					$(div).find("img").hide(0);
					$(div).append('<div class="ajax"></div>');					
					var type_foto = $(el).children("input.give_url_lite").attr("type_foto");	
					var foto_id = $(el).children("input.give_url_lite").attr("foto_id");
					if (foto_id == ""){foto_id = "empty";}
					var big_x = $("table.autoresize input[name=big_x]").val();
					var big_y = $("table.autoresize input[name=big_y]").val();
					var sm_x = $("table.autoresize input[name=sm_x]").val();
					var sm_y = $("table.autoresize input[name=sm_y]").val();
					var lite_x = $("table.autoresize input[name=lite_x]").val();
					var lite_y = $("table.autoresize input[name=lite_y]").val();					
					var num_id = $(el).children("input.give_url_lite").attr("num_id");
					var hdr = $("div.foto_settings input[name=hdr]").val();
					var saturation = $("div.foto_settings input[name=saturation]").val();
					var contrast = $("div.foto_settings input[name=contrast]").val();
					var normalize=""; if ($("div.foto_settings input[name=normalize]").is(':checked')){normalize ="1";} else {normalize ="0";}
					var sharpness=""; if ($("div.foto_settings input[name=sharpness]").is(':checked')){sharpness ="1";} else {sharpness ="0";}
					var params = new Object();
					if ($(el).attr("data-image") == "lite"){
						params.type_foto = type_foto;
						params.param_big_x = big_x;
						params.param_big_y = big_y;
						params.param_sm_x = sm_x;
						params.param_sm_y = sm_y;
						params.param_lite_x = lite_x;
						params.param_lite_y = lite_y;					
						params.param_hdr = hdr;
						params.param_normalize = normalize;
						params.param_contrast = contrast;
						params.param_saturation = saturation;
						params.param_sharpness = sharpness;
						params.foto_id = foto_id;
						params.num_id = num_id;
						params.img_url = url;
					}
					$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
						if (data != ""){
							if (data != "error"){
								$(el).children("div.foto").empty().append(data);
								var heightDiv = parseInt($(el).children("div.foto").height());
								var heightImg ="";
								$(el).children("div.foto").find("img").load(function(){
									heightImg = parseInt($(this).height());
									if (heightImg < heightDiv){
										var def = (heightDiv-heightImg)/2;
										$(el).children("div.foto").find("img").css("marginTop", def+"px");
									}
								});	
							}
							else {
								$(div).children("div.ajax").remove();
								url = url.replace(/Вставьте ссылку Ctrl\+V/g, "");
								url = url.replace(/^\s+/,"");
								url = url.replace(/(.*)http/g, "http");
								var msg = 'Ссылка на изображение<br> не является картинкой';
								if (url == ""){msg = 'Cсылка не имеет адреса,<br> вы вставляете пустой адрес';}
								$(div).append('<div class="error"><p>'+msg+'</p></div>');
								window.setTimeout(function(){
									$(div).children("div.error").fadeOut(200, function(){
										$(this).remove();
									});									
									$(div).find("img").show(0)
								}, 2500);
							}
						}
					});
				}
			}, 100);
		}
	}
});

	// Настройка изображения

	$("a.open_settings").toggle(function() {
		var el = $(this);
		var reg = /introjs-showElement/;
		if (!$(this).attr("class").match(reg)){
			var top = window.pageYOffset ? window.pageYOffset : document.body.scrollTop;
			$(el).attr("data-scroll", top+"px");
			var scroll = $(el).offset().top-165;
			$("body, html").animate({scrollTop:scroll}, 600, function(){
				$(el).attr("data-scroll-down", window.pageYOffset ? window.pageYOffset : document.body.scrollTop);		
			});
			$("div.foto_settings").fadeIn(600);
		}
		return false;
	}, function(){
		var el = $(this);
		var reg = /introjs-showElement/;
		if (!$(this).attr("class").match(reg)){
			var top = window.pageYOffset ? window.pageYOffset : document.body.scrollTop;
			if (top == $(el).attr("data-scroll-down")){
				$("body, html").animate({scrollTop:$(el).attr("data-scroll")}, 600);
			}
			$("div.foto_settings").fadeOut(400);
			$("table.autoresize").fadeOut(400);
		}
		return false;
	});
	
	// Авторазмер изображения

	$("a.show_autoresize").toggle(function() {
		var reg = /introjs-showElement/;
		if (!$(this).attr("class").match(reg)){
			$("table.autoresize").fadeIn(600);
		}
		return false;
	}, function(){
		var reg = /introjs-showElement/;
		if (!$(this).attr("class").match(reg)){	
			$("table.autoresize").fadeOut(400);
		}
		return false;
	});	
	
	// Протестировать настройки изображения
	
	$("div.foto_settings a.test_image").live('click', function(){
		$("div.foto_settings div.test_image").css("height", "200px");
		if ($("div.foto_settings div.test_image a.apply").length){
			image_effects("http://"+location.hostname+""+$("div.foto_settings div.test_image a.img1 img").attr("src"), $("div.foto_settings div.test_image a.apply").attr("data-type"));
		} else {
			image_effects();
		}		
		return false;
	});	
	
	// Применить настройки изображения
	
	$("div.foto_settings div.test_image a.apply").live('click', function(){
		var el = $(this);
		$(el).fadeOut(200, function(){$(this).remove();});
		var type_foto = $(this).attr("data-type");
		var div="";
		$("div.prev_img").each(function(){
			var elem = $(this);
			if ($(elem).attr("data-image") == type_foto){
				div = $(elem);
			}
		});
		$(div).parent().parent().next().children("td").children("input.give_url_big").attr("value", "");
		var img = "no_upload"; var re = /paste/;
		if (re.test($(div).children("img").attr("class")) && !$(div).children("img").attr("data-url")){
			img = $(div).children("img").attr("src");
		}
		$(div).empty().append('<div class="ajax"></div>');
		var hdr = $("div.foto_settings input[name=hdr]").val();
		var saturation = $("div.foto_settings input[name=saturation]").val();
		var contrast = $("div.foto_settings input[name=contrast]").val();
		var normalize=""; if ($("div.foto_settings input[name=normalize]").is(':checked')){normalize ="1";} else {normalize ="0";}
		var sharpness=""; if ($("div.foto_settings input[name=sharpness]").is(':checked')){sharpness ="1";} else {sharpness ="0";}		
		var foto_id = $(div).parent().parent().next().children("td").children("input.give_url_big").attr("foto_id");
		if (foto_id == ""){foto_id = "empty";}
		var params = new Object();
		params.image_effects = img;
		params.type_foto = type_foto;
		params.foto_id = foto_id;
		params.param_hdr = hdr;
		params.param_normalize = normalize;
		params.param_contrast = contrast;
		params.param_saturation = saturation;
		params.param_sharpness = sharpness;
		$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
			if (data != ""){
				alignCenterImg(div, data, type_foto);
				if (type_foto == "big"){
					$("input[name=imagebg_effect]").attr("value", "no");
				}
				else if (type_foto == "small"){
					$("input[name=imagesm_effect]").attr("value", "no");
				}
				ShowTooltipResize();
			}
		});
		return false;
	});	
	
	function image_effects(image, droppable_img){
		var el = $("div.foto_settings a.test_image");
		if ($(el).attr("class") != "test_image loading"){
			$(el).addClass("loading");
			if ($("div.foto_settings").attr("class") == "foto_settings"){
				var selectTop = $("div#cuselFrame-category").offset().top;
				var divTop = $("div.foto_settings").offset().top;
				var def = parseInt(divTop - selectTop);
				if (def < 198){
					var top = 158-def;
					$("div.foto_settings").animate({"margin-top":top+"px"}, 800);
					$("div.foto_settings").addClass("down");
				}
			}
			$("div.foto_settings div.test_image").remove();
			$("div.foto_settings").prepend('<div class="test_image"><div id="ajax_loading"></div></div>');
			var hdr = $("div.foto_settings input[name=hdr]").val();
			var saturation = $("div.foto_settings input[name=saturation]").val();
			var contrast = $("div.foto_settings input[name=contrast]").val();
			var normalize=""; if ($("div.foto_settings input[name=normalize]").is(':checked')){normalize ="1";} else {normalize ="0";}
			var sharpness=""; if ($("div.foto_settings input[name=sharpness]").is(':checked')){sharpness ="1";} else {sharpness ="0";}
			var params = new Object();
			params.type_foto = "test_image";
			if (image){params.test_image = image;}
			if (droppable_img){params.test_image_drop = droppable_img;}
			params.param_hdr = hdr;
			params.param_normalize = normalize;
			params.param_contrast = contrast;
			params.param_saturation = saturation;
			params.param_sharpness = sharpness;
			$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
				if (data != ""){
					$("div.foto_settings div.test_image").append('<div class="container">'+data+'</div>');
					var nmb = $("div.foto_settings div.test_image img").length;
					var cnt = 0;
					$("div.foto_settings div.test_image").find("img").each(function(){
						var img = $(this);
						$(img).load(function(){
							cnt++;
							if (cnt == nmb){
								$("div.foto_settings div.test_image div#ajax_loading").remove();
								$("div.foto_settings div.test_image div.container").fadeIn(200);
								$(el).removeClass("loading");
								$("div.foto_settings a.default").animate({top:"22"}, 200);
							}			
						});						
					});
					DroppableFoto();
				}
			});
		}
	}
	
	DroppableFoto();
	
	function DroppableFoto(){
		$("div.prev_img img").each(function(){
			var el = $(this);
			if ($(el).attr("src") != "/admin/img/gallery_no_photo_sm.png"){
				$(el).draggable({
					revert: true,
					start: function(){
						$(this).parent().css("height", $(this).height()+"px");
						$(this).animate({"width": "152px"}, 300).css("border-radius", "10px").css("z-index", "10");
						$("div.foto_settings div.test_image").addClass("active").css("height", "200px");
						$("div.foto_settings div.test_image div.container.empty").fadeIn(150);
						if ($("div.foto_settings").attr("class") == "foto_settings"){
							var selectTop = $("div#cuselFrame-category").offset().top;
							var divTop = $("div.foto_settings").offset().top;
							var def = parseInt(divTop - selectTop);
							if (def < 198){
								var top = 158-def;
								$("div.foto_settings").animate({"margin-top":top+"px"}, 800);
								$("div.foto_settings").addClass("down");
							}
						}
					},
					stop: function(){
						$(this).css("width", "auto").css("border-radius", "0px").css("z-index", "");
						$("div.foto_settings div.test_image").removeClass("active");
						$("div.foto_settings div.test_image").css("height", "200px");
					}
				});
				$("div.foto_settings div.test_image").droppable({
					accept: "div.prev_img img",
					drop: function(event, ui){
						var img = ui.draggable.attr("src");
						var el = $(this);
						var type = ui.draggable.parent().attr("data-image");
						$("div.foto_settings div.test_image").removeClass("active");
						$("div.foto_settings div.test_image div.container.empty p").remove();
						$("div.foto_settings div.test_image div.container.empty").removeClass("empty");
						var re = /paste/;
						if (re.test(ui.draggable.attr("class")) && !ui.draggable.attr("data-url")){
							image_effects(img, type);
						}
						else {
							image_effects("http://"+location.hostname+""+img, type);
						}							
					}
				});
			}
		});
	}
	
	$("div.test_image a.img1, div.test_image a.img2").live('mouseenter', function(){
		$(this).css("z-index", "3");
		var img = $(this).children("img");
		$(this).animate({marginLeft:"-20px", marginTop:"-20px", width:"176", height:"176"}, {duration:250, easing:'easeOutBack', queue:false});
		if ($(img).attr("class") == "test"){
			$(img).animate({width:"176", height:"176", marginTop:"-88px", marginLeft:"-88px"}, {duration:250, easing:'easeOutBack', queue:false});
		}
	});
	$("div.test_image a.img1, div.test_image a.img2").live('mouseleave', function(){
		var el = $(this);
		if ($(el).index() == "0"){$(el).css("z-index", "1");}
		else if ($(el).index() == "1"){$(el).css("z-index", "2");}
		var img = $(this).children("img");
		$(this).animate({marginLeft:"0px", marginTop:"0px", width:"152", height:"152"}, {duration:250, easing:'easeOutBack', queue:false});
		if ($(img).attr("class") == "test"){
			$(img).animate({width:"152", height:"152", marginTop:"-76px", marginLeft:"-76px"}, {duration:250, easing:'easeOutBack', queue:false});
		}		
	});	
	
	// Хиты продаж
	
	$(".main_button.hits").click(function(){
		var $button = $(this);
		if (!$button.hasClass("active")){
			$button.addClass("active");
			var $products = $("#allProducts");
			$products.append('<div class="clear"></div>');
			var sizeBlock = parseInt($products.height());
			if (sizeBlock < 400){sizeBlock = 400;}
			if (!$products.find("ul").length){sizeBlock = 400;}
			$products.css("height", sizeBlock+"px");		
			$products.empty().append('<div id="ajax_loading"></div>');
			$(".pages").remove();
			
			var params = new Object();
			params.product_hits = true;
			$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
				if (data != ""){
					$("#allProducts").replaceWith(data);
					sortProductHits();
					$("div.products_hits").find("li.add").click(function(){
						var params = new Object();
						params.cat_show_select = $("div.select_category").find("select").val();
						productsSelect(params, $(this).parent(), "hits");
					});
				}
			});
		}
	});
	
	$("div.products_hits ul li a.del_p").live('click', function(){
		var id = $(this).parent().attr("data-id");
		var param = $(this).parent().parent().attr("data-param");
		$(this).parent().fadeOut(200, function(){
			$(this).remove();
		});	
		var params = new Object();
		params.del_product_hits = param;
		params.del_product_hits_id = id;
		$.post(dirs_catalog+'/products_ajax.cgi', params);
		
		return false;
	});		

	function sortProductHits(ul){
		var $list = $("div.products_hits").find("ul");
		if (ul){$list = $(ul);}
		$list.each(function(){
			var $ul = $(this);
			var $add = $ul.find("li.add");
			$ul.sortable({
				revert: 200,
				cancel: $add,
				stop: function(){
					var param = $ul.attr("data-param");
					var ids="";
					$ul.find("li").each(function(){
						var el = $(this);
						if ($(el).attr("class") != "add"){
							ids += $(el).attr("data-id")+'|';
						}
					});
					var params = new Object();
					params.resort_product_hits = param;
					params.resort_product_hits_ids = ids;
					$.post(dirs_catalog+'/products_ajax.cgi', params);
				}
			}).disableSelection();
		});
	}

	// Добавление сопутствующих товаров
	
	$("div.products_recomend li.add").live('click', function(){
		var params = new Object();
		params.cat_show_select = $("div.products_recomend select").val();
		productsSelect(params, $(this).parent());
	});
	
	function productsSelect(params, ul, param){
		if (!$("div#products_select").length){
			var $parent = $(ul).parent().parent();
			var cordX = parseInt($parent.offset().left+235);
			var cordY = parseInt($parent.offset().top-140);
			var select;
			if ($("div.select_category").length){
				select = $("div.select_category").html();
			}
			else {
				select = $("div.products_select div.select").html();
			}
			$("body").append('<div id="products_select" style="top:'+cordY+'px; left:'+cordX+'px;"><div class="select_category">'+select+'</div><form class="search_catalog"><input type="text" value="Поиск:" onfocus="if (this.value==\'Поиск:\') this.value=\'\';" onblur="if (this.value==\'\'){this.value=\'Поиск:\'}" class="word_search" autocomplete="off"><input type="submit" class="search" value="Поиск"></form><div class="container"><div id="ajax_loading" style="opacity:0"></div></div><span id="close"></span><i id="bg_top"></i><i id="bg_bottom"></i></div>');
			$("div#products_select").animate({opacity:"1"}, 100);
			$("div#products_select div#ajax_loading").animate({opacity:"1"}, 250);
			$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
				if (data != ""){
					$("div#products_select div.container").html(data).scrollTop(0);
					if ($("div#products_select div.container ul li").length){
						var count = $("div#products_select div.container li.new").length;
						$("div#products_select div.container").attr("data-count", count);
						$parent.find("div.add_product").fadeIn(0);
						imgProductSelectLoader(ul);
						DropProductSelect(ul, param);
						SearchProductSelect(ul, param);
						ScrollProductSelect(ul, param);
					}
					else {
						$("div#products_select div.container").attr("data-count", "0");
					}
					$("div#products_select select").change(function(){
						if ($("div#products_select div.container div#ajax_loading").length){
							return false;
						}
						else {
							$("div#products_select div.container").attr("id", "").attr("data-count", "0").html('<div id="ajax_loading"></div>');
							var current = $(this).val();
							var params = new Object();
							params.cat_show_select = current;
							$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
								if (data != ""){
									$("div#products_select div.container").html(data).scrollTop(0);
									if ($("div#products_select div.container ul li").length){
										var count = $("div#products_select div.container li.new").length;
										$("div#products_select div.container").attr("data-count", count);
										imgProductSelectLoader(ul);
										DropProductSelect(ul, param);
										SearchProductSelect(ul, param);
										ScrollProductSelect(ul, param);
									}
									else {
										$("div#products_select div.container").attr("data-count", "0");
									}
								}
							});
						}
					});
				}
			});
		}
	}
	
	$("div#products_select span#close").live('click', function(){
		$("div#products_select").animate({opacity:"0"}, 100, function(){
			$(this).remove();
		});
		$("div.products_select div.add_product").fadeOut(0);
	});

	$("div.products_select div.add_product").live('click', function(){
		$(this).fadeOut(0);
	});
	
	$("div.products_recomend ul li a.del_p").live('click', function(){
		var id = $(this).parent().attr("data-id");
		var p_id = $("div.products_select ul").attr("data-id");
		$(this).parent().fadeOut(200, function(){
			$(this).remove();
		});	
		var params = new Object();
		params.del_product_rec_id = p_id;
		params.del_product_recomend = id;
		$.post(dirs_catalog+'/products_ajax.cgi', params);
		
		return false;
	});	
	
	function SearchProductSelect(ul, param){
		var $wrapper = $("div#products_select");
		$wrapper.find("input.search").click(function(){
			var el = $(this);
			var word = $wrapper.find("input.word_search").val();
			if (word != "" && word != "Поиск:" && !$wrapper.find("div#ajax_loading").length){
				$(el).addClass("active");
				var $container = $wrapper.find("div.container");
				$container.attr("id", "").attr("data-count", "0").html('<div id="ajax_loading"></div>');
				var params = new Object();
				params.search_product_select = word;
				$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
					if (data != ""){
						$container.html(data).scrollTop(0);
						if ($container.find("li").length){
							var count = $container.find("li.new").length;
							$container.attr("data-count", count);
							imgProductSelectLoader(ul);
							DropProductSelect(ul, param);
						}
						else {
							$container.attr("data-count", "0");
						}
						$(el).removeClass("active");
					}
				});
			}			
			return false;
		});
	}
	
	function ScrollProductSelect(ul, param){
		$("div#products_select div.container").bind('scroll', function() {
			var el = $(this);
			if ($(el).find("ul").height() - ($(el).scrollTop() + $(el).height()) < ($(el).height()*2) && !$("div#products_select div.container div#ajax_loading").length && $(el).attr("id") != "active" && !$(el).find("div.end_result").length){
				$(el).attr("id", "active");
				var count = parseInt($("div#products_select div.container").attr("data-count"));
				var current = $("div#products_select select").val();
				var params = new Object();
				params.cat_show_select = current;
				params.cat_show_select_append = count;
				$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
					if (data != "" && data != "end"){
						$("div#products_select div.container ul div.clear").before(data);
						var count_new = parseInt($("div#products_select div.container li.new").length);
						$("div#products_select div.container").attr("data-count", count+count_new);
						imgProductSelectLoader(ul);
						DropProductSelect(ul, param);
						$(el).attr("id", "");
					}
				});
			}
		});
	}
	
	function DropProductSelect(ul, param){
		$add_product = $(ul).parent().parent().find(".add_product");
		$("div#products_select ul").sortable({
			revert: 200,
			connectWith: $(ul),
			start: function(){
				$add_product.fadeIn(0);
			},	
			stop: function(){
				$add_product.fadeOut(0);
			}
		}).disableSelection();		
		$add_product.droppable({
			accept: "div#products_select li",
			drop: function(event, ui){
				var id = ui.draggable.attr("data-id");
				var p_id = $(ul).attr("data-id");
				var img = ui.draggable.find("img").attr("src");
				var div = $(this);
				$(ul).prepend('<li data-id="'+id+'"><div class="foto"><img src="'+img+'" alt=""></div><a class="del_p" href="#"></a></li>')
				$(ui.draggable).animate({opacity:"0"}, 150, function(){
					$(this).remove();
				});
				var params = new Object();
				if (param == "hits"){
					params.add_product_hits = $(ul).attr("data-param");
					params.add_product_hits_id = id;
					$.post(dirs_catalog+'/products_ajax.cgi', params);
					sortProductHits(ul);			
				}
				else {
					params.add_product_rec_id = p_id;
					params.add_product_recomend = id;
					$.post(dirs_catalog+'/products_ajax.cgi', params);
					SortProductSelect(ul);
				}
			}
		});			
	}
	
	SortProductSelect();
	
	function SortProductSelect(ul){
		var $add = $(ul).find("li.add");
		$(ul).sortable({
			revert: 200,
			cancel: $add,
			stop: function(){
				var p_id = $(ul).attr("data-id");
				var ids="";
				$(ul).find("li").each(function(){
					var el = $(this);
					if ($(el).attr("class") != "add"){
						ids += $(el).attr("data-id")+'|';
					}
				});
				var params = new Object();
				params.resort_product_rec_id = p_id;
				params.resort_product_recomend = ids;
				$.post(dirs_catalog+'/products_ajax.cgi', params);
			}
		}).disableSelection();
	}

	function imgProductSelectLoader(ul){
		if ($("div#products_select ul").length){
			$("div#products_select ul li.new div.foto img").css("opacity", "0");
			$("div#products_select ul li.new div.foto").append("<span></span>");
			var p_id = $(ul).attr("data-id");
			if (p_id > 0){
				$("div#products_select ul li.new[data-id="+p_id+"]").remove();
			}
			$(ul).find("li").each(function(){
				var id = $(this).attr("data-id");
				$("div#products_select ul li.new[data-id="+id+"]").remove();
			});	
			$("div#products_select ul li.new div.foto img").each(function(){
				$(this).load(function(){
					$(this).parent().children("span").remove();
					$(this).css("opacity", "1");
				});
			});
			$("div#products_select div.container li.new").removeClass("new");
		}
	}

	$("a.addMainParam").click(function(){
		var $row = $(this).parent().parent().prev();
		$row.after('<tr><td class="name"><a href="#" class="addMainParam_ p14">Добавить параметр</a></td><td><div class="field_input"><input value="" placeholder="Введите название параметра" autocomplete="off"><i class="del"></i></div></td></tr>');
		var $row = $(this).parent().parent().prev();
		$row.find(".del").click(function(){
			$(this).parent().parent().parent().remove();
		});
		$row.find(".addMainParam_").click(function(){
			var value = $row.find("input").val();
			if (value.length < 2){
				alert("Введите название параметра");
			}
			else {
				$row.replaceWith('<tr><td class="name">'+value+'</td><td><div class="field_input"><input name="fields_main_'+value+'" type="text" value="" placeholder="Введите значение параметра" autocomplete="off"></td></tr>');
				var params = new Object();
				params.add_main_param = value;
				params.param_type = 'string';
				$.post(dirs_catalog+'/products_param_ajax.cgi', params);	
			}
			return false;
		});		
		return false;
	});	
	
	$(".selCategoryParam").change(function(){
		var $select = $(this);
		var value = $select.val();
		if (value > 0){
			var params = new Object();
			params.getRowsParamsUnic = value;
			$.post(dirs_catalog+'/products_param_ajax.cgi', params, function(data){
				if (data){
					if (data == "not"){
						alert("Для выбранной категории уникальных параметров не нашлось");
					}
					if (!$("#addUnicParam-wrapper").length){
						$select.parent().parent().next().before('<tr><td colspan="2"><div id="addUnicParam-wrapper"><table>'+(data != "not"?data:'<tr></tr>')+'<tr><td class="name"></td><td><a class="add-param addUnicParam" href="#">Добавить уникальный параметр</a></td></tr></table></div></td></tr>');
					}
					else {
						$("#addUnicParam-wrapper").html('<table>'+(data != "not"?data:'<tr></tr>')+'<tr><td class="name"></td><td><a class="add-param addUnicParam" href="#">Добавить уникальный параметр</a></td></tr></table>');
					}
					$(".addUnicParam").click(function(){
						addUnicParam(this);
						return false;
					});
				}
			});
		}
	});
	
	$(".addUnicParam").click(function(){
		addUnicParam(this);
		return false;
	});
	
	function addUnicParam(add){
		var $row = $(add).parent().parent().prev();
		$row.after('<tr><td class="name"><a href="#" class="addUnicParam_ p14">Добавить параметр</a></td><td><div class="field_input"><input value="" placeholder="Введите название параметра" autocomplete="off"><i class="del"></i></div></td></tr>');
		var $row = $(add).parent().parent().prev();
		$row.find(".del").click(function(){
			$(this).parent().parent().parent().remove();
		});
		$row.find(".addUnicParam_").click(function(){
			var value = $row.find("input").val();
			var cat_id = $(".selCategoryParam").val();
			if (value.length < 2){
				alert("Введите название параметра");
			}
			else if (!cat_id){
				alert("Выберите категорию параметра");
			}
			else {
				$row.replaceWith('<tr><td class="name">'+value+'</td><td><div class="field_input"><input name="fields_unic_'+value+'" type="text" value="" placeholder="Введите значение параметра" autocomplete="off"></td></tr>');
				var params = new Object();
				params.add_main_param = value;
				params.param_cat_id = cat_id;
				params.param_type = 'string';
				$.post(dirs_catalog+'/products_param_ajax.cgi', params);
			}
			return false;
		});		
	}

	$("div.save_content div.cb").live('click', function() {
		var el = $(this);
		if ($(el).attr("class") == "cb checked") {$("div.save_content input.button.save").replaceWith('<a class="ajaxSave" href="#">Сохранить</a>');}
		else {$("div.save_content a.ajaxSave").replaceWith('<input type="submit" name="save" value="Сохранить" class="button save" />');}
	});
	
		var ajaxSave = function(){
			var ed1=""; var ed2="";
			if ($("textarea#elm1").length){
				ed1 = tinyMCE.get('elm1');
				ed1.setProgressState(1);
				window.setTimeout(function(){ed1.setProgressState(0);}, 500);
			}		
			if ($("textarea#elm1_sm").length){
				ed2 = tinyMCE.get('elm1_sm');
				ed2.setProgressState(1);
				window.setTimeout(function(){ed2.setProgressState(0);}, 500);
			}
		} 
		
		$("a.ajaxSave").live('click', function() {
			ajaxSave();			
			var ed1=""; var content1="";
			var ed2=""; var content2="";
			var product_id = $("a.preview_page").attr("id");
			if ($("textarea#elm1").length){
				ed1 = tinyMCE.get('elm1');
				content1 = ed1.getContent();
				if (content1 == "" && product_id != ""){content1 = "clear";}
			}		
			if ($("textarea#elm1_sm").length){
				ed2 = tinyMCE.get('elm1_sm');
				content2 = ed2.getContent();
				if (content2 == "" && product_id != ""){content2 = "clear";}
			}
			var content_lite = $("textarea.lite_desc").val();
			if (content_lite == "" && product_id != ""){content_lite = "clear";}
			var params = new Object();
			params.product_id = product_id;
			params.product_content1 = content1;
			params.product_content2 = content2;
			params.product_content_lite = content_lite;
			$.post(dirs_catalog+'/products_ajax.cgi', params);
			return false;
		});
		
	if ($("#products_reviews_send").length){
		var $rait = $("#products_reviews_send").find(".raiting_star");
		$rait.hover(function(){
			$(this).children(".raiting_hover").show(0);
			$(this).children(".raiting_votes").hide(0);
		},
		function(){
			$(this).children(".raiting_hover").hide(0);
			$(this).children(".raiting_votes").show(0);
		});
		$rait.mousemove(function(e){
			var margin = $(this).offset();
			var width_votes = e.pageX - margin.left;
			if (width_votes == 0) {width_votes = 1;}
			var user_votes = Math.ceil(width_votes/29);  
			$(this).children(".raiting_hover").width(user_votes*29);
		});
		$rait.live("click", function(){
			var votes = Math.ceil($(this).children(".raiting_hover").width()/29); 
			var star_width = votes*29;
			$(this).children(".raiting_hover").hide();				
			$(this).children(".raiting_votes").width(star_width).show(0);
			$rait.attr("data-raiting", votes);
		});
		$("#products_reviews_send").find(".send").find(".button").live("click", function(){
			var raiting = $rait.attr("data-raiting");
			var name = $("#products_reviews_send").find("input[name=name]").val();
			var text = $("#products_reviews_send").find("textarea").val();
			if (raiting < 1 || raiting == ""){alert("Поставьте оценку товару");}
			else if (text.length < 5){alert("Оставьте комментарий");}
			else if (name.length < 2){alert("Укажите Имя");}
			else {
				var params = new Object();
				params.reviews_raiting_id = $("#products_reviews_send").find(".raiting_star").attr("data-id");
				params.reviews_raiting = raiting;
				params.reviews_raiting_name = name;
				params.reviews_raiting_text = text;
				$.post(dirs_catalog+'/products_ajax.cgi', params, function(data){
					if (data > 0){
						$("#products_reviews_container").find(".item:first").attr("data-id", data).find("span.date").after('<i title="Редактировать отзыв" class="edit_review fa fa-pencil"></i><i title="Удалить отзыв" class="delete_review fa fa-times"></i>');
					}
				});
				$("#products_reviews_container").find("p.note").remove();
				$("#products_reviews_container").prepend('<div style="display:none" class="item"><div class="name"><span>'+name+'</span><div class="raiting_star"><div class="raiting_blank"></div><div class="raiting_votes" style="width:'+(raiting*19)+'px;"></div></div><span class="date">'+DateNow(".")+' в '+getTimeHM()+'</span></div><div class="comments">'+text+'</div></div>');
				$("#products_reviews_send").fadeOut(200).before('<a href="#" class="add_show_reviews">Отзыв добавлен</a>');
				setTimeout(function(){
					$("#products_reviews_container").find(".item:first").fadeIn(400);
					setTimeout(function(){
						$(".add_show_reviews").text("Добавить отзыв");
						$("#products_reviews_send").find(".raiting_hover").attr("style", "");
						$("#products_reviews_send").find(".raiting_votes").attr("style", "");
						$("#products_reviews_send").find("input[name=name]").val("");
						$("#products_reviews_send").find("textarea").val("");
					}, 1000);
				}, 400);
			}
		});
		
		$(".add_show_reviews").live("click", function(){
			$(this).next().fadeIn(0);
			$(this).remove();
			return false;
		});
		
		$(".show_reviews").click(function(){
			$("#products_reviews_container").find(".item").fadeIn(150);
			$(this).remove();
			return false;
		});	

		$(".public_review").click(function(){
			var $item = $(this).parent().parent();
			var v_id = $item.attr("data-id");
			var params = new Object();
			params.reviews_public_id = v_id;
			$.post(dirs_catalog+'/products_ajax.cgi', params);
			$item.css("display", "block").removeClass("no_public");
			$(this).remove();
			return false;
		});
		
		$(".edit_review").live("click", function(){
			var $item = $(this).parent().parent();
			var text = $item.find(".comments").html();
			text = text.replace(/^\s+/g, "");
			text = text.replace(/\s+$/g, "");
			text = text.replace(/\s+/g, " ");
			text = text.replace(/<br>/g, "\n");
			var height = $item.find(".comments").height();
			if ($item.find(".public_review").length){
				$item.find(".public_review").css("right", "225px");
			}
			$item.addClass("edit").find(".comments").replaceWith('<textarea class="comments" style="height:'+height+'px">'+text+'</textarea>');
			$(this).attr("class", "save_review").text('Сохранить').attr("title", "Сохранить изменения");
			$item.find(".comments").focus();
		});	

		$(".save_review").live("click", function(){
			var $item = $(this).parent().parent();
			var v_id = $item.attr("data-id");
			var text = $item.find(".comments").val();
			var params = new Object();
			params.reviews_edit_id = v_id;
			params.reviews_edit_text = text;
			$.post(dirs_catalog+'/products_ajax.cgi', params);
			text = text.replace(/\r\n|\r|\n/g, "<br>");
			if ($item.find(".public_review").length){
				$item.find(".public_review").css("right", "172px");
			}			
			$item.removeClass("edit").find(".comments").replaceWith('<div class="comments">'+text+'</div>');
			$(this).attr("class", "edit_review fa fa-pencil").html("").attr("title", "Редактировать отзыв");
		});			
		
		$(".delete_review").live("click", function(){
			var $item = $(this).parent().parent();
			if (confirm('Отзыв будет удален?')) {
				var v_id = $item.attr("data-id");
				var params = new Object();
				params.reviews_delete_id = v_id;
				$.post(dirs_catalog+'/products_ajax.cgi', params);
				$item.fadeOut(200, function(){
					$(this).remove();
				});
			}
			else {
				return false;
			}
		});		
	}
	
	function DateNow(prefix) {
		if (!prefix){prefix = "-";}
		var d = new Date();
		var day = d.getDate(); if (day < 10){day = "0"+day;}
		var month = d.getMonth()+1; if (month < 10){month = "0"+month;}
		var date = d.getFullYear()+prefix+month+prefix+day;
		return date;
	}	

	function getTimeHM(){
		var d=new Date();
		var time_hours=d.getHours();
		var time_min=d.getMinutes();
		time_wr=((time_hours<10)?"0":"")+time_hours;
		time_wr+=":";
		time_wr+=((time_min<10)?"0":"")+time_min;
		return time_wr;
	}	

});
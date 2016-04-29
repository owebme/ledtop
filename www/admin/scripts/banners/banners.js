$(document).ready(function(){

	function draggableObject(){
		if ($("div.banner_container div.jSboxBanner-text1").length){
			$("div.banner_container div.jSboxBanner-text1").draggable({
				drag: function(){
					if ($("div.banner_container div.jSboxBanner-text1_bg").length){
						$("div.banner_container div.jSboxBanner-text1_bg").css("top", $(this).position().top+"px");
					}
				},
				stop: function(){
					$("div#banners input[name=text1_cordX]").attr("value", $(this).position().left);
					$("div#banners input[name=text1_cordY]").attr("value", $(this).position().top);
				}
			});
		}
		if ($("div.banner_container div.jSboxBanner-text2").length){
			$("div.banner_container div.jSboxBanner-text2").draggable({
				drag: function(){
					if ($("div.banner_container div.jSboxBanner-text2_bg").length){
						$("div.banner_container div.jSboxBanner-text2_bg").css("top", $(this).position().top+"px");
					}
				},
				stop: function(){
					$("div#banners input[name=text2_cordX]").attr("value", $(this).position().left);
					$("div#banners input[name=text2_cordY]").attr("value", $(this).position().top);
				}
			});
		}
		if ($("div.banner_container div.jSboxBanner-text3").length){
			$("div.banner_container div.jSboxBanner-text3").draggable({
				drag: function(){
					if ($("div.banner_container div.jSboxBanner-text3_bg").length){
						$("div.banner_container div.jSboxBanner-text3_bg").css("top", $(this).position().top+"px");
					}
				},
				stop: function(){
					$("div#banners input[name=text3_cordX]").attr("value", $(this).position().left);
					$("div#banners input[name=text3_cordY]").attr("value", $(this).position().top);
				}
			});
		}	
		if ($("div.banner_container img.jSboxBanner-img1").length){
			$("div.banner_container img.jSboxBanner-img1").draggable({
				stop: function(){
					$("div#banners input[name=img1_cordX]").attr("value", $(this).position().left);
					$("div#banners input[name=img1_cordY]").attr("value", $(this).position().top);
				}
			});
		}
		if ($("div.banner_container img.jSboxBanner-img2").length){
			$("div.banner_container img.jSboxBanner-img2").draggable({
				stop: function(){
					$("div#banners input[name=img2_cordX]").attr("value", $(this).position().left);
					$("div#banners input[name=img2_cordY]").attr("value", $(this).position().top);
				}
			});
		}
	}
	draggableObject();

	$("div.btn-group a.btn").live("click", function(){
		$("div#content").css("overflow", "visible");
	});
	$("div.btn-group ul li a").live("click", function(){
		$("div#content").css("overflow", "hidden");
	});
	
	
	// Поиск изображений
	
	$("div.search-library input#search").live("click", function(){
		var word = $("div.search-library input#word_search").val();
		searchImages(word);
		return false;
	});	
	
	$("div.search-library div.example a").live("click", function(){
		var word = $(this).html();
		$("div.search-library input#word_search").attr("value", word);
		searchImages(word);
		return false;
	});	
	
	function searchImages(word){
		if (word != ""){
			$("div.search-library ul li").removeClass("active");
			var height = $("div.images-library").height();
			$("div.images-library").empty().css("height", height+"px").append('<div class="ajax"></div>');
			var params = new Object();
			params.search_word = word;
			params.search_page = "1";
			params.search_type = "bg";
			$.post('/cgi-bin/admin/modules/banners_ajax.cgi', params, function(data){
				if (data != ""){
					$("div.images-library div.ajax").replaceWith(data);
					$("div.images-library").append('<div class="clear"></div><span id="search" class="more bg" data-page="2">Еще результаты...</span>');
					$("div.images-library").css("height", "auto");
				}
				else if (data == ""){
					$("div.images-library div.ajax").replaceWith('<p class="message">Попробуйте упростить поисковый запрос.</p>');
				}
			});	
		}
		else {
			alert("Введите слово для поиска");
			return false;
		}
	}
	
	// Продолжить поиск изображений
	
	$("div.images-library span.more#search").live("click", function(){
		var el = $(this);
		var cl = $(this).attr("class");
		if ($(el).html() != "<em></em>"){
			var word = $("div.search-library input#word_search").val();
			var page = parseInt($(el).attr("data-page"));
			var type = cl.replace(/more\ /g,'');
			$(el).html('<em></em>');
			var params = new Object();
			params.search_word = word;
			params.search_page = page;
			params.search_type = type;
			$.post('/cgi-bin/admin/modules/banners_ajax.cgi', params, function(data){
				if (data != ""){
					$("div.images-library div.clear").remove();
					$("div.images-library span.more").replaceWith(data);
					$("div.images-library").append('<div class="clear"></div><span id="search" class="more '+type+'" data-page="'+(page+1)+'">Еще результаты...</span>');
				}
			});
		}
	});	
	
	
	// Вызвать библиотеку изображений
	
	$("table.banners-img div.img div.foto").live("click", function(){
		loadLibrary($(this));
	});
	
	$("div.search-library ul li.library a").live("click", function(){
		if ($(this).parent().attr("class") != "library active"){
			$("div.search-library div.search input#word_search").attr("value", "");
			$("div.images-library").remove();
			loadLibrary($("table.banners-img div.img div.foto.active"), "load");
			$(this).parent().addClass("active");
		}
		return false;
	});
	
	function loadLibrary(elem, action){
		var el = $(elem);
		var cl = $(el).attr("class");
		if (action == "load"){cl = cl.replace(/\ active/g,'');}
		var check="";
		if (!$("div.search-library").length){
			$("table.banners-img").after('<div class="search-library">'+(cl == "foto bg"?'<div class="search"><form><input placeholder="Поиск:" type="text" value="" id="word_search" autocomplete="off"><input type="submit" id="search" value=""></form></div><div class="example">Например: <a href="#">весна</a>, <a href="#">оранжевый</a>, <a href="#">зеленый</a></div>':'')+'<ul class="nav nav-pills"><li class="library active"><a href="#">Библиотека</a></li><li class="file"><a href="#">Загрузить</a></li><input title="Загрузить файл" type="file" class="file" value=""></ul><a class="close" href="#">Скрыть</a></div>');
			$("div.search-library input.file").unbind();
			$("div.search-library input.file").bind({
				change: function() {
					addImgOne(this.files, this);
				}
			});
		}
		if ($("table.banners-img div.img div.foto.active").length){
			check = $("table.banners-img div.img div.foto.active").attr("class"); 
			check = check.replace(/\ active/g,'');
		}
		else {check = cl;}
		if ($(el).attr("class") != "foto active" && $(el).attr("class") != "foto bg active" || action == "load"){
			$("table.banners-img div.img div.foto").removeClass("active");
			$(el).addClass("active");
			if ($("div.images-library div.item.active").length){
				$("div.images-library div.item").removeClass("active");
			}
			var type="";
			if (cl == "foto"){type = "img";}
			else if (cl == "foto bg"){type = "bg";}
			if (!$("div.images-library").length || cl != check || action == "load"){
				var height="";
				if ($("div.images-library").length){
					height = parseInt($("div.images-library").height());
					$("div.search-library div.search input#word_search").attr("value", "");
					$("div.images-library").css("height", height+"px").html('<div class="ajax"></div>');
					if (type == "bg" && check == "foto"){
						$("div.search-library").prepend('<div class="search"><form><input placeholder="Поиск:" type="text" value="" id="word_search" autocomplete="off"><input type="submit" id="search" value=""></form></div><div class="example">Например: <a href="#">весна</a>, <a href="#">оранжевый</a>, <a href="#">зеленый</a></div>');
					}
					else {
						$("div.search-library div.search").remove();
						$("div.search-library div.example").remove();
					}
				}
				else {
					$("div.search-library").after('<div class="images-library"><div class="ajax"></div></div>');
					$("div.images-library").animate({"height": "168px"}, 400);
				}
				$("div.search-library ul li.library").addClass("active");
				var params = new Object();
				params.lib_images = type;
				params.lib_images_from = "0";
				$.post('/cgi-bin/admin/modules/banners_ajax.cgi', params, function(data){
					if (data != "" && data != "end"){
						$("div.images-library div.ajax").replaceWith(data);
						$("div.images-library").stop(true, true).css("height", "auto");
					}
					else if (data == "end"){
						$("div.images-library div.ajax").remove();
					}
				});
			}
		}
	}
	
	// Продолжить показ изображений
	
	$("div.images-library span.more#lib").live("click", function(){
		var el = $(this);
		var cl = $(this).attr("class");
		if ($(el).html() != "<em></em>"){
			var type = cl.replace(/more\ /g,'');
			$(el).html('<em></em>');
			var params = new Object();
			params.lib_images = type;
			params.lib_images_from = $(el).attr("data-from");
			$.post('/cgi-bin/admin/modules/banners_ajax.cgi', params, function(data){
				if (data != ""){
					$("div.images-library div.clear").remove();
					if (data == "end"){
						$("div.images-library span.more").replaceWith('<div class="clear"></div>');
					} else {
						$("div.images-library span.more").replaceWith(data);
					}
					if (!$("div.images-library span.more").length){
						$("div.images-library").append('<div class="clear"></div>');
					}
				}
			});
		}
	});
	
	// Выбрать изображение из библиотеки
	
	$("div.images-library div.item").live("click", function(){
		var el = $(this);
		if ($(el).attr("class") != "active"){
			$("div.images-library div.item").removeClass("active");
			$(el).addClass("active");
			$("table.banners-img div.img div.foto.active").html('<div class="ajax"></div>');
			uploadImage(el);
		}
	});
	
	$("div.search-library ul input").live("mouseover mouseout", function(e){
		var el = $(this);
		if (e.type == "mouseover"){
			$(el).prev("li").addClass("hover");
			
		} else if (e.type == "mouseout"){
			$(el).prev("li").removeClass("hover");
		}
	});		
	
	function addImgOne(files, el) {
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
				$("table.banners-img div.img div.foto.active").html('<div class="ajax"></div>');
				var img = $('<img class="paste"/>');
				$("table.banners-img div.img div.foto.active").prepend(img);
				img.get(0).file = file;
				
				var reader = new FileReader();
				reader.onload = (function(aImg) {
					return function(e) {
						aImg.attr('src', e.target.result);
					};
				})(img);
				
				reader.readAsDataURL(file);
			}
		});
		
		setTimeout(function(){
			uploadImage($("table.banners-img div.img div.foto.active"));
		}, 200);
	}	
	
	function uploadImage(el) {
		var type = $("table.banners-img div.img div.foto.active").parent().attr("data-img");
		var params = new Object();
		params.banner_name = $("div.banner_container div.banner").attr("id");
		params.add_images = $(el).find("img").attr("src");
		params.add_images_type = type;
		$.post('/cgi-bin/admin/modules/banners_ajax.cgi', params, function(data){
			if (data != ""){
				if (type == "bg"){
					$("table.banners-img div.img div.foto.active").empty().append('<div title="Сменить фон" class="bg" style="background:url('+data+') 100% 100% repeat;"></div><a class="del" href="#" title="Удалить фон">');
				}
				else {
					$("table.banners-img div.img div.foto.active").empty().append('<img title="Сменить картинку" src="'+data+'" alt=""><a class="del" href="#" title="Удалить картинку"></a>');
				}
				$("table.banners-img input[name="+type+"]").attr("value", data);
				if (type == "bg"){
					if ($("div.banner_container div.banner div.jSboxBanner-"+type).length){
						$("div.banner_container div.banner div.jSboxBanner-"+type).css("background", "url("+data+") 100% 100% repeat");
						addButtonSave();
					}
				}
				else {
					if ($("div.banner_container div.banner img.jSboxBanner-"+type).length){
						$("div.banner_container div.banner img.jSboxBanner-"+type).attr("src", data);
						addButtonSave();
					}
				}
			}
		});	
	}
	
	// Скрыть библиотеку
	
	$("div.search-library a.close").live("click", function(){
		$("table.banners-img div.img div.foto").removeClass("active");
		$("div.search-library").animate({"height": "0px"}, 400, function(){
			$(this).remove();
		});
		$("div.images-library").animate({"height": "0px"}, 400, function(){
			$(this).remove();
		});
		return false;
	});	
	
	// Предпросмотр баннера
	
	$("div#banners input.button.create").live("click", function(){
		createBanner();
		draggableObject();
		addButtonSave();
	});	
	
	function addButtonSave(){
		if (!$("div.banner_container div.save").length){
			var left = parseInt($("div.banner_container div.roulette-height").position().left);
			var width = parseInt($("div.banner_container div.roulette-width input").val());
			var bottom="";
			if (width < 280){bottom = "81";} else {bottom = "46";}
			$("div.banner_container div.save").remove();
			$("div.banner_container").append('<div class="save" style="left:'+(left-134)+'px; bottom:-'+bottom+'px"><input type="button" class="button" value="Сохранить"></div>');
			$("div.banner_container div.save").fadeIn(200);
		}
	}
	
	// Удалить изображение
	
	$("table.banners-img div.foto a.del").live("click", function(){
		var el = $(this).parent();
		var type = $(this).parent().parent().attr("data-img");
		if (type == "bg"){
			$(el).html('<span><em>Добавить фон</em></span>');
		}
		else {
			$(el).html('<span><em>Добавить картинку</em></span>');
		}
		$("table.banners-img input[name="+type+"]").attr("value", "")
		createBanner("save");
		return false;
	});	
	
	// Сброс настроек
	
	$("div#banners input.button.reset").live("click", function(){
		if (confirm('Сбросить параметры?')) {
			$("table.banners-img a.img1_speed span.value").html('1.2 сек');
			$("table.banners-img a.img2_speed span.value").html('2.4 сек');
			$("table.banners-img input[name=link]").attr("value", "");
			$("table.banners-text input[name=text_1]").attr("value", "");
			$("table.banners-text input[name=text_2]").attr("value", "");
			$("table.banners-text input[name=text_3]").attr("value", "");
			$("table.banners-text tr.fields_text1 div#choice-size span.value").html('28px');
			$("table.banners-text tr.fields_text2 div#choice-size span.value").html('18px');
			$("table.banners-text tr.fields_text3 div#choice-size span.value").html('60px');
			$("table.banners-text tr.fields_text1 div#choice-font span.value").html('Calibri');
			$("table.banners-text tr.fields_text2 div#choice-font span.value").html('Tahoma');
			$("table.banners-text tr.fields_text3 div#choice-font span.value").html('Magistral');
			$("table.banners-text a.mask").removeClass("active");
			$("table.banners-text div.mask").removeClass("active");
			$("table.banners-text input.color").attr("value", "#ffffff").attr("style", "");
			$("table.banners-text div#choice-opacity span.value").html('100%');
			$("table.banners-text div#choice-style button").removeClass("active");
			$("table.banners-text div#choice-style button[name=shadow]").addClass("active");
			$("div#banners div.repeat span.value").html('7 сек');
			$("div#banners div.choice-border div.js-box").addClass("checked");
			$("div.banner_container div.banner div.jSboxBanner-text1").empty().css({"color": "#ffffff", "font-size": "28px", "line-height": "28px", "font-family": "Calibri"});
			$("div.banner_container div.banner div.jSboxBanner-text2").empty().css({"color": "#ffffff", "font-size": "18px", "line-height": "18px", "font-family": "Tahoma"});
			$("div.banner_container div.banner div.jSboxBanner-text3").empty().css({"color": "#ffffff", "font-size": "60px", "line-height": "60px", "font-family": "Magistral"});
			$("div.banner_container div.banner div.jSboxBanner-text1_bg").remove();
			$("div.banner_container div.banner div.jSboxBanner-text2_bg").remove();
			$("div.banner_container div.banner div.jSboxBanner-text3_bg").remove();
			addButtonSave();
			
		} else {
			return false;
		}
	});		

	// Cохранение настроек
	
	$("div.banner_container div.save input.button").live("click", function(){
		$("div.banner_container").append('<div class="banner-save"></div>');
		$("div.banner_container div.save").append('<div class="ajax">Сохранение...</div>');
		$("div.banner_container div.save div.ajax").fadeIn(250);
		createBanner("save");
	});
	
	function createBanner(type){
		var img = $("table.banners-img");
		var text = $("table.banners-text");
		var banner = $("div.banner_container div.banner");
		var width = $("div.banner_container").find("input[name=width]").val();
		var height = $("div.banner_container").find("input[name=height]").val();
		var link = "no_mask";
		var mode="";
		if (type == "save"){
			banner = $("div.banner_container div.banner-save");
			link = $(img).find("input[name=link]").val();
			mode = "static";
		}
		var img1 = $(img).find("input[name=img1]").val();
		var img2 = $(img).find("input[name=img2]").val();
		var repeat = $("div.repeat div.btn-group span.value").html();
		if (repeat == "откл. анимацию"){repeat = "off";}
		else if (repeat == "без повтора"){repeat = 0;}
		else {repeat = repeat.replace(/\ сек/g,''); repeat = repeat*1000;}
		if (type != "save"){repeat = 0;}
		var border = false;
		if ($("div.choice-border div.js-box.checked").length){border = true;}
		var img1_speed = $(img).find("a.img1_speed").find("span.value").html();
		img1_speed = img1_speed.replace(/\ сек/g,''); img1_speed = img1_speed*1000;
		var img2_speed = $(img).find("a.img2_speed").find("span.value").html();
		img2_speed = img2_speed.replace(/\ сек/g,''); img2_speed = img2_speed*1000;
		var bg = $(img).find("input[name=bg]").val();
		var text1 = $(text).find("input[name=text_1]").val().trim();
		var text2 = $(text).find("input[name=text_2]").val().trim();
		var text3 = $(text).find("input[name=text_3]").val().trim();
		
		var text1_size = $(text).find("tr.fields_text1").find("div#choice-size").find("span.value").html();
		text1_size = text1_size.replace(/px/g,'');
		var text1_font = $(text).find("tr.fields_text1").find("div#choice-font").find("span.value").html();
		var text1_color = "#"+$(text).find("tr.fields_text1").find("input[name=text1_color]").val();
		var text1_opacity = $(text).find("tr.fields_text1").find("div#choice-opacity").find("span.value").html();
		text1_opacity = text1_opacity.replace(/%/g,''); text1_opacity = text1_opacity/100;
		var text1_bold = false;
		if ($(text).find("tr.fields_text1").find("div#choice-style").find("button[name=bold].btn.active").length){text1_bold = true;}
		var text1_italic = false;
		if ($(text).find("tr.fields_text1").find("div#choice-style").find("button[name=italic].btn.active").length){text1_italic = true;}		
		var text1_underline = false;
		if ($(text).find("tr.fields_text1").find("div#choice-style").find("button[name=underline].btn.active").length){text1_underline = true;}	
		var text1_shadow = false;
		if ($(text).find("tr.fields_text1").find("div#choice-style").find("button[name=shadow].btn.active").length){text1_shadow = true;}	
		var text1_blink = false;
		if ($(text).find("tr.fields_text1").find("div#choice-style").find("button[name=blink].btn.active").length){text1_blink = true;}	
		var text1_bg=""; var text1_bg_opacity="";
		if ($(text).find("tr.fields_text1").find("a.mask.active").length){
			text1_bg = "#"+$(text).find("tr.fields_text1").find("input[name=text1_color_mask]").val();
			text1_bg_opacity = $(text).find("tr.fields_text1").find("div#choice-opacity-mask").find("span.value").html();
			text1_bg_opacity = text1_bg_opacity.replace(/%/g,''); text1_bg_opacity = text1_bg_opacity/100;
		}
		
		var text2_size = $(text).find("tr.fields_text2").find("div#choice-size").find("span.value").html();
		text2_size = text2_size.replace(/px/g,'');
		var text2_font = $(text).find("tr.fields_text2").find("div#choice-font").find("span.value").html();
		var text2_color = "#"+$(text).find("tr.fields_text2").find("input[name=text2_color]").val();		
		var text2_opacity = $(text).find("tr.fields_text2").find("div#choice-opacity").find("span.value").html();
		text2_opacity = text2_opacity.replace(/%/g,''); text2_opacity = text2_opacity/100;
		var text2_bold = false;
		if ($(text).find("tr.fields_text2").find("div#choice-style").find("button[name=bold].btn.active").length){text2_bold = true;}
		var text2_italic = false;
		if ($(text).find("tr.fields_text2").find("div#choice-style").find("button[name=italic].btn.active").length){text2_italic = true;}		
		var text2_underline = false;
		if ($(text).find("tr.fields_text2").find("div#choice-style").find("button[name=underline].btn.active").length){text2_underline = true;}	
		var text2_shadow = false;
		if ($(text).find("tr.fields_text2").find("div#choice-style").find("button[name=shadow].btn.active").length){text2_shadow = true;}	
		var text2_blink = false;
		if ($(text).find("tr.fields_text2").find("div#choice-style").find("button[name=blink].btn.active").length){text2_blink = true;}	
		var text2_bg=""; var text2_bg_opacity="";
		if ($(text).find("tr.fields_text2").find("a.mask.active").length){
			text2_bg = "#"+$(text).find("tr.fields_text2").find("input[name=text2_color_mask]").val();
			text2_bg_opacity = $(text).find("tr.fields_text2").find("div#choice-opacity-mask").find("span.value").html();
			text2_bg_opacity = text2_bg_opacity.replace(/%/g,''); text2_bg_opacity = text2_bg_opacity/100;
		}

		var text3_size = $(text).find("tr.fields_text3").find("div#choice-size").find("span.value").html();
		text3_size = text3_size.replace(/px/g,'');
		var text3_font = $(text).find("tr.fields_text3").find("div#choice-font").find("span.value").html();
		var text3_color = "#"+$(text).find("tr.fields_text3").find("input[name=text3_color]").val();
		var text3_opacity = $(text).find("tr.fields_text3").find("div#choice-opacity").find("span.value").html();
		text3_opacity = text3_opacity.replace(/%/g,''); text3_opacity = text3_opacity/100;
		var text3_bold = false;
		if ($(text).find("tr.fields_text3").find("div#choice-style").find("button[name=bold].btn.active").length){text3_bold = true;}
		var text3_italic = false;
		if ($(text).find("tr.fields_text3").find("div#choice-style").find("button[name=italic].btn.active").length){text3_italic = true;}		
		var text3_underline = false;
		if ($(text).find("tr.fields_text3").find("div#choice-style").find("button[name=underline].btn.active").length){text3_underline = true;}	
		var text3_shadow = false;
		if ($(text).find("tr.fields_text3").find("div#choice-style").find("button[name=shadow].btn.active").length){text3_shadow = true;}	
		var text3_blink = false;
		if ($(text).find("tr.fields_text3").find("div#choice-style").find("button[name=blink].btn.active").length){text3_blink = true;}	
		var text3_bg=""; var text3_bg_opacity="";
		if ($(text).find("tr.fields_text3").find("a.mask.active").length){
			text3_bg = "#"+$(text).find("tr.fields_text3").find("input[name=text3_color_mask]").val();
			text3_bg_opacity = $(text).find("tr.fields_text3").find("div#choice-opacity-mask").find("span.value").html();
			text3_bg_opacity = text3_bg_opacity.replace(/%/g,''); text3_bg_opacity = text3_bg_opacity/100;
		}	
		
		var text1_cordX = $("div#banners").find("input[name=text1_cordX]").val();
		var text1_cordY = $("div#banners").find("input[name=text1_cordY]").val();
		var text2_cordX = $("div#banners").find("input[name=text2_cordX]").val();
		var text2_cordY = $("div#banners").find("input[name=text2_cordY]").val();
		var text3_cordX = $("div#banners").find("input[name=text3_cordX]").val();
		var text3_cordY = $("div#banners").find("input[name=text3_cordY]").val();
		var img1_cordX = $("div#banners").find("input[name=img1_cordX]").val();
		var img1_cordY = $("div#banners").find("input[name=img1_cordY]").val();
		var img2_cordX = $("div#banners").find("input[name=img2_cordX]").val();
		var img2_cordY = $("div#banners").find("input[name=img2_cordY]").val();
		
		$(banner).jSboxBanner({
			mode: mode,
			width: width,
			height: height,
			repeat: repeat,
			border: border,
			link: link,
			img1: img1,
			img2: img2,
			img1_speed: img1_speed,
			img2_speed: img2_speed,
			bg: bg,
			text1: text1,
			text2: text2,
			text3: text3,
			text1_size: text1_size,
			text1_font: text1_font,
			text1_color: text1_color,
			text1_opacity: text1_opacity,
			text1_bold: text1_bold,
			text1_italic: text1_italic,
			text1_underline: text1_underline,
			text1_shadow: text1_shadow,
			text1_blink: text1_blink,
			text1_bg: text1_bg,
			text1_bg_opacity: text1_bg_opacity,
			text2_size: text2_size,
			text2_font: text2_font,
			text2_color: text2_color,
			text2_opacity: text2_opacity,
			text2_bold: text2_bold,
			text2_italic: text2_italic,
			text2_underline: text2_underline,
			text2_shadow: text2_shadow,
			text2_blink: text2_blink,
			text2_bg: text2_bg,
			text2_bg_opacity: text2_bg_opacity,
			text3_size: text3_size,
			text3_font: text3_font,
			text3_color: text3_color,
			text3_opacity: text3_opacity,
			text3_bold: text3_bold,
			text3_italic: text3_italic,
			text3_underline: text3_underline,
			text3_shadow: text3_shadow,
			text3_blink: text3_blink,
			text3_bg: text3_bg,
			text3_bg_opacity: text3_bg_opacity,
			text1_cordX: text1_cordX,
			text1_cordY: text1_cordY,
			text2_cordX: text2_cordX,
			text2_cordY: text2_cordY,
			text3_cordX: text3_cordX,
			text3_cordY: text3_cordY,
			img1_cordX: img1_cordX,
			img1_cordY: img1_cordY,
			img2_cordX: img2_cordX,
			img2_cordY: img2_cordY		
		});			
		if (type == "save"){
			setTimeout(function(){
				var params = new Object();
				params.banner_name = $("div.banner_container div.banner").attr("id");
				params.banner_body = $(banner).html();
				params.banner_width = width;
				params.banner_height = height;
				params.banner_border = border;
				params.banner_repeat = repeat;
				params.link = link;
				params.img1 = img1;
				params.img2 = img2;
				params.img1_speed = img1_speed;
				params.img2_speed = img2_speed;
				params.bg = bg;
				params.text1 = text1;
				params.text2 = text2;
				params.text3 = text3;
				params.text1_size = text1_size;
				params.text1_font = text1_font;
				params.text1_color = text1_color;
				params.text1_opacity = text1_opacity;
				params.text1_bold = text1_bold;
				params.text1_italic = text1_italic;
				params.text1_underline = text1_underline;
				params.text1_shadow = text1_shadow;
				params.text1_blink = text1_blink;
				params.text1_bg = text1_bg;
				params.text1_bg_opacity = text1_bg_opacity;
				params.text2_size = text2_size;
				params.text2_font = text2_font;
				params.text2_color = text2_color;
				params.text2_opacity = text2_opacity;
				params.text2_bold = text2_bold;
				params.text2_italic = text2_italic;
				params.text2_underline = text2_underline;
				params.text2_shadow = text2_shadow;
				params.text2_blink = text2_blink;
				params.text2_bg = text2_bg;
				params.text2_bg_opacity = text2_bg_opacity;
				params.text3_size = text3_size;
				params.text3_font = text3_font;
				params.text3_color = text3_color;
				params.text3_opacity = text3_opacity;
				params.text3_bold = text3_bold;
				params.text3_italic = text3_italic;
				params.text3_underline = text3_underline;
				params.text3_shadow = text3_shadow;
				params.text3_blink = text3_blink;
				params.text3_bg = text3_bg;
				params.text3_bg_opacity = text3_bg_opacity;
				params.text1_cordX = text1_cordX;
				params.text1_cordY = text1_cordY;
				params.text2_cordX = text2_cordX;
				params.text2_cordY = text2_cordY;
				params.text3_cordX = text3_cordX;
				params.text3_cordY = text3_cordY;
				params.img1_cordX = img1_cordX;
				params.img1_cordY = img1_cordY;
				params.img2_cordX = img2_cordX;
				params.img2_cordY = img2_cordY;				
				$(banner).remove();
				$.post('/cgi-bin/admin/modules/banners_ajax.cgi', params, function(data){
					if (data == "ok"){
						$("div.banner_container div.save").fadeOut(250, function(){
							$(this).remove();
						});
					}
				});
			}, 500);
		}
	}
	
	// Создание подложки
	
	$("table.banners-text td.field a.mask").live("click", function(){
		var el = $(this);
		var num = $(this).parent().parent().parent().attr("class");
		num = num.replace(/fields_text/g,'');		
		if ($(el).attr("class") == "mask"){
			$(el).addClass("active").html("Подложка");
			$(el).parent().parent().next().find("div.mask").addClass("active");
			$("div.banner_container div.jSboxBanner-text"+num+"_bg").show(0);
			if ($("div.banner_container div.jSboxBanner-text"+num).length && !$("div.banner_container div.jSboxBanner-text"+num+"_bg").length) {
				var bgcolor = $("table.banners-text tr.fields_text"+num+" input[name=text"+num+"_color_mask]").val();
				var opacity = $("table.banners-text tr.fields_text"+num+" div#choice-opacity-mask span.value").html();
				opacity = opacity.replace(/\%/g,'');
				opacity = opacity/100;
				var top = $("div.banner_container div.jSboxBanner-text"+num).position().top;
				var height = $("table.banners-text tr.fields_text"+num+" div#choice-size span.value").html();
				$("div.banner_container div.jSboxBanner-text"+num).after('<div style="position:absolute; top:'+top+'px; left:0px; background-color:#'+bgcolor+'; opacity:'+opacity+'; width:100%; height:'+height+'; z-index:1;" class="jSboxBanner-text'+num+'_bg"></div>');
				addButtonSave();
			}			
		}
		else {
			$(el).removeClass("active").html("+ подложка");
			$(el).parent().parent().next().find("div.mask").removeClass("active");
			$("div.banner_container div.jSboxBanner-text"+num+"_bg").hide(0);
		}
		return false;
	});
	$("table.banners-text td.field a.mask").live("mouseover mouseout", function(e){
		var el = $(this);
		if (e.type == "mouseover" && $(el).attr("class") == "mask active"){
			$(el).html("Убрать");
			
		} else if (e.type == "mouseout" && $(el).attr("class") == "mask active"){
			$(el).html("Подложка");
		}
	});		
	
	// Изменение содержания строк
	
	$("table.banners-text input[name=text_1]").keyup(function(){
		if ($("div.banner_container div.jSboxBanner-text1").length){
			if ($("div.banner_container div.jSboxBanner-text1 blink").length){
				$("div.banner_container div.jSboxBanner-text1 blink").html($(this).val());
			}
			else {
				$("div.banner_container div.jSboxBanner-text1").html($(this).val());
			}
			addButtonSave();
		}
	});
	$("table.banners-text input[name=text_2]").keyup(function(){
		if ($("div.banner_container div.jSboxBanner-text2").length){
			if ($("div.banner_container div.jSboxBanner-text2 blink").length){
				$("div.banner_container div.jSboxBanner-text2 blink").html($(this).val());
			}
			else {
				$("div.banner_container div.jSboxBanner-text2").html($(this).val());
			}
			addButtonSave();
		}
	});
	$("table.banners-text input[name=text_3]").keyup(function(){
		if ($("div.banner_container div.jSboxBanner-text3").length){
			if ($("div.banner_container div.jSboxBanner-text3 blink").length){
				$("div.banner_container div.jSboxBanner-text3 blink").html($(this).val());
			}
			else {
				$("div.banner_container div.jSboxBanner-text3").html($(this).val());
			}
			addButtonSave();
		}
	});	
	
	// Изменение размера шрифта
	
	$("div.btn-group#choice-size ul li a").click(function(){
		var num = $(this).parent().parent().parent().parent().parent().attr("class");
		var size = $(this).html();
		num = num.replace(/fields_text/g,'');
		if ($("div.banner_container div.jSboxBanner-text"+num).length){
			$("div.banner_container div.jSboxBanner-text"+num).css("font-size", size);
			$("div.banner_container div.jSboxBanner-text"+num).css("line-height", size);
			if ($("div.banner_container div.jSboxBanner-text"+num+"_bg").length){
				$("div.banner_container div.jSboxBanner-text"+num+"_bg").css("height", size);
			}
			var shadow="";
			var cl = $("table.banners-text tr.fields_text"+num).find("div#choice-style").children("button[name=shadow]").attr("class");
			if (cl == "btn active"){
				size = size.replace(/px/g,'');
				if (size <= 30){shadow = "1px 1px 2px rgba(0,0,0,1)";}
				else if (size <= 40){shadow = "1px 1px 3px rgba(0,0,0,0.85)";}
				else if (size > 40){shadow = "1px 1px 4px rgba(0,0,0,0.85)";}
				$("div.banner_container div.jSboxBanner-text"+num).css("text-shadow", shadow);
			}
			addButtonSave();
		}
	});
	
	// Изменение семейства шрифта
	
	$("div.btn-group#choice-font ul li a").click(function(){
		var num = $(this).parent().parent().parent().parent().parent().attr("class");
		var font = $(this).html();
		num = num.replace(/fields_text/g,'');
		if ($("div.banner_container div.jSboxBanner-text"+num).length){
			$("div.banner_container div.jSboxBanner-text"+num).css("font-family", font);
			addButtonSave();
		}
	});	
	
	// Изменение прозрачности текста
	
	$("div.btn-group#choice-opacity ul li a").click(function(){
		var num = $(this).parent().parent().parent().parent().parent().attr("class");
		var op = String($(this).html());
		op = op.replace(/\%/g,'');
		op = op/100;
		$(this).parent().parent().parent().parent().prev().children("input.color").css("opacity", op);
		num = num.replace(/fields_text/g,'');
		if ($("div.banner_container div.jSboxBanner-text"+num).length){
			$("div.banner_container div.jSboxBanner-text"+num).css("opacity", op);
			addButtonSave();
		}		
	});	
	
	// Изменение прозрачности подложки

	$("div.btn-group#choice-opacity-mask ul li a").click(function(){
		var num = $(this).parent().parent().parent().parent().parent().parent().attr("class");
		var op = String($(this).html());
		op = op.replace(/\%/g,'');
		op = op/100;
		$(this).parent().parent().parent().parent().find("input.color").css("opacity", op);
		num = num.replace(/fields_text/g,'');
		if ($("div.banner_container div.jSboxBanner-text"+num+"_bg").length){
			$("div.banner_container div.jSboxBanner-text"+num+"_bg").css("opacity", op);
			addButtonSave();
		}
	});		
	
	// Изменение стиля шрифта
	
	$("div.btn-group#choice-style button").click(function(){
		var num = $(this).parent().parent().parent().attr("class");
		var style = $(this).attr("name");
		var cl = $(this).attr("class");
		cl = cl.replace(/btn/g,'');
		cl = cl.replace(/\ /g,'');
		num = num.replace(/fields_text/g,'');
		if ($("div.banner_container div.jSboxBanner-text"+num).length){
			if (style == "bold" && cl == ""){$("div.banner_container div.jSboxBanner-text"+num).css("font-weight", "bold");}
			else if (style == "bold" && cl == "active"){$("div.banner_container div.jSboxBanner-text"+num).css("font-weight", "normal");}
			if (style == "italic" && cl == ""){$("div.banner_container div.jSboxBanner-text"+num).css("font-style", "italic");}
			else if (style == "italic" && cl == "active"){$("div.banner_container div.jSboxBanner-text"+num).css("font-style", "normal");}
			if (style == "underline" && cl == ""){$("div.banner_container div.jSboxBanner-text"+num).css("text-decoration", "underline");}
			else if (style == "underline" && cl == "active"){$("div.banner_container div.jSboxBanner-text"+num).css("text-decoration", "none");}	
			if (style == "shadow" && cl == ""){
				var shadow="";
				var size = $("table.banners-text tr.fields_text"+num).find("div#choice-size").find("span.value").html();
				size = size.replace(/px/g,'');
				if (size <= 30){shadow = "1px 1px 2px rgba(0,0,0,1)";}
				else if (size <= 40){shadow = "1px 1px 3px rgba(0,0,0,0.85)";}
				else if (size > 40){shadow = "1px 1px 4px rgba(0,0,0,0.85)";}
				$("div.banner_container div.jSboxBanner-text"+num).css("text-shadow", shadow);
			}
			else if (style == "shadow" && cl == "active"){$("div.banner_container div.jSboxBanner-text"+num).css("text-shadow", "none");}
			if (style == "blink" && cl == ""){
				var text = $("div.banner_container div.jSboxBanner-text"+num).html();
				$("div.banner_container div.jSboxBanner-text"+num).html('<blink>'+text+'</blink>');
			}
			else if (style == "blink" && cl == "active"){
				var text = $("div.banner_container div.jSboxBanner-text"+num).children("blink").html();
				$("div.banner_container div.jSboxBanner-text"+num).html(text);
			}
			addButtonSave();
		}
	});	
	
	// Повтор анимации, выбор интервала
	$("div#banners div.repeat ul li a").live("click", function(){
		addButtonSave();
	});
	
	// Закруглить углы баннера
	
	$("div.choice-border div.js-box").live("click", function(){
		var el = $(this);
		if ($(el).attr("class") == "js-box"){
			$(el).addClass("checked");
			if ($("div.banner_container div.banner").length){
				$("div.banner_container div.banner").css("border-radius", "10px");
			}
		}
		else {
			$(el).removeClass("checked");
			if ($("div.banner_container div.banner").length){
				$("div.banner_container div.banner").css("border-radius", "0px");
			}	
		}
		addButtonSave();
	});	
	
	// Изменение размера баннера
	
	$("div.banner_container .ui-spinner-up").live('click', function(){
		var count = parseInt($(this).parent().children("input").val());
		count = count+1;
		$(this).parent().children("input").attr("value", count).focus();
		var type = String($(this).parent().attr("class"));
		type = type.replace(/roulette-/g,'');
		resizeBanner(type, count);		
	});
	$("div.banner_container .ui-spinner-down").live('click', function(){
		var count = parseInt($(this).parent().children("input").val());
		if (count > 80){
			count = count-1;
			$(this).parent().children("input").attr("value", count).focus();
			var type = String($(this).parent().attr("class"));
			type = type.replace(/roulette-/g,'');
			resizeBanner(type, count);
		}
	});
	$("div.banner_container div.roulette-width input").keyup(function(){
		var value = $(this).val();
		if (value > 79){
			resizeBanner("width", value);
		}
	});
	$("div.banner_container div.roulette-height input").keyup(function(){
		var value = $(this).val();
		if (value > 79){
			resizeBanner("height", value);
		}
	});	
	
	function resizeBanner(type, value){
		if (type == "width"){
			$("div.banner_container div.banner").css({"width": value+"px", "margin-left": -((value/2)+1)+"px"});
			$("div.banner_container div.banner div.jSboxBanner-bg").css({"width": value+"px"});
		}
		else if (type == "height"){
			$("div.banner_container").css({"height": value+"px"});
			$("div.banner_container div.banner").css({"height": value+"px"});
			$("div.banner_container div.banner div.jSboxBanner-bg").css({"height": value+"px"});
			$("div.banner_container div.roulette-height").css({"height": value+"px"});
		}
		$("div.banner_container div.save").remove();
		var width_banner = parseInt($("div.banner_container div.banner").width());
		var rol_x_left="";
		var rol_x_width = parseInt(width_banner/2.5);
		if (width_banner < 961){rol_x_left = ((961-width_banner)/2)-28;}
		if (rol_x_left < 18){rol_x_left = 18;}
		$("div.banner_container div.roulette-width").css({"width": rol_x_width+"px", "left": rol_x_left+"px"});
		var rol_y_right="";
		if (width_banner < 961){rol_y_right = ((961-width_banner)/2)-39;}
		if (rol_y_right < 18){rol_y_right = 18;}
		$("div.banner_container div.roulette-height").css({"right": rol_y_right+"px"});
		if (rol_y_right < 32){
			$("div.banner_container div.roulette-height input").css({"left": "-20px"});
			$("div.banner_container div.roulette-height a.ui-spinner-button").css({"left": "21px"});
		}
		else {
			$("div.banner_container div.roulette-height input").css({"left": "-5px"});
			$("div.banner_container div.roulette-height a.ui-spinner-button").css({"left": "36px"});
		}		
	}
	
});

// Изменение цвета текста и подложки

function setColorFont(){
	for (i=1; i <= 3; i++){
		if ($("div.banner_container div.jSboxBanner-text"+i).length){
			$("div.banner_container div.jSboxBanner-text"+i).css("color", "#"+$("div#banners input[name=text"+i+"_color]").val());
		}
		if ($("div.banner_container div.jSboxBanner-text"+i+"_bg").length){
			$("div.banner_container div.jSboxBanner-text"+i+"_bg").css("background-color", "#"+$("div#banners input[name=text"+i+"_color_mask]").val());
		}		
	}
}

String.prototype.trim = function() {return this.replace(/^[\s\r\n\t]+|[\s\r\n\t]+$/g,'');};

function onerrorBgImg(data){
	$(function(){
		var link = $("div.images-library div.item div.img img#"+data).attr("alt");
		$("div.images-library div.item div.img img#"+data).attr("src", link);
		$("div.images-library div.item div.img img#"+data).parent().addClass("bg").css("background", "url("+link+") 100% 100% repeat");
	});
};

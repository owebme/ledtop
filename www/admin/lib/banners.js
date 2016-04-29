$(document).ready(function(){

	$("div.btn-group a.btn").live("click", function(){
		$("div#content").css("overflow", "visible");
	});
	$("div.btn-group ul li a").live("click", function(){
		$("div#content").css("overflow", "hidden");
	});
	
	if ($("div.banner_container.upload div.banner img").length){
		$("div.banner_container.upload div.banner input.file").easyTooltip();
	}

	// Загрузить картинку

	$("div.banner_container.upload input.file").bind({
		change: function() {
			addBanner(this.files, this);
		}
	});

	function addBanner(files, el) {
		var input = el; 
		var imageType = /image.*/;
		var num = 0;
		$.each(files, function(i, file) {
			if (!file.type.match(imageType)) {
				alert('Добавляемый файл "'+file.name+'" не является картинкой');
				return true;
			}
			num++;
			if (num == 1){
				if ($(input).parent().attr("class") == "banner"){
					$(input).parent().find("div.img").children("img").replaceWith('<div class="ajax"></div>');
				}
				else if ($(input).parent().attr("class") == "banner add"){
					$(input).parent().find("div.img").children("span").replaceWith('<div class="ajax"></div>');
					$(input).parent().removeClass("add");
					$(input).parent().append('<a href="#" class="del" title="Удалить картинку"></a>');
				}
				$("div.banner_container div.resize").remove();
				var img = $('<img class="paste"/>');
				$(input).parent().find("div.img").prepend(img);
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
			$(input).parent().find("div.img").find('img.paste').each(function(){
				var uploadItem = $(this);
				var id = $(uploadItem).parent().parent().attr("id");
				var params = new Object();
				params.banner_upload_id = id;
				params.banner_upload = $(uploadItem).attr("src");
				$.post('/cgi-bin/admin/modules/banners_ajax.cgi', params, function(data){
					if (data != ""){
						var width = data.replace(/(\d+)\|(\d+)\|(.*)/,'$1');
						var height = data.replace(/(\d+)\|(\d+)\|(.*)/,'$2');
						var img = data.replace(/(\d+)\|(\d+)\|(.*)/,'$3');
						resizeBanner("width", width);
						resizeBanner("height", height);
						$("div.banner_container div.roulette-width input").attr("value", width);
						$("div.banner_container div.roulette-height input").attr("value", height);
						$(uploadItem).replaceWith('<img class="paste" src="/files/banners/'+img+'" alt="">');
						$("div.banner_container.upload div.banner").find("img.paste").css("margin-left", -(width/2)+"px");
						$("div.banner_container.upload div.banner").find("div.ajax").remove();
						$("div.banner_container.upload div.banner").find("img.paste").css("opacity", "1");
						$("div.banner_container.upload div.banner input.file").addClass("off").attr("title", "Сменить картинку").easyTooltip();
						$("div.banner_container div.resize").remove();
					}
				});
			});
		}, 200);
	}
	
	
	// Удалить изображения
	
	$("div.banner_container a.del").live('click', function(){
		var el = $(this);
		var id = $(el).parent().attr("id");
		var params = new Object();
		params.banner_del = id;
		$.post('/cgi-bin/admin/modules/banners_ajax.cgi', params);
		$(el).parent().addClass("add");
		$(el).parent().find("div.img").html('<span><em>Загрузите картинку</em></span>');
		$(el).parent().find("input.file").attr("title", "").easyTooltip();
		$(el).remove();
		$("div.banner_container div.resize").remove();
		
		return false;
	});	
	
	
	// Изменить размер изображения
	
	$("div.banner_container div.resize input").live('click', function(){
		var input = $(this);
		$(input).parent().parent().children("div.banner").find("div.img").children("img").replaceWith('<div class="ajax"></div>');
		var banner_resize_width = parseInt($("div.banner_container div.roulette-width input").val());
		var banner_resize_height = parseInt($("div.banner_container div.roulette-height input").val());
		var params = new Object();
		params.banner_resize = $(input).parent().parent().children("div.banner").attr("id");
		params.banner_resize_width = banner_resize_width;
		params.banner_resize_height = banner_resize_height;
		$(input).parent().remove();		
		$.post('/cgi-bin/admin/modules/banners_ajax.cgi', params, function(data){
			if (data != ""){
				$("div.banner_container.upload div.banner").find("div.ajax").replaceWith('<img style="margin-left:-'+(banner_resize_width/2)+'px" src="/files/banners/'+data+'" alt="">');	
			}
		});
	});
	
	
	// Изменение размера баннера
	
	$("div.banner_container .ui-spinner-up").live('click', function(){
		var count = parseInt($(this).parent().children("input").val());
		count = count+1;
		if (count <= 800){
			$(this).parent().children("input").attr("value", count).focus();
			var type = String($(this).parent().attr("class"));
			type = type.replace(/roulette-/g,'');
			resizeBanner("resize", count);	
		}
	});
	$("div.banner_container .ui-spinner-down").live('click', function(){
		var count = parseInt($(this).parent().children("input").val());
		if (count >= 80){
			count = count-1;
			$(this).parent().children("input").attr("value", count).focus();
			var type = String($(this).parent().attr("class"));
			type = type.replace(/roulette-/g,'');
			resizeBanner("resize", count);
		}
	});
	$("div.banner_container div.roulette-width input").keyup(function(){
		var value = $(this).val();
		if (value >= 80 && value <= 800){
			resizeBanner("resize", value);
		}
	});
	$("div.banner_container div.roulette-height input").keyup(function(){
		var value = $(this).val();
		if (value >= 80){
			resizeBanner("resize", value);
		}
	});	
	
	function resizeBanner(type, value){
		if (type == "width"){
			$("div.banner_container div.banner").css({"width": value+"px", "margin-left": -((value/2)+1)+"px"});
			$("div.banner_container div.banner div.img").css({"width": value+"px"});
		}
		else if (type == "height"){
			$("div.banner_container").css({"height": value+"px"});
			$("div.banner_container div.banner").css({"height": value+"px"});
			$("div.banner_container div.banner div.img").css({"height": value+"px"});
			$("div.banner_container div.roulette-height").css({"height": value+"px"});
		}
		else if (type == "resize"){
			var width = parseInt($("div.banner_container div.roulette-width input").val());
			var height = parseInt($("div.banner_container div.roulette-height input").val());
			var width_img = parseInt($("div.banner_container div.banner div.img img").width());
			var height_img = parseInt($("div.banner_container div.banner div.img img").height());
			if (!width_img){width_img = width;}
			if (!height_img){height_img = height;}
			if (width != width_img){
				var delta = width_img/width;
				height = (height_img/delta).toFixed(0);
			}
			else if (height != height_img){
				var delta = height_img/height;
				width = (width_img/delta).toFixed(0);
			}
			$("div.banner_container div.banner").css({"width": width+"px", "height": height+"px", "margin-left": -((width/2)+1)+"px"});
			$("div.banner_container div.banner div.img").css({"width": width+"px", "height": height+"px"})
			$("div.banner_container div.banner div.img img").css({"width": width+"px", "height": height+"px", "margin-left": -(width/2)+"px"});
			$("div.banner_container").css({"height": height+"px"});
			$("div.banner_container div.roulette-height").css({"height": height+"px"});
			$("div.banner_container div.roulette-width input").attr("value", width);
			$("div.banner_container div.roulette-height input").attr("value", height);
		}
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
		var left = parseInt($("div.banner_container div.roulette-height").position().left);
		var bottom="";
		if (width_banner < 280){bottom = "81";} else {bottom = "46";}
		if ($("div.banner_container div.resize").length){
			$("div.banner_container div.resize").css({"left": (left-134)+"px", bottom: "-"+bottom+"px"});
		}
		else {
			$("div.banner_container").append('<div class="resize "style="left:'+(left-134)+'px; bottom:-'+bottom+'px"><input title="Изменить размер изображения" type="button" class="button resize" value="Применить"></div>');
		}		
	}

});
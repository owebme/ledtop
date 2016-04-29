var dirs_foto = '/cgi-bin/admin/modules';

$(function() {
	$("#sortable").sortable();
	$("#sortable").disableSelection();
});

$(function() {
$("#sortable" ).bind( "sortstop", function(event, ui) {
	var params = new Object();
	params.album_list = $("#sortable").html();
	$.post(dirs_foto+'/fotogal_ajax.cgi', params);
});
});

$(document).ready(function(){

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
				if (isNaN($("div.save_page").html())){
					location.replace($("div#main_menu div#gallery a").attr("href"));
					e.preventDefault();
				}
			}
			else {
				return true;
			}
		}
		else if (e.which == 27){
			if (getUrlVars()["par"] == "new"){
				if (confirm('Отменить создание фотогалереи?')) {
					location.replace($("div#main_menu div#gallery a").attr("href"));
					e.preventDefault();
				} else {
					return false;
				}
			}
		}		
	});
	
	$("table#page_new input").keydown(function(e){
		if (e.which == 13){
			e.preventDefault();	
			return false;
		}		
	});	
	
	function getUrlVars() {
		var vars = {};
		var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
			vars[key] = value;
		});
		return vars;
	}	

	$("a.lamp").click(function() {
		var el = $(this);
		var params = new Object();
		params.fotogal_show = "active";
		params.fotogal_id = $(this).parent().attr("inum");		
		$.post(dirs_foto+'/fotogal_ajax.cgi', params, function(data){
		if(data == "1"){
			$(el).parent().removeClass("off");		
			$(el).animate({opacity:1}, 0);
			$(el).attr("title", "Скрыть фотогалерею");				
			return false;
		} else if(data == "0"){
			$(el).parent().addClass("off");	
			$(el).animate({opacity:0.5}, 0);	
			$(el).attr("title", "Сделать активной");				
			return false;
		}});
		return false;
	});
		
	$("a.del").click(function() {
		var el = $(this);
		var params = new Object();
		params.fotogal_del = "active";
		params.fotogal_id = $(this).parent().attr("inum");
		var	name_product = $(this).parent().attr("name");	
		if (confirm('Удалить фотогалерею "'+name_product+'"')) {		
			$.post(dirs_foto+'/fotogal_ajax.cgi', params);
			$(el).parent().fadeOut("slow", function(){
				$(el).parent().remove();
			});
			return false;		
		}
		return false;
	});
	
	$("div.gallery_type div.maket div.save a").live("click", function(){
		var code = $(this).parent().next().next().children("div.CodeMirror");
		$(code).css('background-color','#e0ffe0');
		var id = $(this).parent().parent().attr("type_id");
		var params = new Object();
		var css_file="";
		if (id == "1"){css_file = editor1.getValue();}
		else if (id == "2"){css_file = editor2.getValue();}
		else if (id == "3"){css_file = editor3.getValue();}
		params.css_id = id;
		params.css_file = css_file;		
		$.post(dirs_foto+'/fotogal_ajax.cgi', params, function(data){
			if (data == "ok") {
				$(code).animate({'background-color': '#ffffff'});
			}
		}); 
		return false;
	});	
	
	$("div.gallery_type div.maket").css("display", "none").css("status", "hide");
	$("div.gallery_type div.edit a").live("click", function(){
		var el = $(this).parent();
		$("div.gallery_type div.maket").each(function(){
			var maket = $(this);
			if ($(el).attr("id") == $(maket).attr("type_id")){
				if ($(maket).attr("status") == "active"){
					$(maket).fadeOut(200);
					$(maket).attr("status", "hide");
				}
				else {
					$(maket).fadeIn(400);
					$(maket).attr("status", "active");
				}
			}
		});
		
		return false;
	});
	
	if ($("div.watermark-upload div.watermark-img img").length){
		$("div.watermark-upload div.watermark-img input.file").easyTooltip();
	}	

	$("div.watermark-upload input.file").bind({
		change: function() {
			addWatermark(this.files, this);
		}
	});

	function addWatermark(files, el) {
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
				if ($(input).parent().attr("class") == "watermark-img"){
					$(input).parent().find("div.img").children("img").replaceWith('<div class="ajax"></div>');
					$(input).parent().addClass("add");
				}
				else if ($(input).parent().attr("class") == "watermark-img add"){
					$(input).parent().find("div.img").children("span").replaceWith('<div class="ajax"></div>');
					$(input).parent().append('<a href="#" class="del_watermark" title="Удалить водяной знак"></a>');
				}
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
				var params = new Object();
				params.watermark_upload = $(uploadItem).attr("src");
				$.post(dirs_foto+'/fotogal_ajax.cgi', params, function(data){
					if (data != ""){
						var width = data.replace(/(\d+)\|(\d+)\|(.*)/,'$1');
						var height = data.replace(/(\d+)\|(\d+)\|(.*)/,'$2');
						var img = data.replace(/(\d+)\|(\d+)\|(.*)/,'$3');
						var divHeight = parseInt($("div.watermark-upload div.watermark-img div.img").height())*1;
						var divDefHeight = parseInt($("div.watermark-upload").attr("data-height"))*1;
						if (height > (divHeight-20)){
							var mTop = parseInt(height)*1;
							$("div.watermark-upload, div.watermark-img, div.watermark-upload div.watermark-img div.img").animate({"height":(mTop+30)+"px"}, 400);
						}
						else if (height < divDefHeight && divHeight > divDefHeight){
							$("div.watermark-upload, div.watermark-img, div.watermark-upload div.watermark-img div.img").animate({"height":divDefHeight+"px"}, 400);
						}
						$(uploadItem).replaceWith('<img class="paste" src="'+img+'" alt="">');
						$("div.watermark-upload div.watermark-img").find("img.paste").css({"margin-top": -(height/2)+"px", "margin-left": -(width/2)+"px"});
						$("div.watermark-upload div.watermark-img").find("div.ajax").remove();
						var val_opacity = $("div.widget-slider.opacity input").val();
						val_opacity = parseInt(val_opacity.replace(/\%/g, ''));
						$("div.watermark-upload div.watermark-img").find("img.paste").css("opacity", (val_opacity)/100).removeClass("paste");
						$("div.watermark-upload div.watermark-img").removeClass("add");
						$("div.watermark-upload div.watermark-img input.file").addClass("off").attr("title", "Сменить картинку").easyTooltip();
					}
				});
			});
		}, 200);
	}
	
	if ($("div.watermark-fonts").length){
		var size = parseInt($("div.watermark-fonts select[name=watermark_size]").attr("data-value"));
		if (size > 0){
			$("div.watermark-fonts select[name=watermark_size] option").each(function(){
				if ($(this).attr("value") == size){
					$(this).attr('selected', true);
				}
			});
		}
		$("div.watermark-fonts input[name=watermark_text]").keyup(function(){
			var text = $("div.watermark-fonts input[name=watermark_text]").val();
			var size = $("div.watermark-fonts select[name=watermark_size]").val();
			$("div.watermark-fonts h5.test").css({"font-size": size+"px", "line-height": size+"px"}).html(text);
		});
		$("div.watermark-fonts select[name=watermark_size]").change(function(){
			var size = $("div.watermark-fonts select[name=watermark_size]").val();
			$("div.watermark-fonts h5.test").css({"font-size": size+"px", "line-height": size+"px"});
		});
		$("div.watermark-fonts h5.test").html($("div.watermark-fonts input[name=watermark_text]").val());
	}	
	
	$("div.watermark-fonts input.button").live('click', function(){	
		var text = $("div.watermark-fonts input[name=watermark_text]").val();
		var size = $("div.watermark-fonts select[name=watermark_size]").val();
		var color = $("div.watermark-fonts input[name=watermark_color]").val();
		var width = $("div.watermark-fonts h5.test").width();
		var height = $("div.watermark-fonts h5.test").height();
		if ($("div.watermark-upload div.watermark-img").attr("class") == "watermark-img"){
			$("div.watermark-upload div.watermark-img").find("div.img").children("img").replaceWith('<div class="ajax"></div>');
			$("div.watermark-upload div.watermark-img").addClass("add");
		}
		else if ($("div.watermark-upload div.watermark-img").attr("class") == "watermark-img add"){
			$("div.watermark-upload div.watermark-img").find("div.img").children("span").replaceWith('<div class="ajax"></div>');
			$("div.watermark-upload div.watermark-img").append('<a href="#" class="del_watermark" title="Удалить водяной знак"></a>');
		}	
		if (text != ""){
			text = text.replace(/^\s+/, "");
			text = text.replace(/\s+$/, "");
		}
		if (text != ""){
			var params = new Object();
			params.watermark_text = text;
			params.watermark_size = size;
			params.watermark_color = color;
			params.watermark_width = width;
			params.watermark_height = height;
			$.post(dirs_foto+'/fotogal_ajax.cgi', params, function(data){
				if (data != ""){
					var width = data.replace(/(\d+)\|(\d+)\|(.*)/,'$1');
					var height = data.replace(/(\d+)\|(\d+)\|(.*)/,'$2');
					var img = data.replace(/(\d+)\|(\d+)\|(.*)/,'$3');
					var divHeight = parseInt($("div.watermark-upload div.watermark-img div.img").height())*1;
					var divDefHeight = parseInt($("div.watermark-upload").attr("data-height"))*1;
					if (height > (divHeight-20)){
						var mTop = parseInt(height)*1;
						$("div.watermark-upload, div.watermark-img, div.watermark-upload div.watermark-img div.img").animate({"height":(mTop+30)+"px"}, 400);
					}
					else if (height < divDefHeight && divHeight > divDefHeight){
						$("div.watermark-upload, div.watermark-img, div.watermark-upload div.watermark-img div.img").animate({"height":divDefHeight+"px"}, 400);
					}
					$("div.watermark-upload div.watermark-img").find("div.img").html('<img class="paste" src="'+img+'" alt="">');
					$("div.watermark-upload div.watermark-img").find("img.paste").css({"margin-top": -(height/2)+"px", "margin-left": -(width/2)+"px"});
					$("div.watermark-upload div.watermark-img").find("div.ajax").remove();
					var val_opacity = $("div.widget-slider.opacity input").val();
					val_opacity = parseInt(val_opacity.replace(/\%/g, ''));
					$("div.watermark-upload div.watermark-img").find("img.paste").css("opacity", (val_opacity)/100).removeClass("paste");
					$("div.watermark-upload div.watermark-img").removeClass("add");
					$("div.watermark-upload div.watermark-img input.file").addClass("off").attr("title", "Сменить картинку").easyTooltip();
				}
			});
		}
		else {
			alert("Введите текст для водяного знака");
		}
	});
		
	$("div.watermark-upload a.del_watermark").live('click', function(){
		var el = $(this);
		var params = new Object();
		params.watermark_del = "delete";
		$.post(dirs_foto+'/fotogal_ajax.cgi', params);
		$(el).parent().addClass("add");
		$(el).parent().find("div.img").html('<span><em>Загрузите файл в формате <ins>png, gif, jpg</ins></em></span>');
		$(el).parent().find("input.file").attr("title", "").easyTooltip();
		$(el).remove();
		
		return false;
	});	

	// Регулировка прозрачности (слайдер)
	
	var val_opacity="";
	if ($("div.watermark-upload").length){
		val_opacity = $("div.widget-slider.opacity input").val();
		if (val_opacity == "OFF"){
			val_opacity = 0;
		}
		else {val_opacity = parseInt(val_opacity.replace(/\%/g, ''));}
		$(window).load(function(){
			$("div.watermark-settings").css("opacity", "1");
		});		
	}
	if ($("div.watermark-upload div.watermark-img div.img img").length){
		$("div.watermark-upload div.watermark-img div.img img").css("opacity", (val_opacity)/100);
	}	
	$("div#slider-opacity").slider({
		value:val_opacity,
		min: 10,
		max: 100,
		step: 1,
		range: "min",
		slide: function(event, ui){
			if (ui.value > 0){
				$("div.widget-slider.opacity input").val(ui.value + "%").removeClass("off");
				$("div#slider-opacity").removeClass("off");
			}
			else if (ui.value == 0){
				$("div.widget-slider.opacity input").val("OFF").addClass("off");
				$("div#slider-opacity").addClass("off");
			}
			if ($("div.watermark-upload div.watermark-img div.img img").length){
				$("div.watermark-upload div.watermark-img div.img img").css("opacity", (ui.value)/100);
			}
		}
	});
	$("div.widget-slider.opacity input").val($("div#slider-opacity").slider("value") + "%");
	if ($("div#slider-opacity").slider("value") == "0"){
		$("div.widget-slider.opacity input").val("OFF").addClass("off");
		$("div#slider-opacity").addClass("off");
	}	
	
});
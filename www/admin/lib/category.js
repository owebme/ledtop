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
				if (isNaN($("div.save_page").html())){
					location.replace("/cgi-bin/admin/engine/index.cgi?adm_act=category");
					e.preventDefault();
				}
			}
			else {
				return true;
			}
		}
		else if (e.which == 27){
			if (getUrlVars()["par"] == "new"){
				if (confirm('Отменить создание категории?')) {
					location.replace("/cgi-bin/admin/engine/index.cgi?adm_act=category");
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
	
	//$("div.three_pages ul.level0").nestedSortable({
	//	disableNesting: 'no-nest',
	//	forcePlaceholderSize: true,
	//	handle: 'a.name',
	//	helper:	'clone',
	//	items: 'li',
	//	maxLevels: 3,
	//	opacity: .75,
	//	placeholder: 'placeholder',
	//	revert: 250,
	//	tabSize: 25,
	//	tolerance: 'pointer',
	//	toleranceElement: '> a.name'
	//});	
	

$("a.lamp").click(function() {
		var el = $(this);
		var params = new Object();
		params.category_lamp = $(this).parent().attr("c_id");		
		$.post(dirs_catalog+'/category_ajax.cgi', params, function(data){
		if(data == "1"){
			$(el).parent().removeClass("off");
			$(el).animate({opacity:1}, 0);
			$(el).attr("title", "Скрыть категорию");				
			return false;
		} else if(data == "0"){
			$(el).parent().addClass("off");		
			$(el).animate({opacity:0.5}, 0);	
			$(el).attr("title", "Сделать активной");				
			return false;
		}});
		return false;
});



$("a.del").each(function(){
		var el = $(this);
		$(this).click(function(){
		var name_cat = $(this).parent().attr("name");
		if (confirm('Удалить категорию "'+name_cat+'"? Товары также будут удалены в этой категории')) {
		$(this).parent().fadeOut("slow", function(){
			$(el).parent().remove();
		});		
		
advAJAX.post({
url: (dirs_catalog+'/category_ajax.cgi'),
category_del: $(el).parent().attr("c_id")
});
			return false;

		}
			return false;
	});
});

$("div.prev_img").each(function(){
	var el = $(this);
	var heightDiv = parseInt($(el).height());
	var heightImg = parseInt($(el).find("img").height());
	if (heightImg < heightDiv && $(el).find("img").attr("style") != ""){
		var def = (heightDiv-heightImg)/2;
		$(el).find("img").css("marginTop", def+"px");
	}
});


$(function(){
    $('.up').click(move_up_cat);
    $('.down').click(move_down_cat);
	 
    function move_up_cat(eventObject){
		if ($(this).parent().next().next().next().attr("class") == "point last"){
			$(this).parent().parent().prev().children("div.point").addClass("last");
			$(this).parent().next().next().next().removeClass("last");
		}
        var curr_li = $(this).parent().parent();
        var prev_li = $(curr_li).prev();
        prev_li.insertAfter(curr_li);
				
		advAJAX.post({
			url: (dirs_catalog+'/category_ajax.cgi'),
			cat_move_up: $(this).parent().parent().attr("c_id"),
			cat_move_pid: $(this).parent().parent().attr("c_pid"),			
			cat_move_pos: $(this).parent().parent().attr("c_pos")			
		});			
			return false;
    }
	 
	function move_down_cat(eventObject){
		if ($(this).parent().parent().next().children("div.point").attr("class") == "point last"){
			$(this).parent().next().next().next().addClass("last");
			$(this).parent().parent().next().children("div.point").removeClass("last");
		}
	    var curr_li = $(this).parent().parent();
	    var next_li = $(curr_li).next();
	    next_li.insertBefore(curr_li);
		advAJAX.post({
			url: (dirs_catalog+'/category_ajax.cgi'),
			cat_move_down: $(this).parent().parent().attr("c_id"),
			cat_move_pid: $(this).parent().parent().attr("c_pid"),			
			cat_move_pos: $(this).parent().parent().attr("c_pos")
		});		
			return false;
    }
});

	$("input.fileInput").change(function(){
		addImgFile(this.files, this);
	});

	function addImgFile(files, el) {
		var div = $(el).prev();
		var imageType = /image.*/;
		var num = 0;
		$.each(files, function(i, file) {
			if (!file.type.match(imageType)) {
				alert('Добавляемый файл "'+file.name+'" не является картинкой');
				return true;
			}
			num++;
			if (num == 1){
				var img = $('<img/>');
				$(div).removeClass("no_show").empty().append(img);
				var heightDiv = parseInt($(div).height());
				var heightImg ="";
				$(div).find("img").load(function(){
					heightImg = parseInt($(this).height());
					if (heightImg < heightDiv){
						var def = (heightDiv-heightImg)/2;
						$(div).find("img").css("marginTop", def+"px");
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
			}
		});
	}

	$("td.img_load input.give_url_big").live('mouseover mouseout', function(e){
		var el = $(this);
		if (e.type == 'mouseover'){
			$(el).attr("value", "Вставьте ссылку Ctrl+V");
			$(el).next("div.help").stop(true, true);
			$(el).next("div.help").fadeIn(200);
			$(el).focus();
		}
		else if (e.type == 'mouseout'){
			$(el).attr("value", "");
			$(el).next("div.help").fadeOut(200);
		}
	});
	
	$("td.img_load input.give_url_big").live('mouseover', function(){
		var el = $(this);
		var div = $(this).parent().parent().parent().prev().children("td.img_load").children("div.prev_img");
		document.onkeydown = hotkeys;
		function hotkeys(e) {
			if (!e) e = window.event;
			var k = e.keyCode;
			if (e.ctrlKey && k == 86) {
				window.setTimeout(function(){
					var url = $(el).val();				
					if (url != ""){
						$(el).attr("value", "");
						$(div).children("div.error").remove();
						$(div).children("img").hide(0);
						$(div).show(0);
						$(div).append('<div class="ajax"></div>');
						var cat_id = $(el).attr("cat_id");
						if (cat_id == ""){cat_id = "empty";}
						var img_ox = $("tr.autoresize input[name=img_ox]").val();
						var img_oy = $("tr.autoresize input[name=img_oy]").val();
						var params = new Object();
						params.ajax_cat_id = cat_id;
						params.ajax_img_url = url;
						params.ajax_img_ox = img_ox;
						params.ajax_img_oy = img_oy;
						$.post(dirs_catalog+'/category_ajax.cgi', params, function(data){
							if (data != ""){
								if (data != "error"){
									$(div).empty().append(data);
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
								else {
									var widthDiv = parseInt($(div).width());
									var heightDiv = parseInt($(div).height());
									$(div).children("div.ajax").remove();
									url = url.replace(/Вставьте ссылку Ctrl\+V/g, "");
									url = url.replace(/^\s+/,"");
									url = url.replace(/(.*)http/g, "http");
									var msg = 'Ccылка на изображение:<span>&laquo;<b>'+url+'</b>&raquo;</span> не является картинкой';
									if (url == ""){msg = 'Cсылка не имеет адреса,<br> вы вставляете пустой адрес';}
									$(div).append('<div class="error"><p style="width:'+widthDiv+'px; height:'+heightDiv+'px;">'+msg+'</p></div>');
									$(div).children("img").show(0);
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
				$.post(dirs_catalog+'/category_ajax.cgi', params, function(data){
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
			$.post(dirs_catalog+'/category_ajax.cgi', params, function(data){
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
		$.post(dirs_catalog+'/category_ajax.cgi', params);
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
	
	$(function(){
	
		$("a.ajaxSave").live('click', function() {
			ajaxSave();			
			var ed1=""; var content1="";
			var ed2=""; var content2="";
			var category_id = $("a.preview_page").attr("id");
			if ($("textarea#elm1").length){
				ed1 = tinyMCE.get('elm1');
				content1 = ed1.getContent();
				if (content1 == "" && category_id != ""){content1 = "clear";}
			}		
			if ($("textarea#elm1_sm").length){
				ed2 = tinyMCE.get('elm1_sm');
				content2 = ed2.getContent();
				if (content2 == "" && category_id != ""){content2 = "clear";}
			}
			var params = new Object();
			params.category_id = category_id;
			params.category_content1 = content1;
			params.category_content2 = content2;
			$.post(dirs_catalog+'/category_ajax.cgi', params);
			return false;
		});
	});	

});

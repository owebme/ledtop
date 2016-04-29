var dirs_catalog = '/cgi-bin/admin/modules';

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
					location.replace($("div#main_menu div#news a").attr("href"));
					e.preventDefault();
				}
			}
			else {
				return true;
			}
		}		
		else if (e.which == 27){
			if (getUrlVars()["par"] == "new"){
				if (confirm('Отменить создание новости?')) {
					location.replace($("div#main_menu div#news a").attr("href"));
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
		params.news_lamp = $(this).parent().attr("c_id");		
		$.post(dirs_catalog+'/news_ajax.cgi', params, function(data){
		if(data == "1"){
			$(el).parent().removeClass("off");
			$(el).animate({opacity:1}, 0);
			$(el).attr("title", "Скрыть новость");				
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
		var name_news = $(this).parent().attr("name");
		if ($(this).attr("id") == "off") {return false;}
		else {if (confirm('Удалить новость "'+name_news+'"')) {
		$(this).parent().fadeOut("slow", function(){
			$(el).parent().remove();
		});		
		
advAJAX.post({
url: (dirs_catalog+'/news_ajax.cgi'),
news_del: $(el).parent().attr("c_id")
});
			return false;

		}}
			return false;
	});
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

	$("div.prev_img").each(function(){
		var el = $(this);
		var heightDiv = parseInt($(el).height());
		var heightImg = parseInt($(el).find("img").height());
		if (heightImg < heightDiv && $(el).find("img").attr("style") != ""){
			var def = (heightDiv-heightImg)/2;
			$(el).find("img").css("marginTop", def+"px");
		}
	})

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
						params.ajax_news_id = cat_id;
						params.ajax_img_url = url;
						params.ajax_img_ox = img_ox;
						params.ajax_img_oy = img_oy;
						$.post(dirs_catalog+'/news_ajax.cgi', params, function(data){
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

});
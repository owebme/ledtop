var dirs_foto = '/cgi-bin/admin/modules';

$(function() {
	$("#sortable").sortable();
//	$("#sortable").disableSelection();
});

$(function() {
$("#sortable" ).bind( "sortstop", function(event, ui) {
	var params = new Object();
	params.fotolist = $("#sortable").html();
	params.num_edit = $("#sortable").attr("idnum");
	$.post(dirs_foto+'/fotolist_ajax.cgi', params);
});
});

$(document).ready(function(){

	// Обработка f5 и ctrl+f5
	var isCtrl = false;
	var isCmd = false;
	$(document).keyup(function(e) {
		if(e.which == 17) isCtrl=false;
		if(e.which == 91) isCmd=false;
	}).keydown(function(e) {
		if(e.which == 17) isCtrl=true;
		if(e.which == 91) isCmd=true;
		if(e.which == 116 && (isCtrl || isCmd)) {
			if (isNaN($("div.save_page").html())){
				location.replace(location.href);
				e.preventDefault();				
			}
			else {
				return true;
			}
		}		
		else if (e.which == 116){
			location.replace(location.href);
			e.preventDefault();
		}
	});
	
	$("table#page_new input").keydown(function(e){
		if (e.which == 13){
			e.preventDefault();	
			return false;
		}		
	});	
	
	$("div.hdr#on").live("click", function(){
		$(this).attr("id", "off");
		$(this).next().attr('checked', false);
		$(this).attr('title', "HDR выключен");
	});	
	
	$("div.hdr#off").live("click", function(){
		$(this).attr("id", "on");
		$(this).next().attr('checked', true);
		$(this).attr("title", "HDR включен");
		$("input.hdr_off").next().removeClass("checked")
		$("input.hdr_off").attr('checked', false);
	});
	
    $("div.cb").live("click", function(){
		var el = $(this);
		if ($(el).prev().attr("class") == "cb hdr_off" && $(el).attr("class") == "cb checked"){
			$("div.hdr").attr("id", "off");
			$("div.hdr").attr("title", "HDR выключен");
			$("div.hdr").next().attr('checked', false);
		}
	});
	

	$("a#click_addfoto").click(function() {
		if (!$("div.introjs-overlay").length){
			$("div#desc_fotogal").fadeOut(150, "easeOutSine");
			$("div#fotogal").fadeOut(150, "easeOutSine", function() {
			$("div#addfoto").fadeIn(150, "easeInSine");	
			});
			$("div#tabs li").removeClass("activetab");		
			var el = $(this).parent();
			$(el).addClass("activetab");
			$("input").each(function() {
				if ($(this).attr("name") == "imagetextsm") {$(this).attr("value","");}
			});
			$("textarea.lite").each(function() {
				if ($(this).attr("name") == "imagetextbig") {$(this).html();}
			});		
		}
		return false;
	});
	
	$("a#click_fotogal").click(function() {
		if (!$("div.introjs-overlay").length){
			$("div#addfoto").fadeOut(150, "easeOutSine", function() {
			$("div#fotogal").fadeIn(150, "easeInSine");
			$("div#desc_fotogal").fadeIn(150, "easeInSine");		
			});
			$("div#tabs li").removeClass("activetab");		
			var el = $(this).parent();
			$(el).addClass("activetab");
		}
		return false;
	});	

	$(".model").click(function(){
		if($(this).attr("editing")!='1'){
			$(this).attr("editing","1");
			$(this).html('<textarea class="editor_desc" id="editor'+$(this).attr("idtext")+'">'+$(this).html()+'</textarea>');
			setActionEditor_desc($("#editor"+$(this).attr("idtext")));
			
		}
	})
	
	var onMouseOutOpacity = 0.67;	

	$('ul#sortable li').opacityrollover({
	mouseOutOpacity:   onMouseOutOpacity,
	mouseOverOpacity:  1.0,
	fadeSpeed:         'fast',
	exemptionSelector: '.selected'
	});
	
	
	$("ul#sortable li div.foto").live('mouseover mouseout', function(e){
		if( e.type == 'mouseover' ){
			var id = $(this).attr('id_foto');
			$("a.zoom_foto").each(function(){
				if( $(this).attr('id_zoom') == id) $(this).fadeIn(0);
			});
		} else if( e.type == 'mouseout' ){
			$("a.zoom_foto").stop(true, true);	
			$("a.zoom_foto").each(function(){
				if( $(this).attr('id_zoom') != id) $(this).fadeOut(0);
			});
		}
	});	

	$("div.hide_resize input").attr("readonly", "readonly").css("color", "#888888");
	
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
				var img_big = $('<img style="max-width:220px; max-height:150px;"/>');
				$(elem).parent().parent().prev().children("td").children("div.prev_img").attr("style", "width:220px; height:150px; overflow:hidden;");
				$(elem).parent().parent().prev().children("td").children("div.prev_img").empty().append(img_big);
				img_big.get(0).file = file;
				
				var reader = new FileReader();
				reader.onload = (function(aImg) {
					return function(e) {
						aImg.attr('src', e.target.result);
					};
				})(img_big);
				
				reader.readAsDataURL(file);

				if (resize_sm.is(':checked') && type_img == "imagebg"){
					var img_sm = $('<img style="max-width:220px; max-height:150px;"/>');
					$(elem).parent().parent().next().children("td").children("div.prev_img").attr("style", "width:220px; height:150px; overflow:hidden;");
					$(elem).parent().parent().next().children("td").children("div.prev_img").empty().append(img_sm);
					img_sm.get(0).file = file;
					
					var reader = new FileReader();
					reader.onload = (function(aImg) {
						return function(e) {
							aImg.attr('src', e.target.result);
						};
					})(img_sm);
					
					reader.readAsDataURL(file);				
				}
			}
		});
	}	

});	

function setActionEditor_desc(editor){
	editor.focus();
	editor.blur(function(){
		$(this).parent().attr("editing","");
		var params = new Object();
		params.id_des = $(this).parent().attr("idtext");
		params.num_edit = $("#sortable").attr("idnum");
		if ($(this).val() == "") {params.descript_text = " ";}
		else {params.descript_text = $(this).val();}
		$.post(dirs_foto+'/fotolist_ajax.cgi', params);
		$(this).parent().html($(this).val());
	});
}

$(function(){
	$("a.del_foto").each(function(){
		var el = $(this);
		$(this).click(function(){

advAJAX.post({
url: (dirs_foto+'/fotolist_ajax.cgi'),
del_foto: $(this).attr("id_del"),
num_edit: $("#sortable").attr("idnum"),
onSuccess : function(obj) {
							$(el).parent().animate({opacity:"hide"}, 400, function(){
						     	});
}
		});
return false;
	});
});
});
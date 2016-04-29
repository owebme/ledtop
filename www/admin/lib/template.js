var dirs_template = '/cgi-bin/admin/modules';

$(document).ready(function(){
	
var file = $("div.maket a.button").attr("file");			
var params = new Object();
params.file_edit = file;
var mesg_save = "Файл сохранен.";
$("div#content").css("overflow", "visible");
	
	// Обработка ctrl+s
	var isCtrl = false;
	var isCmd = false;
	$(document).keyup(function (e) {
		if(e.which == 17) isCtrl=false;
		if(e.which == 91) isCmd=false;
	}).keydown(function (e) {
		if(e.which == 17) isCtrl=true;
		if(e.which == 91) isCmd=true;
		if(e.which == 83 && (isCtrl || isCmd)) {
			$('.CodeMirror').css('background-color','#e0ffe0');
			params.template_edit = editor.getValue()
			$.post(dirs_template+'/template_ajax.cgi', params, function(data){
				if (data == "ok") {
					var sm="";
					if ($("div.maket div a").size() == 2){sm = " sm";}
					$('.CodeMirror').animate({'background-color': '#ffffff'});
					$("div.save_maket").empty().append('<div class="save_string'+sm+'">Файл "'+file+'.cgi" сохранен.</div>').animate({opacity: "1"}, 600, function(){
						setInterval('$("div.save_maket div.save_string").animate({opacity: "0"}, 600 )', 1500, function(){
							$("div.save_maket").empty().css("opacity", "0");
						});
					});
				return false;
			}}); 
			e.preventDefault();
		}
	});

	// Обработка ctrl+enter
	var isCtrl = false;
	var isCmd = false;
	$(document).keyup(function (e) {
		if(e.which == 17) isCtrl=false;
		if(e.which == 91) isCmd=false;
	}).keydown(function (e) {
		if(e.which == 17) isCtrl=true;
		if(e.which == 91) isCmd=true;
		if(e.which == 13 && (isCtrl || isCmd)) {
			$("div#pages.template").addClass("fullscreen");
			var maketsH = parseInt($("div.makets").height())-46;
			var windowH = parseInt($(window).height()-96-maketsH);
			$("div.CodeMirror").height(windowH+"px");
			$("div.CodeMirror .CodeMirror-scroll").css("max-height", windowH+"px");
			$('html, body').animate({scrollTop:0}, 0);
			$("div#content").css("min-height", "0");
			$("body").css("overflow", "hidden");
			var params = new Object();
			params.maket_screen = "1";
			$.get(dirs_template+'/template_ajax.cgi', params);			
			e.preventDefault();
		}
	});
	
	// Обработка Esc
	$(document).keydown(function(e){
		if(e.which == 27) {
			$("div#pages.template").removeClass("fullscreen");
			$("body").css("overflow", "visible");
			$("div#content").css("min-height", "600px");
			$("div.CodeMirror").height("600px");
			$("div.CodeMirror .CodeMirror-scroll").css("max-height", "600px");
			var params = new Object();
			params.maket_screen = "0";
			$.get(dirs_template+'/template_ajax.cgi', params);			
			e.preventDefault();
		}
	});
	

	$("a.save_maket").live('click', function() {
		var el = $(this);
		$('.CodeMirror').css('background-color','#e0ffe0');
		var template = editor.getValue();
		var file = $(el).attr("file");			
		var params = new Object();
		params.file_edit = file;
		params.template_edit = template;
		$.post(dirs_template+'/template_ajax.cgi', params, function(data){
			if (data == "ok") {
				var sm="";
				if ($("div.maket div a").size() == 2){sm = " sm";}
				$('.CodeMirror').animate({'background-color': '#ffffff'});
				$("div.save_maket").empty().append('<div class="save_string'+sm+'">Файл "'+file+'.cgi" сохранен.</div>').animate({opacity: "1"}, 600, function(){
					setInterval('$("div.save_maket div.save_string").animate({opacity: "0"}, 600 )', 1500, function(){
						$("div.save_maket").empty().css("opacity", "0");
					});
				});
				return false;
			}
		});
		return false;
	});

	$("div.makets a.create").live('click', function(){
		if ($(this).attr("id") == "new" && $(this).prev("div.new").children().attr("value") == "Введите название"){
			alert("Введите название файла");
			return false;
		}
		else if ($(this).attr("id") == "new"){
			var name = $(this).prev("div.new").children().attr("value");
			var params = new Object();
			params.template_create = name;
			$.post(dirs_template+'/template_ajax.cgi', params, function(data){
				if (data != "") {
					location.replace("/cgi-bin/admin/engine/index.cgi?adm_act=template&file="+data);
				}
			});
			return false;
		}
		else {
			$(this).before('<div class="new"><input type="text" onblur="if (this.value==\'\'){this.value=\'Введите название\'}" onfocus="if (this.value==\'Введите название\') this.value=\'\';" value="Введите название"></div>');
			$(this).attr("id", "new");
			return false;
		}
	});
	
	$("a.del_maket").live('click', function(){
		var name = $("div.makets a.active").html();
		var file = $(this).attr("file");
		if (confirm('Вы хотите удалить файл "'+name+'"?')){
			var params = new Object();
			params.template_del = file;
			$.post(dirs_template+'/template_ajax.cgi', params, function(data){
				if (data != "") {
					location.replace("/cgi-bin/admin/engine/index.cgi?adm_act=template");
				}
			});
			return false;
		}
		else {return false;}
	});
		
});
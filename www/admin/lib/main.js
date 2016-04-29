var dirs = '/cgi-bin/admin/modules';

$(document).ready(function(){
		
	$(".off").easyTooltip();
	
	$("div#main_enter input").attr("value", "");
	setTimeout(function(){
		$("div#main_enter input[name=user_login]").focus();
	}, 300);
	
	$(".body_contacts div.item input.code").each(function(){
		var count = $(this).val().length;
		var size = count*7;
		if (size > 28){
			$(this).css("width", size+"px");
		}
	});	
	$(".body_contacts div.item input.code").keyup(function(){
		var count = $(this).val().length;
		var size = count*7;
		if (size > 28){
			$(this).css("width", size+"px");
		}
	});
	
	var params = {
		changedEl: "select#category",
		visRows: 10,
		scrollArrows: true
	}
	cuSel(params);	
	
	// Обработка ctrl+alt+m
	var isCtrl = false;
	var isCmd = false;
	$(document).keyup(function (e) {
		if(e.which == 17) isCtrl=false;
		if(e.which == 91) isCmd=false;
	}).keydown(function (e) {
		if(e.which == 17) isCtrl=true;
		if(e.which == 91) isCmd=true;
		if(e.which == 77 && (isCtrl || isCmd) && e.altKey) {
			$("body").append('<div id="elfinder_container"><div id="elfinder_header"><p>Файловый менеджер UpleCMS</p><span class="close"></span></div><div id="elfinder"></div></div>');
			var elf = $('#elfinder').elfinder({
				url : '/admin/js/elfinder/php/connector.php',
				lang: 'ru'
			}).elfinder('instance');
			$('html, body').animate({scrollTop:302}, 0);
			$("div#elfinder_container").draggable({handle: "div#elfinder_header"});
			e.preventDefault();
		}
	});	
	$("div#elfinder_header .close").live('click', function(){
		$("div#elfinder_container").remove();
		$("div.ui-helper-reset").remove();
		$("audio").remove();
	});

	$(function() {
		$("#date_creat").datepicker();

	});
	$(function() {
		$("#date_edit").datepicker();

	});	

	setInterval('$("#menu2 .upload").fadeIn(0)', 0);

	$("#showhidetop").click(function() {
		var params = new Object();
		params.showtop = "active";
		$.post(dirs+'/save_ajax.cgi', params, function(data){
		if(data == "1"){	
			$("#header").animate({marginTop: "-159px"}, 600 );
			$("#showhidetop").addClass("active");
			$("#showhidetop").attr("title", "Опустить");
			return false;
		} else if(data == "0"){
			$("#header").animate({marginTop: "0px"}, 600 );
			$("#showhidetop").removeClass("active");
			$("#showhidetop").attr("title", "Скрыть");			
			return false;
		}});
	});
		
	
	$("a#click_pages_new").click(function() {
		$("div.three_pages").slideUp("slow");		
		$("div#pages_new").show(1200);
		$("div#tabs li").removeClass("activetab");		
		var el = $(this).parent();
		$(el).addClass("activetab");
		return false;
	});
	
	$("a#click_pages").click(function() {
		$("div#pages_new").fadeOut("slow");	
		$("div#pages_old").css("margin", "33px 0 0 23px");
		$("div.three_pages").slideDown("slow");		
		$("div#tabs li").removeClass("activetab");		
		var el = $(this).parent();
		$(el).addClass("activetab");
		return false;
	});	
	
	$("a.ext").toggle(function() {
		var el = $(this);
		var reg = /introjs-showElement/;
		if (!$(this).attr("class").match(reg)){
			var top = window.pageYOffset ? window.pageYOffset : document.body.scrollTop;
			$(el).attr("data-scroll", top+"px");
			var scroll = $(el).offset().top-165;
			$("body, html").animate({scrollTop:scroll}, 600, function(){
				$(el).attr("data-scroll-down", window.pageYOffset ? window.pageYOffset : document.body.scrollTop);		
			});
			$("table.ext_param").fadeIn(600);
		}		
		return false;
	}, function() {
		var el = $(this);
		var reg = /introjs-showElement/;
		if (!$(this).attr("class").match(reg)){
			var top = window.pageYOffset ? window.pageYOffset : document.body.scrollTop;
			if (top == $(el).attr("data-scroll-down")){
				$("body, html").animate({scrollTop:$(el).attr("data-scroll")}, 600);
			}
			$("table.ext_param").fadeOut(400);
		}		
		return false;	
	});	

	$(".no_link a").click(function() {
		return false;	
	});	
	$("a.no_link").click(function() {
		return false;	
	});	

	setInterval('$("div.save_page").animate({opacity: "0"}, 600 ); $("div.save_page").animate({marginTop: "-48px"}, 450 )', 1500);						

	$("#edittitle").toggle(function(){
		if($("#title_site").attr("editing")!='1'){
			$("#title_site").attr("editing","1");
			$("#title_site").html('<textarea class="editor" id="editor'+$("#title_site").attr("idtext")+'">'+$("#title_site").html()+'</textarea>');
			setActionEditor($("#editor"+$("#title_site").attr("idtext")));
		}
		$(this).html("сохранить");
		
	}, function() {
		$(this).html("редактировать");
	})
	
	$("table td.name div.scroll").hover(function(){
		if ($(this).attr("class") == "scroll"){
			$(this).find("span").animate({"margin-top":"-38px"}, 250);
		}
	}, function(){
		$(this).find("span").animate({"margin-top":"0px"}, 250);
	});
	
	// $("ul.nav-pills li.disabled a").live('click', function(){
		// return false;
	// });
	// $("a.dropdown-toggle").live('click', function(){
		// var el = $(this);
		// if ($(el).parent("div.btn-group").attr("class") == "btn-group"){
			// $("div.btn-group").removeClass("open");
			// $(el).parent("div.btn-group").addClass("open");
		// }
		// else {
			// $(el).parent("div.btn-group").removeClass("open");
		// }
		// return false;
	// });
	// $("div.btn-group ul li a").live("click", function(){
		// $(this).parent().parent().parent().find("a.dropdown-toggle").children("span.value").html($(this).html());
		// $(this).parent().parent().parent("div.btn-group").removeClass("open");
		// if ($(this).parent().parent().parent("div.btn-group").attr("id") == "no-change"){
			// return true;
		// }
		// else {
			// return false;
		// }
	// });
	// $("div.btn-group button.btn").live("click", function(){
		// var el = $(this);
		// if ($(el).attr("class") == "btn"){
			// $(el).addClass("active");
		// }
		// else {
			// $(el).removeClass("active");
		// }		
	// });
	
	$("input.js-cbox").hide().after('<div class="js-cbox"></div>');
	$("input.js-cbox:checked").next().addClass("checked");
	$("div.js-cbox").click(function(){
		var input_cb = $(this).prev("input");
		if (input_cb.is(':checked'))
		{
		 $(this).removeClass("checked");
		 input_cb.attr('checked', false);
		}
		else 
		{
		 $(this).addClass("checked");
		 input_cb.attr('checked', true);
		}
	});	
	
});

function checkbox_init(wrap){

	var $wrap;
	if (wrap === undefined){$wrap = $("body");}
	else {$wrap = $(wrap);}

	$wrap.find(".checkbox__box, .radiobox__box").find("input").each(function(){
		cb_styler($(this));
	});
	
	$wrap.find(".checkbox__box").find("input").on("click", function(){
		cb_styler($(this));
	});
	
	$wrap.find(".radiobox__box").find("input").on("click", function(){
		var $input = $(this);
		var name = $input.attr("name");
		$("input[type=radio]").each(function(){
			if ($(this).attr("name") == name && !$(this).is(':checked')){
				$(this).parent().removeClass("checked");
			}
		});
		cb_styler($input);
	});	
}

function cb_styler(input){
	var $input = $(input);
	var $box = $input.parent();
	if ($input.is(':checked')){
		$box.addClass("checked");
	}
	else {
		$box.removeClass("checked");
	}
}

function setActionEditor(editor){
	editor.focus();
	editor.blur(function(){
		$(this).parent().attr("editing","");
		var params = new Object();
		params.title_site = $(this).val();
		$.post(dirs+'/save_ajax.cgi', params);
		$(this).parent().html($(this).val());
	});
}
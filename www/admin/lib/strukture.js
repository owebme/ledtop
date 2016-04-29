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
					location.replace($("div#main_menu div#pages a").attr("href"));
					e.preventDefault();
				}
			}
			else {
				return true;
			}
		}
		else if (e.which == 27){
			if (getUrlVars()["par"] == "new"){
				if (confirm('Отменить создание страницы?')) {
					location.replace($("div#main_menu div#pages a").attr("href"));
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
		params.page_lamp = $(this).parent().attr("c_id");		
		$.post(dirs_catalog+'/strukture_ajax.cgi', params, function(data){
		if(data == "1"){
			$(el).parent().removeClass("off");
			$(el).animate({opacity:1}, 0);
			$(el).attr("title", "Скрыть страницу");				
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
		if (confirm('Удалить страницу "'+name_cat+'"')) {
		$(this).parent().fadeOut("slow", function(){
			$(el).parent().remove();
		});		
		
advAJAX.post({
url: (dirs_catalog+'/strukture_ajax.cgi'),
page_del: $(el).parent().attr("c_id")
});
			return false;

		}
			return false;
	});
});


$("div#pages div.three_pages li a").live('mouseenter', function(e){
	var el = $(this);
	if (e.ctrlKey == true){
		$("div#pages div.three_page div.controls").stop(true)
		$(el).parent().children("div.controls").queue("fx", function(){
			$(el).parent().children("div.controls").fadeIn(0);
			$(this).dequeue("fx");
		});
	}
});
$("div#pages div.three_pages li").live('mouseleave', function(){
	$(this).children("div.controls").fadeOut(0);
});

$("div#pages div.three_pages li div.controls").live('mouseenter', function(){
	$(this).parent().children("a:last").addClass("hover");
});
$("div#pages div.three_pages li div.controls").live('mouseleave', function(){
	$(this).parent().children("a:last").removeClass("hover");
});

$("div#pages div.three_pages li div.controls span.choice, div#pages div.three_pages li div.controls span.reset").live('click', function(){
	var type = $(this).attr("class"); 
	$(this).parent().children("select").remove();
	$(this).prev("em").css("padding-top", "4px");
	$(this).before('<select name="mirror"><option>Загрузка разделов...</option></select>');
	var el = $(this).prev();
	$(this).remove();
	var params = new Object();
	params.load_razdel = $(el).parent().parent().parent().attr("c_id");	
	$.post(dirs_catalog+'/strukture_ajax.cgi', params, function(data){	
		if (data != ""){
			$(el).empty().append(data).addClass("active");
			$("div#pages div.three_pages li div.controls select.active").click(function(){
				$(this).parent().parent().parent().children("div.controls").addClass("open");
				$("div#pages div.three_pages li div.controls select.active").click(function(){
					var id = $(this).val();
					if (isAlphaNumeric(id) || id == "/news/" || id == "/public/" || id == "/gallery/" || id == "questions" || id == "/catalog/" || id == "/catalog/all" || id == "/poleznoe/"){
						var alias="";
						if (id == "questions"){
							alias = $(this).parent().parent().prev().attr("title");
							var alias = alias.replace(/^Страница: /, '');
						}
						var option = $(this).find(":selected").html();
						//alert(id);
						var data="";
						var params = new Object();
						if (alias != ""){
							params.mirror_link = alias;
							params.mirror_link_id = id;								
						} else {
							params.mirror_link = id;
							params.mirror_link_id = $(el).parent().parent().parent().attr("c_id");							
						}
						$.post(dirs_catalog+'/strukture_ajax.cgi', params, function(data){	
							if (data != ""){
								$(el).parent().parent().parent().children("a:last").attr("href", data).append(' <em class="mirror">(зеркало)</em>');
							}
						});
						$(this).empty().append('<option>'+option+'</option>');
						$(this).parent().parent().parent().children("div.controls").removeClass("open");
						$(this).removeClass("active");
						$(this).parent().append('<span class="reset">Сбросить</span>');
					}
				});	
			});
		}
	});
	if (type == "reset"){
		var mirror_link_id = $(el).parent().parent().parent().attr("c_id");
		var params = new Object();
		params.mirror_link = "reset";
		params.mirror_link_id = mirror_link_id;
		$.post(dirs_catalog+'/strukture_ajax.cgi', params);
		$(el).parent().parent().children("div#remove_link").children("div.cb").removeClass("checked");
		$(el).parent().parent().children("div#remove_link").children("input").attr('checked', false);
		$(el).parent().parent().children("div#remove_link").children("input[name=no]").attr('checked', true);
		$(el).parent().parent().children("div#remove_link").children("input[name=no]").next("div.cb").addClass("checked");
		$(el).parent().parent().parent().children("a:last").attr("href", "?adm_act=strukture&num_edit="+mirror_link_id).removeClass("point").children("em.mirror").remove().attr("title", "");
	}
});




$("div#pages div.three_pages li div.controls div#del div.cb").live('click', function(){
		var el = $(this);
		var params = new Object();
		params.hide_del = $(el).prev("input").attr("name");
		params.hide_del_id = $(this).parent().parent().parent().attr("c_id");		
		$.post(dirs_catalog+'/strukture_ajax.cgi', params, function(data){
		if (data == "0"){
			$(el).parent().parent().parent().children("a.del").removeClass("off");
		} else if (data == "1"){
			$(el).parent().parent().parent().children("a.del").addClass("off");		
		}});
});

$("div#pages div.three_pages li div.controls div#remove_link div.cb").live('click', function(){
		var el = $(this);
		var params = new Object();
		var remove_link_id = $(this).parent().parent().parent().attr("c_id");
		params.remove_link = $(el).prev("input").attr("name");
		params.remove_link_id = remove_link_id;		
		$.post(dirs_catalog+'/strukture_ajax.cgi', params, function(data){
		if (data == "0"){
			$(el).parent().parent().parent().children("a:last").attr("href", "?adm_act=strukture&num_edit="+remove_link_id).removeClass("point");
		} else if (data == "1"){
			$(el).parent().parent().parent().children("a:last").attr("href", "#!").attr("title", "").addClass("point");	
		}});
});

$("div#pages div.three_pages div.controls div.cb").live('click', function(){
$(this).parent().children("div.cb").removeClass("checked");
$(this).parent().children("input").attr('checked', false);   
  var input_cb = $(this).prev("input")
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
			url: (dirs_catalog+'/strukture_ajax.cgi'),
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
			url: (dirs_catalog+'/strukture_ajax.cgi'),
			cat_move_down: $(this).parent().parent().attr("c_id"),
			cat_move_pid: $(this).parent().parent().attr("c_pid"),			
			cat_move_pos: $(this).parent().parent().attr("c_pos")
		});		
			return false;
    }
});

	$("div.save_content div.cb").live('click', function() {
		var el = $(this);
		if ($(el).attr("class") == "cb checked") {$("div.save_content input.button.save").replaceWith('<a class="ajaxSave" href="#">Сохранить</a>');}
		else {$("div.save_content a.ajaxSave").replaceWith('<input type="submit" name="save" value="Сохранить" class="button save" />');}
	});
	
		var ajaxSave = function(){
		var ed = tinyMCE.get('elm1');
		ed.setProgressState(1);
        window.setTimeout(function(){ed.setProgressState(0);}, 500);
		} 
		
		$(function(){
		
			$("a.ajaxSave").live('click', function() {
				ajaxSave();			
				var ed = tinyMCE.get('elm1');
				var content = ed.getContent();
				var page_id = $("a.preview_page").attr("id");
				var params = new Object();
				params.page_id = page_id;
				if (content == "" && page_id != ""){content = "clear";}
				params.page_content = content;		
				$.post(dirs_catalog+'/strukture_ajax.cgi', params);
				return false;
			});
		});	

});

function isAlphaNumeric(input) {
    var regexp = /^[A-Za-z0-9]+$/;        
    return regexp.test(input);
}

var dirs_articles = '/cgi-bin/admin/modules';

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
					var link = $("div#main_menu div#pages a").attr("href");
					link = link.replace(/adm_act\=(.*)/g, "adm_act=articles");
					location.replace(link);
					e.preventDefault();
				}
			}
			else {
				return true;
			}
		}
		else if (e.which == 27){
			if (getUrlVars()["par"] == "new"){
				if (confirm('Отменить создание статьи?')) {
					var link = $("div#main_menu div#pages a").attr("href");
					link = link.replace(/adm_act\=(.*)/g, "adm_act=articles");
					location.replace(link);
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
		$.post(dirs_articles+'/articles_ajax.cgi', params, function(data){
		if(data == "1"){
			$(el).parent().removeClass("off");
			$(el).animate({opacity:1}, 0);
			$(el).attr("title", "Скрыть статью");				
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
		if (confirm('Удалить статью "'+name_cat+'"')) {
		$(this).parent().fadeOut("slow", function(){
			$(el).parent().remove();
		});		
		
advAJAX.post({
url: (dirs_articles+'/articles_ajax.cgi'),
page_del: $(el).parent().attr("c_id")
});
			return false;

		}
			return false;
	});
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
			url: (dirs_articles+'/articles_ajax.cgi'),
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
			url: (dirs_articles+'/articles_ajax.cgi'),
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
				$.post(dirs_articles+'/articles_ajax.cgi', params);
				return false;
			});
		});	

});

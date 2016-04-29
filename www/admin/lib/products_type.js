var dirs_catalog = '/cgi-bin/admin/modules';

$(document).ready(function(){

	$("div#sheettop li.first a").attr("href", $("div#main_menu div#products a").attr("href"));

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
				location.replace("/cgi-bin/admin/engine/index.cgi?adm_act=products_type");
				e.preventDefault();				
			}
			else {
				return true;
			}
		}		
		else if (e.which == 116){
			location.replace("/cgi-bin/admin/engine/index.cgi?adm_act=products_type");
			e.preventDefault();
		}
	});
	
	$("table#page_new input").keydown(function(e){
		if (e.which == 13){
			e.preventDefault();	
			return false;
		}		
	});
	

$("a.lamp").click(function() {
		var el = $(this);
		var params = new Object();
		params.category_lamp = $(this).parent().attr("t_id");		
		$.post(dirs_catalog+'/products_type_ajax.cgi', params, function(data){
		if(data == "1"){
			$(el).parent().removeClass("off");
			$(el).animate({opacity:1}, 0);
			$(el).attr("title", "Скрыть тип товара");				
			return false;
		} else if(data == "0"){
			$(el).parent().addClass("off");		
			$(el).animate({opacity:0.5}, 0);	
			$(el).attr("title", "Сделать активным");				
			return false;
		}});
		return false;
});



$("a.del").each(function(){
		var el = $(this);
		$(this).click(function(){
		var name_cat = $(this).parent().attr("name");
		if (confirm('Удалить тип товара "'+name_cat+'"')) {
		$(this).parent().fadeOut("slow", function(){
			$(el).parent().remove();
		});			
		
advAJAX.post({
url: (dirs_catalog+'/products_type_ajax.cgi'),
category_del: $(el).parent().attr("t_id")
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
        var curr_li = $(this).parent().parent();
        var prev_li = $(curr_li).prev();
        prev_li.insertAfter(curr_li);
				
		advAJAX.post({
			url: (dirs_catalog+'/products_type_ajax.cgi'),
			cat_move_up: $(this).parent().parent().attr("t_id"),
			cat_move_pid: $(this).parent().parent().attr("t_pid"),			
			cat_move_pos: $(this).parent().parent().attr("t_pos")			
		});			
			return false;
    }
	 
	function move_down_cat(eventObject){
	    var curr_li = $(this).parent().parent();
	    var next_li = $(curr_li).next();
	    next_li.insertBefore(curr_li);
		advAJAX.post({
			url: (dirs_catalog+'/products_type_ajax.cgi'),
			cat_move_down: $(this).parent().parent().attr("t_id"),
			cat_move_pid: $(this).parent().parent().attr("t_pid"),			
			cat_move_pos: $(this).parent().parent().attr("t_pos")
		});		
			return false;
    }
});


});

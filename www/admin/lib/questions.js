var dirs_que = '/cgi-bin/admin/modules';

$(document).ready(function(){

$("div.questions div.main div.page a").live("click", function(){
	var el = $(this);
	var label = $("div.questions div.body-que").attr("id");
	var attr = $(el).attr("class");
	if (attr != "current" && label != "loader"){
		$("div.questions div.body-que").attr("id", "loader");
		var body_width = parseFloat($("div.questions div.body-que").width());
		var body_height = parseFloat($("div.questions div.body-que").height());
		$(el).parent().children("a").removeClass("current");
		$(el).addClass("current");
		$("div.questions div.body-que").css("width", body_width);
		$("div.questions div.body-que").css("height", body_height+7);
		$("div.questions div.body-que").empty().append('<div class="ajax"></div>');
		var page = $(el).html();
		var pages_count = $(el).attr("id");
		setTimeout(function(){
		var params = new Object();
		params.page = page;
		params.pages_count = pages_count;
		$.post(dirs_que+'/questions_ajax.cgi', params, function(data){
			if (data != ""){		
				$("div.questions div.body-que").empty().append(data);
				$("div.questions div.body-que").css("height", "auto");
				$("div.questions div.body-que").attr("id", "");
			}
		});
		}, 500);
	}
	else {
		return false;	
	}	
	return false;
});

$("div.questions div.send_form button.send_que").live("click", function(){
	var que_id = $(this).parent().parent().attr("send_id");
	var q_name = $(this).prev().prev("input").val();
	var q_html = $(this).prev("textarea").val();
	q_html = q_html.replace(/^\s+/,"");
	q_html = q_html.replace(/\s+$/,"");
	if (q_html != ""){
		$("div.questions div.send_form").fadeOut(600);
		var params = new Object();
		params.que_id = que_id;
		params.name = q_name;
		params.message = q_html;
		$.post(dirs_que+'/questions_ajax.cgi', params, function(data){
			if (data != ""){
				$("div.questions div.item").each(function(){
					var el = $(this);
					if ($(el).attr('que_id') == que_id) {
						$(el).attr("id", "");
						$(el).after(data);
						$(el).next().fadeIn(600);
					}
				});
				$("div.questions div.body-que").css("height", "auto");
			}
		});
	}
	else {
		return false;
	}

});

$("div.questions div.item a.answer").live("click", function(){
	var que_id = $(this).parent().attr("que_id");
	$(this).parent().attr("id", "active");
	$(this).next().fadeOut(0);
	$(this).fadeOut(0);	
	$("div.questions div.send_form").fadeIn(600);
	$("div.questions div.send_form textarea").focus();
	$("div.questions div.send_form").attr("send_id", que_id);
	return false;
});

$("div.questions div.item").live('mouseover mouseout', function(e){
	if (e.type == 'mouseover'){
		var id = $(this).attr('que_id');
		$("div.questions div.item a.del").each(function(){
			if( $(this).attr('del_id') == id) $(this).fadeIn(0);
		});
	} else if (e.type == 'mouseout'){
        $("div.questions div.item a.del").stop(true, true);	
		$("div.questions div.item a.del").each(function(){
			if( $(this).attr('del_id') != id) $(this).fadeOut(0);
		});
	}
});	


$("div.questions div.item a.del").live("click", function(){
	var el = $(this);
	var que_class = $(this).parent().attr("class");
	var que_id = $(this).attr("del_id");
	if ($(el).parent().next().attr("class") == "item answer"){
		$(el).parent().next().fadeOut(600, function(){
			$(el).parent().next().remove();
		});
	}
	$(this).parent().fadeOut(600, function(){
		$(el).parent().remove();
	});	
	$("div.questions div.body-que").css("height", "auto");
	if (que_class == "item answer"){
		$(el).parent().prev().attr("id", "no_answer");
		$(el).parent().prev().append('<a class="answer" href="#">Ответить</a>');
	}
	var params = new Object();
	params.que_del = que_id;	
	$.post(dirs_que+'/questions_ajax.cgi', params);
	
	return false
});


});	
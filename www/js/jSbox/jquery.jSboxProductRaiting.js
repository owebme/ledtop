$(function(){

jQuery.fn.ProductRaiting = function() {
	if ($("div.raiting_star").length){
		$("div.raiting_star div.raiting").each(function(){
			var raiting = $(this).attr("p_raiting");
			var p_id = $(this).attr("p_id");
			var star_width = raiting*19;
			$(this).children(".raiting_votes").width(star_width);
			var voted = $.cookie("products_"+p_id);
			if (voted == null){
				$(".raiting[p_id="+p_id+"]").attr("title", "Поставить оценку");
				$(".raiting[p_id="+p_id+"]").hover(function(){
					$(this).children(".raiting_hover").show(0);
					$(this).children(".raiting_votes").hide(0);
				},
				function(){
					$(this).children(".raiting_hover").hide(0);
					$(this).children(".raiting_votes").show(0);
				});
				$(".raiting[p_id="+p_id+"]").mousemove(function(e){
					var margin = $(".raiting").offset();
					var width_votes = e.pageX - margin.left;
					if (width_votes == 0) {width_votes = 1;}
					var user_votes = Math.ceil(width_votes/19);  
					$(this).children(".raiting_hover").width(user_votes*19);
				});	

				$(".raiting[p_id="+p_id+"]").live("click", function(){
					var el = $(this);
					if ($(el).attr("id") != "no_active"){
						var p_id = $(el).attr("p_id");
						var total_votes = parseInt($(el).next(".raiting_info").children("span").html());
						var user_votes = Math.ceil($(el).children(".raiting_hover").width()/19); 
						$(".raiting[p_id="+p_id+"]").attr("id", "no_active");
						var params = new Object();
						params.raiting = user_votes;
						params.raiting_id = p_id;
						$.post('/cgi-bin/product_ajax.cgi', params, function(data){
							if (data != ""){
								$.cookie('products_'+p_id, '1', {expires: 1, path: '/'});
								$(el).children(".raiting").unbind();
								$(el).children(".raiting_hover").hide();
								$(el).next(".raiting_info").children("span").html(total_votes+1);
								$(el).replaceWith(data);
								$("div.raiting_star div.raiting[p_id="+p_id+"]").each(function(){
									var raiting = $(this).attr("p_raiting");
									var star_width = raiting*19;
									$(this).children(".raiting_votes").width(star_width);
									$(this).css("cursor", "default");
								});
							}
						});
					}
				});
			}
			else {
				$(this).css("cursor", "default");
			}
		});
	}
}
	
$().ProductRaiting();
	
});
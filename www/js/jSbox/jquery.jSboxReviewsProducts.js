$(function(){

jQuery.fn.ProductReviews = function() {
	if ($("#products_reviews_wrap").length){	
		var p_id = $("#products_reviews_send").find(".raiting_star").attr("data-id");
		var voted = $.cookie("products_"+p_id);
		if (voted == null){
			var $rait = $("#products_reviews_send").find(".raiting_star");
			$rait.hover(function(){
				$(this).children(".raiting_hover").show(0);
				$(this).children(".raiting_votes").hide(0);
			},
			function(){
				$(this).children(".raiting_hover").hide(0);
				$(this).children(".raiting_votes").show(0);
			});
			$rait.mousemove(function(e){
				var margin = $(this).offset();
				var width_votes = e.pageX - margin.left;
				if (width_votes == 0) {width_votes = 1;}
				var user_votes = Math.ceil(width_votes/29);  
				$(this).children(".raiting_hover").width(user_votes*29);
			});
			$rait.live("click", function(){
				var votes = Math.ceil($(this).children(".raiting_hover").width()/29); 
				var star_width = votes*29;
				$(this).children(".raiting_hover").hide();				
				$(this).children(".raiting_votes").width(star_width).show(0);
				$rait.attr("data-raiting", votes);
			});
			$("#products_reviews_send").find(".send").find(".button").live("click", function(){
				var raiting = $rait.attr("data-raiting");
				var name = $("#products_reviews_send").find("input[name=name]").val();
				var text = $("#products_reviews_send").find("textarea").val();
				if (raiting < 1 || raiting == ""){alert("Поставьте оценку товару");}
				else if (text.length < 5){alert("Оставьте комментарий");}
				else if (name.length < 2){alert("Укажите Имя");}
				else {
					$("#products_reviews_send").fadeOut(200);
					var params = new Object();
					params.reviews_raiting_id = p_id;
					params.reviews_raiting = raiting;
					params.reviews_raiting_name = name;
					params.reviews_raiting_text = text;
					$.post('/cgi-bin/product_ajax.cgi', params, function(data){
						if (data == "ok"){
							$.cookie('products_'+p_id, '1', {expires: 1, path: '/'});
							$("#products_reviews_container").find("p.note").remove();
							$("#products_reviews_container").prepend('<p style="display:none" class="note">Спасибо за ваш отзыв, после прохождения модерации он будет размещен.</p>');							
							$("#products_reviews_container").find("p.note").fadeIn(400);
						}
					});
				}
			});		
			$(".add_show_reviews").live("click", function(){
				$("#products_reviews_send").find("input[name=name]").val("");
				$("#products_reviews_send").find("textarea").val("");		
				$("#products_reviews_send").fadeIn(0);
				$(this).remove();
				return false;
			});
		}
		else {
			$(".add_show_reviews").remove();
		}
	}	
}
	
$().ProductReviews();
	
});
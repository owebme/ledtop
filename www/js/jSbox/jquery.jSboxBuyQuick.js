(function($) {	
    $.fn.jSboxBuyQuick = function(opt) {
		opt = jQuery.extend({
			width : 433,
			speed : 0,
			theme : "green",
			border : true,
			borderWidth : 6,
			box : ".buy-quick-container"
				}, opt);	
	
		$(this).live('click', function(e){
			var jSbox="";
			var widthBox = opt.width;
			var scrollTop = window.pageYOffset ? window.pageYOffset : document.body.scrollTop;
			var marginLeft = -(widthBox/2);
			var id = $(this).attr("p_id");
			
			clearInterval(loadingTimer);
			loadingTimer = setInterval(jSbox_loading, 66);

			if (opt.ajax){
				$.ajax({
				  async: false,
				  url: opt.ajax,
				  type: "GET",
				  success : function(data) {
					$(opt.box).remove();
					$("body").append(data);
				  }
				});
			}			
			$(opt.box).attr("id", "jSbox");
			var content = $(opt.box).html();
			$(opt.box).empty();
			var height="";
			if (opt.height){height = "height:"+opt.height+"px; overflow:hidden;";}			
			if (opt.border){
				jSbox += '<div id="jSbox-popup" class="border '+opt.theme+'" style="margin-left:'+marginLeft+'px">';
				jSbox += '<div id="jSbox-wrap" style="width:'+widthBox+'px; margin:'+opt.borderWidth+'px; '+height+'">';		
			} else {
				jSbox += '<div id="jSbox-popup" class="'+opt.theme+'" style="margin-left:'+marginLeft+'px">';
				jSbox += '<div id="jSbox-wrap" style="width:'+widthBox+'px; '+height+'">';
			}
			jSbox += '<div id="jSbox-container">';
			jSbox += content;
			jSbox += '</div></div></div>';

			var windowH = $(window).height();			
			var marginTopAjax = (windowH-40)/2;
			var marginLeftAjax = -(40/2);
			$("body").append('<div id="jSbox-overlay"></div><div id="jSbox-loading" style="top:'+scrollTop+'px; margin:'+marginTopAjax+'px 0px 0px '+marginLeftAjax+'px"></div>'+jSbox);
			
			var heightBox = $("div#jSbox-popup").height();
			var top_popup ="40px"; var marginTop_popup ="0";
			if (windowH > heightBox+40){top_popup = (windowH-heightBox)/2;}

			$("div#jSbox-popup").css({'top':scrollTop,'margin-top':top_popup});
			
			$(window).resize(function() {
				jSbox_center();
			});
				
			window.setTimeout(function(){
				$("div#jSbox-loading").remove();
				$("div#jSbox-overlay").fadeIn(200, function(){
					$("div#jSbox-popup").fadeIn(200);
				});

				$("#jSbox-container input.text").autoClear();
				var value = $("#jSbox-container input.text[name=PHONE]").attr("value");
				$("#jSbox-container input.text[name=PHONE]").mask("(999) 999-99-99");
				$("#jSbox-container input.text[name=PHONE]").attr("value", value);
				
			}, opt.speed);
			
			return false;
		});
		
		$("div#jSbox-container input[type=submit].buy-quick-send").live("click", function(e){
			var hBox = $("div#jSbox-wrap").height();
			var name = $("div#jSbox-container input[name=NAME]").attr("value");
			var phone = $("div#jSbox-container input[name=PHONE]").attr("value");
			var id = $("div#jSbox-container input[name=ID]").attr("p_id");
				
			if (name != "" && name != "¬ведите" && phone != "" && phone != "¬ведите"){			
				var params = new Object();
				params.name = name;
				params.phone = phone;
				params.buy_quick = id;
				$.get("/cgi-bin/send_buy_quick.cgi", params, function(data){
					if (data != ""){
						$("div#jSbox-wrap").css("height", hBox+"px");
						$("div#jSbox-wrap").append('<div id="jSbox-message-send">'+data+'</div>');
						$("div#jSbox-wrap div#jSbox-container").fadeOut(400, function(){
							$("div#jSbox-wrap div#jSbox-message-send").fadeIn(600, function(){
								window.setTimeout(function(){
									$().jSboxClose();
								}, 2500);
							});
						});
					}
				});			
			}
			else {
				return false;
			}
			e.preventDefault();
		});			
		
		function jSbox_center() {
			var heightBox = $("div#jSbox-popup").height();
			var windowH = $(window).height();
			var top_popup ="40px"; var marginTop_popup ="0";
			if (windowH > heightBox+40){top_popup = (windowH-heightBox)/2;}
			$("div#jSbox-popup").css({'margin-top':top_popup});
		};

		var loadingTimer, loadingFrame = 1;
		
		function jSbox_loading() {
			$('#jSbox-loading').css('background-position', '0px ' + (loadingFrame * -40) + 'px');
			loadingFrame = (loadingFrame + 1) % 12;
		};

		$("div#jSbox-overlay, a.submit.jSbox-close").live('click', function(){
			$().jSboxClose();
			return false;
		});
		
		$(document).keydown(function(e){
			if (e.which == 27){
				$().jSboxClose();
				return false;
			}
		});	
    }
	
	$.fn.jSboxClose = function() {
		$("div#jSbox").html($("div#jSbox-container").html());		
		$("div#jSbox-overlay").fadeOut(200);
		$("div#jSbox-popup").fadeOut(200, function(){
			$("div#jSbox-popup").remove();
			$("div#jSbox-overlay").remove();
		});
	}

})(jQuery);
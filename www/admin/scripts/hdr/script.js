$(function(){

	if ($("div.foto_settings").length){
	
		// Регулировка HDR
	
		$("div.foto_settings div.hdr_set a.control").live("click", function(){
			var el = $("div.foto_settings div.hdr_set");
			if ($(el).attr("id") == "off"){
				$("div#slider_hdr").removeClass("off").slider({value:80});
				$("div.widget.hdr input").val("80%").removeClass("off");
				$("div.hdr_set").addClass("change").append('<div class="hdr_on"></div>');
				$("div.hdr_set div.hdr_on").fadeIn(200, function(){
					$("div.hdr_set").attr("id", "on").removeClass("change");
					$(this).remove();
				});
				$("div#slider_contrast").slider({value:0});
				$("div.widget.contrast input").val("OFF").addClass("off");
				$("div#slider_contrast").addClass("off");
				$("div.foto_settings div.checkbox input[name=normalize]").attr('checked', false);	
				$("div.foto_settings div.checkbox input[name=normalize]").next().removeClass("checked");				
			}
			else if ($(el).attr("id") == "on"){
				$("div#slider_hdr").addClass("off").slider({value:0});
				$("div.widget.hdr input").val("OFF").addClass("off");
				$("div.hdr_set").addClass("change").append('<div class="hdr_off"></div>');
				$("div.hdr_set div.hdr_off").fadeIn(200, function(){
					$("div.hdr_set").attr("id", "off").removeClass("change");
					$(this).remove();
				});
			}
			return false;
		});
	
		// Регулировка силы HDR (слайдер)
		
		var val_hdr = $("div.widget.hdr input").val();
		if (val_hdr == "OFF"){
			val_hdr = 0;
		}
		else {val_hdr = parseInt(val_hdr.replace(/\%/g, ''));}
		$("div#slider_hdr").slider({
			value:val_hdr,
			min: 0,
			max: 150,
			step: 1,
			range: "min",
			slide: function(event, ui){
				if (ui.value > 0){
					$("div.widget.hdr input").val(ui.value + "%").removeClass("off");
					$("div#slider_hdr").removeClass("off");
					if ($("div.hdr_set").attr("id") == "off" && $("div.hdr_set").attr("class") != "hdr_set change"){
						$("div.hdr_set").addClass("change").append('<div class="hdr_on"></div>');
						$("div.hdr_set div.hdr_on").fadeIn(200, function(){
							$("div.hdr_set").attr("id", "on").removeClass("change");
							$(this).remove();
						});
					}
					$("div#slider_contrast").slider({value:0});
					$("div.widget.contrast input").val("OFF").addClass("off");
					$("div#slider_contrast").addClass("off");
					$("div.foto_settings div.checkbox input[name=normalize]").attr('checked', false);	
					$("div.foto_settings div.checkbox input[name=normalize]").next().removeClass("checked");					
				}
				else if (ui.value == 0){
					$("div.widget.hdr input").val("OFF").addClass("off");
					$("div#slider_hdr").addClass("off");
					if ($("div.hdr_set").attr("id") == "on" && $("div.hdr_set").attr("class") != "hdr_set change"){
						$("div.hdr_set").addClass("change").append('<div class="hdr_off"></div>');
						$("div.hdr_set div.hdr_off").fadeIn(200, function(){
							$("div.hdr_set").attr("id", "off").removeClass("change");
							$(this).remove();
						});
					}
				}
			}
		});
		$("div.widget.hdr input").val($("div#slider_hdr").slider("value") + "%");
		if ($("div#slider_hdr").slider("value") == "0"){
			$("div.widget.hdr input").val("OFF").addClass("off");
			$("div#slider_hdr").addClass("off");
			$("div.hdr_set").attr("id", "off");		
		}		
		
		// Регулировка насыщенности (слайдер)
		
		var val_saturation = $("div.widget.saturation input").val();
		if (val_saturation == "OFF"){
			val_saturation = 0;
		}		
		else if (val_saturation == "Ч/Б"){
			val_saturation = -100;
		}
		else {val_saturation = parseInt(val_saturation.replace(/\+/g, ''));}
		$("div#slider_saturation").slider({
			value:val_saturation,
			min: -100,
			max: 100,
			step: 1,
			range: "min",
			slide: function(event, ui){
				$("div#slider_saturation").removeClass("off").removeClass("zero");
				$("div.widget.saturation input").removeClass("off");
				$("div.widget.saturation a.reset").fadeIn(200);
				if (ui.value > 0){
					$("div.widget.saturation input").val("+" + ui.value);
				}
				else if (ui.value < 0){
					$("div.widget.saturation input").val(ui.value);
				}
				else if (ui.value == 0){
					$("div.widget.saturation input").val("OFF").addClass("off");
					$("div#slider_saturation").addClass("zero").addClass("off");
				}			
				if (ui.value == "-100"){
					$("div.widget.saturation input").val(ui.value);
					$("div#slider_saturation").addClass("off");
					$("div.widget.saturation input").val("Ч/Б").addClass("off");
				}
			}
		});
		if (parseInt($("div#slider_saturation").slider("value")) > 0){
			$("div.widget.saturation input").val("+" + $("div#slider_saturation").slider("value"));
		}
		else if ($("div#slider_saturation").slider("value") == "-100"){
			$("div#slider_saturation").addClass("off");
			$("div.widget.saturation input").val("Ч/Б").addClass("off");	
		}		
		else if (parseInt($("div#slider_saturation").slider("value")) < 0){
			$("div.widget.saturation input").val($("div#slider_saturation").slider("value"));
		}
		else if ($("div#slider_saturation").slider("value") == 0){
			$("div#slider_saturation").addClass("zero").addClass("off");
			$("div.widget.saturation input").val("OFF").addClass("off");
		}
		if ($("div#slider_saturation").slider("value") != 0){
			$("div.widget.saturation a.reset").fadeIn(0);
		}
		
		// Сброс насыщенности
		
		$("div.widget.saturation a.reset").live("click", function(){
			$(this).fadeOut(200);
			$("div#slider_saturation").slider({value:0});
			$("div.widget.saturation input").val("OFF").addClass("off");
			$("div#slider_saturation").addClass("zero").addClass("off");
			return false;
		});		

		// Регулировка контрастности (слайдер)
		
		var intervalTimer="";
		var val_contrast = $("div.widget.contrast input").val();
		if (val_contrast == "OFF"){
			val_contrast = -100;
		}
		else {val_contrast = parseInt(val_contrast.replace(/\+/g, ''));}
		$("div#slider_contrast").slider({
			value:val_contrast,
			min: 0,
			max: 100,
			step: 1,
			range: "min",
			slide: function(event, ui){
				if (ui.value > 0){
					$("div.widget.contrast input").val("+" + ui.value);
					$("div#slider_contrast").removeClass("off");
					$("div#slider_hdr").slider({value:0});
					$("div.widget.hdr input").val("OFF").addClass("off");
					$("div#slider_hdr").addClass("off");
					if ($("div.hdr_set").attr("id") == "on"){
						$("div.hdr_set").addClass("change").append('<div class="hdr_off"></div>');
						$("div.hdr_set div.hdr_off").fadeIn(200, function(){
							$("div.hdr_set").attr("id", "off").removeClass("change");
							$(this).remove();
						});
					}
					if ($("div.hdr_set").attr("id") == "on" && $("div.foto_settings div.pointer2").attr("class") != "pointer2 show"){
						$("div.foto_settings div.test_image").animate({opacity:"0"}, 200);
						$("div.foto_settings div.pointer2").addClass("show");
						$("div.foto_settings div.pointer1").fadeOut(200);
						$("div.hdr_set div.notic").fadeIn(200, function(){
							var el = $(this);
							clearInterval(intervalTimer);
							intervalTimer = setTimeout(function(){
								$(el).fadeOut(400);
								$("div.foto_settings div.pointer2").fadeOut(400);
								$("div.foto_settings div.test_image").animate({opacity:"1"}, 400);								
							}, 5000);
						});
						$("div.foto_settings div.pointer2").fadeIn(0).animate({height:"105px"}, 400);						
					}					
				}
				else if (ui.value == 0){
					$("div.widget.contrast input").val("OFF").addClass("off");
					$("div#slider_contrast").addClass("off");
				}
			}
		});
		$("div.widget.contrast input").val("+" + $("div#slider_contrast").slider("value"));
		if ($("div#slider_contrast").slider("value") == 0){
			$("div.widget.contrast input").val("OFF").addClass("off");
			$("div#slider_contrast").addClass("off");
		}
		
		// Чекбоксы
		
		$("div.foto_settings div.checkbox input").hide().after('<div class="js-box"></div>');
		$("div.foto_settings div.checkbox input:checked").next().addClass("checked");
		$("div.foto_settings div.js-box").click(function(){
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
			 if ($(this).parent().attr("class") == "checkbox normalize"){
				$("div#slider_hdr").slider({value:0});
				$("div.widget.hdr input").val("OFF").addClass("off");
				$("div#slider_hdr").addClass("off");
				if ($("div.hdr_set").attr("id") == "on"){
					$("div.hdr_set").addClass("change").append('<div class="hdr_off"></div>');
					$("div.hdr_set div.hdr_off").fadeIn(200, function(){
						$("div.hdr_set").attr("id", "off").removeClass("change");
						$(this).remove();
					});
				}
				if ($("div.hdr_set").attr("id") == "on" && $("div.foto_settings div.pointer1").attr("class") != "pointer1 show"){
					$("div.foto_settings div.test_image").animate({opacity:"0"}, 200);
					$("div.foto_settings div.pointer1").addClass("show");
					$("div.foto_settings div.pointer2").fadeOut(200);
					$("div.hdr_set div.notic").fadeIn(200, function(){
						var el = $(this);
						clearInterval(intervalTimer);
						intervalTimer = setTimeout(function(){
							$(el).fadeOut(400);
							$("div.foto_settings div.pointer1").fadeOut(400);
							$("div.foto_settings div.test_image").animate({opacity:"1"}, 400);
						}, 5000);
					});
					$("div.foto_settings div.pointer1").fadeIn(0).animate({height:"105px"}, 400);
				}
			 }
			}
		});
		
		// Восстановить настройки по умолчанию
		
		var hdr_set = $("div.foto_settings input[name=hdr]").val();
		var saturation_set = $("div.foto_settings input[name=saturation]").val();
		var contrast_set = $("div.foto_settings input[name=contrast]").val();
		var sharpness_set=""; if ($("div.foto_settings input[name=sharpness]").is(':checked')){sharpness_set="on";}
		var normalize_set=""; if ($("div.foto_settings input[name=normalize]").is(':checked')){normalize_set="on";}

		if (hdr_set != "80%" || saturation_set != "OFF" || contrast_set != "OFF" || sharpness_set != "on" || normalize_set != ""){

			$("div.foto_settings").prepend('<a href="#" class="default">Восстановить настройки</a>');
			
			$("div.foto_settings a.default").live("click", function(){
				$(this).fadeOut(200);			
				$("div#slider_hdr").removeClass("off").slider({value:80});
					$("div.widget.hdr input").val("80%").removeClass("off");
					if ($("div.hdr_set").attr("id") == "off"){
						$("div.hdr_set").addClass("change").append('<div class="hdr_on"></div>');
						$("div.hdr_set div.hdr_on").fadeIn(200, function(){
							$("div.hdr_set").attr("id", "on").removeClass("change");
							$(this).remove();
						});
					}
				$("div#slider_saturation").addClass("zero").addClass("off").slider({value:0});
					$("div.widget.saturation input").val("OFF").addClass("off");
				$("div#slider_contrast").addClass("off").slider({value:0});
					$("div.widget.contrast input").val("OFF").addClass("off");
				$("div.foto_settings div.checkbox input[name=sharpness]").attr('checked', true);	
					$("div.foto_settings div.checkbox input[name=sharpness]").next().addClass("checked");
				$("div.foto_settings div.checkbox input[name=normalize]").attr('checked', false);	
					$("div.foto_settings div.checkbox input[name=normalize]").next().removeClass("checked");
				
				return false;
			});
		}
	}
	
});
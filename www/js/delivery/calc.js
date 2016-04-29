$(function(){
	var $formParamsDelivery = $("#formParamsDelivery"),
		$cityDelivery = $formParamsDelivery.find("#cityDelivery"),
		$sendParamsDelivery = $formParamsDelivery.find("#sendParamsDelivery");
	
	$cityDelivery.autocomplete({
		source : function(request, response) {
			$sendParamsDelivery.css("visibility", "hidden");
			$.ajax({
				url : "http://api.cdek.ru/city/getListByTerm/jsonp.php?callback=?",
				dataType : "jsonp",
				data : {
					q : function() {						
						return $cityDelivery.val()
					},
					name_startsWith : function() {
						return $cityDelivery.val()
					}
				},
				success : function(data) {					
					response($.map(data.geonames, function(item) {
						return {
							label : item.name,
							value : item.name,
							id : item.id
						}
					}));
				}
			});
		},
		minLength : 1,
		select : function(event, ui) {
			$('#receiverCityId').val(ui.item.id);
			$sendParamsDelivery.css("visibility", "visible");
		}
	});	
	
	$formParamsDelivery.find(".result-block").find("input").each(function(){
		var value = $(this).data("value");
		$(this).val(value);
	});
	
	$sendParamsDelivery.on("click", function(){
		$sendParamsDelivery.before('<img class="ajax" src="/img/ajax-loader_lite.gif">');
		$sendParamsDelivery.css("visibility", "hidden");
		var formData = form2js('formParamsDelivery', '.', true, function(node) {
			if (node.id && node.id.match(/callbackTest/)) {
				return {
					name : node.id,
					value : node.innerHTML
				};
			}
		});
		var formDataJson = JSON.stringify(formData);
		//console.log(JSON.stringify(formData));

		$.ajax({
			url : 'http://api.cdek.ru/calculator/calculate_price_by_jsonp.php',
			jsonp : 'callback',
			data : {
				"json" : formDataJson
			},
			type : 'GET',
			dataType : "jsonp",
			success : function(data) {
				//console.log(data);
				$sendParamsDelivery.prev(".ajax").remove();
				$sendParamsDelivery.css("visibility", "visible");
				$formParamsDelivery.find(".result-error").remove();
				if (data.hasOwnProperty("result")) {
					$formParamsDelivery.find(".order-delivery-result").show(0);
					$formParamsDelivery.find(".order-delivery-result").html('<div class="order-delivery-total">Cтоимость доставки до двери &mdash; <span>' + data.result.price + ' руб.</span></div>'
					+'<div class="order-delivery-total">Срок доставки &mdash; <span>' + data.result.deliveryPeriodMin + ' &ndash; ' + data.result.deliveryPeriodMax + ' дн.</span></div>'
					+'<div class="order-delivery-total">Планируемая дата доставки &mdash; <span>c ' + data.result.deliveryDateMin + ' по ' + data.result.deliveryDateMax + '</span></div>');					
					$formParamsDelivery.find(".result-block").show(0);
				} else {
					for (var key in data["error"]) {
						$formParamsDelivery.find(".order-delivery-result").hide(0);
						$formParamsDelivery.find(".result-block").before('<div class="result-error">' + data["error"][key].text + '</div>');
					}
				}
			}
		});
		return false;
	});	
});
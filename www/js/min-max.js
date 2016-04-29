$(function(){

	var $slider = $("#slider");
	if ($slider.length){
	
		var $minCost = $("input#minCost");
		var $maxCost = $("input#maxCost");

		var price_from = parseInt($("#price_from").text())*1;
		var price_to = parseInt($("#price_to").text())*1;

		$slider.slider({
			min: price_from,
			max: price_to,
			values: [$minCost.val(), $maxCost.val()],
			range: true,
			stop: function(event, ui) {
				$minCost.val($slider.slider("values",0));
				$maxCost.val($slider.slider("values",1));
			},
			slide: function(event, ui){
				$minCost.val($slider.slider("values",0));
				$maxCost.val($slider.slider("values",1));
			}
		});
		$minCost.change(function(){
			var value1 = $minCost.val();
			var value2 = $maxCost.val();
			if (parseInt(value1) > parseInt(value2)){
				value1 = value2;
				$minCost.val(value1);
			}
			$slider.slider("values",0,value1);
		});
		$maxCost.change(function(){
			var value1 = $minCost.val();
			var value2 = $maxCost.val();
			if (value2 > 10000) {
				value2 = 10000;
				$maxCost.val(10000);
			}
			if (parseInt(value1) > parseInt(value2)){
				value2 = value1;
				$maxCost.val(value2);
			}
			$slider.slider("values",1,value2);
		});

		$(".filter-form input").keyup(function(event){
			var key, keyChar;
			if (!event) var event = window.event;
			if (event.keyCode) key = event.keyCode;
			else if (event.which) key = event.which;
			if (key==null || key==0 || key==8 || key==13 || key==9 || key==46 || key==37 || key==39 ) return true;
			keyChar=String.fromCharCode(key);
			if (!/\d/.test(keyChar)) return false;
		});
	}
	
});
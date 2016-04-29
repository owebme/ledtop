	
	function imgCropSet (imgWidth, imgHeight, cordX2, cordY2){	
		var selectX1 = 0;
		var selectY1 = 0;	
		var selectX2="";
		var selectY2="";
		if (imgHeight > cordX2){
			var def = imgHeight/cordY2
			selectY2 = parseInt(imgHeight);
			selectX2 = parseInt((def*cordX2).toFixed(0));
			if (selectX2 > imgWidth){
				var def = imgWidth/cordX2
				selectX2 = parseInt(imgWidth);
				selectY2 = parseInt((def*cordY2).toFixed(0));
			}
		} else {selectX2 = cordX2; selectY2 = cordY2;}
		
		if (selectX2 < imgWidth){
			selectX1 = parseInt(((imgWidth-selectX2)/2).toFixed(0));
		}
		if (selectY2 < imgHeight){
			selectY1 = parseInt(((imgHeight-selectY2)/2).toFixed(0));
		}	
		
		imgCrop(cordX2, cordY2);
		$('div.resize_format img#photo').imgAreaSelect({
			fadeSpeed: true,
			x1: selectX1, y1: selectY1, x2: selectX2+selectX1, y2: selectY2+selectY1,
		});
		
		$('div.resize_format input[name=x1]').attr("value", selectX1);
		$('div.resize_format input[name=y1]').attr("value", selectY1);
		$('div.resize_format input[name=x2]').attr("value", selectX2+selectX1);
		$('div.resize_format input[name=y2]').attr("value", selectY2+selectY1);
		$('div.resize_format input[name=cropW]').attr("value", selectX2);
		$('div.resize_format input[name=cropH]').attr("value", selectY2);
	}

	function imgCrop(imgW, imgH){

		var ratio = imgW/imgH;

		$('div.resize_format img#photo').imgAreaSelect({
			aspectRatio: ratio+':1',
			keys: true,
			handles: true,
			onSelectEnd: function ( image, selection ) {
				$('div.resize_format input[name=x1]').val(selection.x1);
				$('div.resize_format input[name=y1]').val(selection.y1);
				$('div.resize_format input[name=x2]').val(selection.x2);
				$('div.resize_format input[name=y2]').val(selection.y2);
				$('div.resize_format input[name=cropW]').val(selection.width);
				$('div.resize_format input[name=cropH]').val(selection.height);
			}
		}); 
	}

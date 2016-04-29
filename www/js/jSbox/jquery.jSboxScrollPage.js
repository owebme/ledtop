$(function(){
	
	if ($("div.pages.wide").length){
		var wrapper = $("div.pages div.container");
		var wrapper_top = $("div.pages.top div.container");
		var wrapper_bottom = $("div.pages.bottom div.container");
		var scrollable = $("div.pages div.container div.width");
		var count_page = $("div.pages.bottom div.container div.width").children("a").length;
		var sizeWidth = parseInt(count_page-9)*24+(9*17)+2;
		$(scrollable).css("width", sizeWidth+"px");
		var inactiveMargin = 80;					
		var wrapperWidth = wrapper.width();
		var wrapperHeight = wrapper.height();
		var scrollableWidth = scrollable.outerWidth() + 2*inactiveMargin;
		wrapper_top.scrollLeft(0);
		wrapper_bottom.scrollLeft(0);
		if ($("div.pages.top").length){
			wrapper_top.mousemove(function(e){
				lastTarget = e.target;
				var wrapperOffset = wrapper_top.offset();		
				var left = (e.pageX - wrapperOffset.left) * (scrollableWidth - wrapperWidth) / wrapperWidth - inactiveMargin;
				if (left < 0){
					left = 0;
				}
				wrapper_top.scrollLeft(left);
				wrapper_bottom.scrollLeft(left);
			});	
		}
		if ($("div.pages.bottom").length){
			wrapper_bottom.mousemove(function(e){
				lastTarget = e.target;
				var wrapperOffset = wrapper_bottom.offset();		
				var left = (e.pageX - wrapperOffset.left) * (scrollableWidth - wrapperWidth) / wrapperWidth - inactiveMargin;
				if (left < 0){
					left = 0;
				}
				wrapper_bottom.scrollLeft(left);
				wrapper_top.scrollLeft(left);
			});
		}
	}
	
});
(function($) {	
    $.fn.jSboxSlideShow = function(opt) {
		opt = jQuery.extend({
			pause : 5000,
			container : "#slideshow",
			item : ".unit",
			prevEffect: 'easeInSine',
			prevSpeed: 1600,
			nextEffect: 'easeInOutSine',
			nextSpeed: 1600,
			pagination : true,
			change : true,
			progress : false
				}, opt);

		var set_slideshow = parseInt($.cookie("set_slideshow"));
		curCollage = 0;
		prevCollage = 0;
		var first = $(opt.container+' '+opt.item+':first').attr("style");
		first = first.replace(/.*slides\/(.+?)\.(\w+).*/, "$1.$2");
		if (!isNaN(set_slideshow) && set_slideshow){
		  if ((set_slideshow+1) == $(opt.container+' '+opt.item).length){
			   $(opt.container).css("background", "url(/files/slides/"+first+") no-repeat");
			   curCollage = 0;
			   prevCollage = 0;          
		  }
		  else {
			   set_slideshow = parseInt(set_slideshow+2);
			   $(opt.container).css("background", "url(/files/slides/slide"+(set_slideshow+1000)+".jpg) no-repeat");
			   curCollage = set_slideshow-1;
			   prevCollage = set_slideshow-1;
		  }
		}
		else {
		  $(opt.container).css("background", "url(/files/slides/"+first+") no-repeat");
		  $.cookie('set_slideshow', "", {expires: 1, path: '/'});     
		}
		var pgInterval, pgWidth;
		var slides = $(opt.container+' '+opt.item).length;
		if (slides > 0){
			if (opt.pagination){
				var button="";
				for (i=0; i < slides; i++){
				   button +='<a setHomeCollage="'+i+'">&nbsp;</a>'; 
				}          
				$(opt.container).append('<div class="pagination">'+button+'</div>');
				$(opt.container).find(".pagination").css("z-index", "20");
			}
			$(opt.container).css("position", "relative");
			$(opt.container).find(opt.item).css({"display": "none", "position": "absolute", "top": "0px", "left": "0px", "z-index": "1"});
			if (opt.progress){
				pgWidth = $(opt.container).find(".s-progress").width();
				$(opt.container).find(".s-progress").css("width", "0px");
			}
			showHomeCollages(true);     
		}
		
		if (opt.pagination){
			$(opt.container+' .pagination a').css("cursor", "pointer");
		}
		
		var collageTimeoutID;
		var stopCollage = false;
		
		function showHomeCollages(start) {
			if ($(opt.container).attr("class") != "loading"){
				$(opt.container).addClass("loading");
				if (opt.progress){
					clearInterval(pgInterval);
				}
				window.clearTimeout(collageTimeoutID);
				var collages = $(opt.container).children(opt.item);
				if (collages.length <= 0) return;
				if (curCollage >= collages.length) curCollage = 0;
				if (start){
					$(collages[prevCollage]).fadeOut(0);
					$(collages[curCollage]).fadeIn(0);
					if (opt.progress){
						var pg = 0;
						pgInterval = setInterval(function(){
							pg = pg+1;
							if (pg < pgWidth+1){
								$(opt.container).find(".s-progress").css("width", pg+"px");
							}
						}, parseFloat(opt.pause/pgWidth));
					}				
					collageTimeoutID = window.setTimeout(showHomeCollages, opt.pause);
					$.cookie('set_slideshow', curCollage-1, {expires: 1, path: '/'});
					$(opt.container).removeClass("loading");				
				}
				else {
					if (opt.progress){
						window.setTimeout(function(){
							$(opt.container).find(".s-progress").css("width", "0px");
						}, 150);
					}
					$(collages[prevCollage]).fadeOut(opt.prevSpeed, opt.prevEffect);
					$(collages[curCollage]).fadeIn(opt.nextSpeed, opt.nextEffect, function() {
					  if (!stopCollage) {
							if (opt.progress){
								var pg = 0;
								pgInterval = setInterval(function(){
									pg = pg+1;
									if (pg < pgWidth+1){
										$(opt.container).find(".s-progress").css("width", pg+"px");
									}
								}, parseFloat(opt.pause/pgWidth));
							}
						   collageTimeoutID = window.setTimeout(showHomeCollages, opt.pause);
					  }
					  $.cookie('set_slideshow', curCollage-1, {expires: 1, path: '/'});
					  $(opt.container).removeClass("loading");
					});
					//var collagesText = $(collages[curCollage]).children('.text');
					//$(collagesText).css('right', '200px').animate({right:'25px'}, 1200);
				}
				var collagesNum = $(opt.container+' .pagination').children();
				$(opt.container+' .pagination a').removeClass('active');
				$(collagesNum[curCollage]).addClass('active');
				prevCollage = curCollage;
				curCollage = parseInt(curCollage)+1;
			}
		}
		$(opt.container+" div.pagination a").live('click', function(){
			var el = $(this);
			if ($(opt.container).attr("class") != "loading"){
				curCollage = $(el).attr("setHomeCollage");
				if (!opt.change){stopCollage = true;}
				$.cookie('set_slideshow', curCollage, {expires: 1, path: '/'});
				if (opt.progress){
					clearInterval(pgInterval);				
				}				
				showHomeCollages();		
			}
		});
	}	
})(jQuery);
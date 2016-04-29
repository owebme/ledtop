(function($) {                                          // Compliant with jquery.noConflict()
$.fn.jCarouselLite = function(o) {
    o = $.extend({
        btnPrev: null,
        btnNext: null,
        btnGo: null,
        mouseWheel: false,
        auto: null,

		speed: 350,
        easing: "easeOutSine",
		yaimagesUpload: true,

        vertical: false,
        circular: false,
        visible: 4,
        start: 0,
        scroll: 2,

        beforeStart: null,
        afterEnd: null
    }, o || {});

    return this.each(function() {                           // Returns the element collection. Chainable.

        var running = false, animCss=o.vertical?"top":"left", sizeCss=o.vertical?"height":"width";
        var div = $(this), ul = $("ul", div), tLi = $("li", ul), tl = tLi.size(), v = o.visible;

        if(o.circular) {
            ul.prepend(tLi.slice(tl-v-1+1).clone())
              .append(tLi.slice(0,v).clone());
            o.start += v;
        }

        var li = $("li", ul), itemLength = li.size(), curr = o.start;
        div.css("visibility", "visible");

        li.css({overflow: "hidden", float: o.vertical ? "none" : "left"});
        ul.css({margin: "0", padding: "0", position: "relative", "list-style-type": "none", "z-index": "1"});
        div.css({overflow: "hidden", position: "relative", "z-index": "2", left: "0px"});

        var liSize = o.vertical ? height(li) : width(li);   // Full li size(incl margin)-Used for animation
        var ulSize = liSize * itemLength;                   // size of full ul(total length, not just for the visible items)
        var divSize = liSize * v;                           // size of entire div(total length for just the visible items)

        //li.css({width: li.width(), height: li.height()});
        ul.css(sizeCss, ulSize+"px").css(animCss, -(curr*liSize));

        div.css(sizeCss, divSize+"px");                     // Width of the DIV. length of visible images

        if(o.btnPrev)
            $(o.btnPrev).click(function() {
                return go(curr-o.scroll);
            });

        if(o.btnNext)
            $(o.btnNext).click(function() {
                return go(curr+o.scroll);
            });

        if(o.btnGo)
            $.each(o.btnGo, function(i, val) {
                $(val).click(function() {
                    return go(o.circular ? o.visible+i : i);
                });
            });

        if(o.mouseWheel && div.mousewheel)
            div.mousewheel(function(e, d) {
				if (!$(".images").find("li.ui-sortable-helper").length){
					return d>0 ? go(curr-o.scroll) : go(curr+o.scroll);
				}
            });

        if(o.auto)
            setInterval(function() {
                go(curr+o.scroll);
            }, o.auto+o.speed);

        function vis() {
            return li.slice(curr).slice(0,v);
        };
		
		$("input#search").live("click", function(){
			var el = $(this);
			if ($("div.container_slider").attr("load") != "active"){
				var word = $("input#word_search").val();
				if (word != "" && word != "Поиск:"){
					$("div.container_slider div.preload-img").remove();
					$("div.container_slider").attr("load", "active");
					$(el).addClass("active");
					$("div.container_slider").append('<div class="loading"><div></div></div>');
					var intervalLoading="";
					var params = new Object();
					params.search_word = word;
					params.search_page = "1";
					$.post(o.yaimagesUpload, params, function(data){
						if (data != "" && $("div.container_slider").attr("load") != "error"){
							clearInterval(intervalLoading);
							$(el).removeClass("active");					
							$("div.container_slider div.images ul").empty().append(data);
							$("div.container_slider div.images").attr("data-page", "1");
							$("div.container_slider div.images li.item img.load").parent().css("opacity", "0").css("display", "block");
							var nmb = $("div.container_slider div.images img.load").length;
							var cnt = 0; 
							var intervalTime="";
							$("div.container_slider div.images img.load").each(function(key, item){
								var src = $(item).attr("src");
								$(item).attr("src", src+"?"+Math.random());
								$(item).load(function(){
									$(item).parent().fadeTo(400, 1);
									$(item).removeClass("load");
									cnt++;
									if (cnt == nmb){
										clearInterval(intervalTime);
										li = $("li", ul), itemLength = li.size(), curr = o.start;
										liSize = o.vertical ? height(li) : width(li);
										ulSize = liSize * itemLength;
										ul.css(sizeCss, ulSize+"px").css(animCss, "0px");
										$("input#word_search").attr("data-search", word);
										$("div.container_slider div.loading").remove();
										$("div.container_slider").attr("load", "");
									}
								});
							});
							intervalTime = setTimeout(function(){
								li = $("li", ul), itemLength = li.size(), curr = o.start;
								liSize = o.vertical ? height(li) : width(li);
								ulSize = liSize * itemLength;
								ul.css(sizeCss, ulSize+"px").css(animCss, "0px");
								$("input#word_search").attr("data-search", word);
								$("div.container_slider div.loading").remove();
								$("div.container_slider").attr("load", "");
							}, 2000);
						}
						else if ($("div.container_slider").attr("load") != "error") {
							$(el).removeClass("active");
							$("div.container_slider div.images ul").empty().append('<li class="no-result">Ничего не найдено, попробуйте поменять поисковый запрос</li>');
							$("div.container_slider div.images ul li.no-result").fadeTo(400, 1);
							ul.css(sizeCss, $("div.container_slider div.images").width()+"px").css(animCss, "0px");
							$(o.btnPrev + "," + o.btnNext).addClass("disabled");
							$("input#word_search").attr("data-search", word);
							$("div.container_slider div.loading").remove();
							$("div.container_slider").attr("load", "");
						}
					});
					intervalLoading = setTimeout(function(){
						if (!$("div.container_slider div.images ul li.no-result").length){
							$(el).removeClass("active");
							$("div.container_slider").attr("load", "error");
							$("div.container_slider div.loading").fadeOut(400, function(){
								$(this).remove();
							});
							$("div.container_slider ul").empty().append('<li class="buffer" style="display:none;">Сервис временно не доступен, попробуйте позже</li>');
							ul.css(sizeCss, $("div.container_slider div.images").width()+"px").css(animCss, "0px");
							$(o.btnPrev + "," + o.btnNext).addClass("disabled");
							$("div.container_slider ul li.buffer").fadeIn(400);
						}
					}, 10000);						
				}
				else {
					alert("Введите слово для поиска");
					return false;
				}
			}
			return false;
		});	

		$('div.container_slider div.images ul').unbind();
		$('div.container_slider div.images ul').bind({
			dragenter: function() {
				return false;
			},
			dragover: function() {
				return false;
			},
			dragleave: function() {
				return false;
			},
			drop: function(e) {
				var dt = e.originalEvent.dataTransfer;
				addFiles(dt.files);
				return false;
			}
		});
		
		$('div.yaimages input.add_images').unbind();
		$('div.yaimages input.add_images').bind({
			change: function() {
				addFiles(this.files);
			}
		});
		
		function addFiles(files) {
			var imageType = /image.*/;
			var num = 0;
			var imgCount="";
			var imgSize="";
			
			if ($("div.container_slider div.images ul li.no-result").length){
				$("div.container_slider div.images ul li.no-result").removeClass("no-result").addClass("buffer");
			}
			$("div.container_slider div.images ul li.buffer").hide(0);
			var posLeft = parseInt($("div.container_slider div.images ul").position().left);
			posLeft = -(posLeft/215);
			$.each(files, function(i, file) {
				if (!file.type.match(imageType)) {
					//alert('Добавляемый файл "'+file.name+'" не является картинкой');
					return true;
				}
				num++;
				var li = $('<li class="load"/>');
				var div = $('<div class="load"/>').appendTo(li);				 
				var img = $('<img/>').appendTo(li);
				$('<span/>').appendTo(div);
				if (posLeft > 0){$('div.container_slider div.images ul li:nth-child('+posLeft+')').after(li);}
				else {$('div.container_slider div.images ul').prepend(li);}
				li.get(0).file = file;
				
				var reader = new FileReader();
				reader.onload = (function(aImg) {
					return function(e) {
						aImg.attr('src', e.target.result);
						//imgCount++;
						//imgSize += file.size;
					};
				})(img);
				
				reader.readAsDataURL(file);
			});
			li = $("li", ul), itemLength = li.size();
			liSize = o.vertical ? height(li) : width(li);
			ulSize = liSize * itemLength;
			ul.css(sizeCss, ulSize+"px");
			
			setTimeout(function(){
				$("div.container_slider div.images ul").find('li.load').each(function(){
					var uploadItem = this;
					var params = new Object();
					params.add_images_strip = $(uploadItem).children("img").attr("src");
					$.post(o.yaimagesUpload, params, function(data){	
						if (data != "error"){
							$(uploadItem).children("div.load").remove();
							$(uploadItem).removeClass("load").addClass("item").fadeIn(0);
							$(uploadItem).children("img").attr("alt", data);
						}
						else {
							$(uploadItem).remove();
							li = $("li", ul), itemLength = li.size();
							liSize = o.vertical ? height(li) : width(li);
							ulSize = liSize * itemLength;
							ul.css(sizeCss, ulSize+"px");
						}
					});
				});
			}, 200);
		}		
		
		$("div.container_slider li.item").live('mouseenter', function(){
			var el = $(this);
			if ($(el).children("img").attr("alt") != ""){
				$(el).append('<a href="'+$(this).children("img").attr("alt")+'" class="highslide zoom" onclick="return hs.expand(this)">Увеличить</a>');
			}
			else if ($(el).children("img").attr("data-reserve") != ""){
				$(el).append('<a href="'+$(this).children("img").attr("data-reserve")+'" class="highslide zoom" onclick="return hs.expand(this)">Увеличить</a>');
			}
		});
		
		$("div.container_slider li.item").live('mouseleave', function(){
			$(this).children("a.zoom").remove();
		});	

        function go(to) {
            if(!running && !ul.children("li.no-result").length) {

                if(o.beforeStart)
                    o.beforeStart.call(this, vis());

                if(o.circular) {            // If circular we are in first or last, then goto the other end
                    if(to<=o.start-v-1) {           // If first, then goto last
                        ul.css(animCss, -((itemLength-(v*2))*liSize)+"px");
                        // If "scroll" > 1, then the "to" might not be equal to the condition; it can be lesser depending on the number of elements.
                        curr = to==o.start-v-1 ? itemLength-(v*2)-1 : itemLength-(v*2)-o.scroll;
                    } else if(to>=itemLength-v+1) { // If last, then goto first
                        ul.css(animCss, -( (v) * liSize ) + "px" );
                        // If "scroll" > 1, then the "to" might not be equal to the condition; it can be greater depending on the number of elements.
                        curr = to==itemLength-v+1 ? v+1 : v+o.scroll;
                    } else curr = to;
                } else {                    // If non-circular and to points to first or last, we just return.
                    if(to<0 || to>itemLength-v) return;
                    else curr = to;
                }                           // If neither overrides it, the curr will still be "to" and we can proceed.

                running = true;
			
				var speed = o.speed;
			

				var leftScroll = -(curr*liSize);
                ul.animate(
                    animCss == "left" ? { left: leftScroll } : { top: -(curr*liSize) } , o.speed, o.easing,
                    function() {
                        if(o.afterEnd)
                            o.afterEnd.call(this, vis());
                        running = false;
                    }
                );
				if ($("div.container_slider div.images ul li.item.search").length){
					var def = parseInt($("div.container_slider div.images ul").width())+leftScroll;
					if (def < 2000 && $("div.container_slider").attr("load") != "active" && $("div.container_slider").attr("load") != "end"){
						$("div.container_slider").prepend('<div class="preload-img">Подгрузка изображений</div>');
						$("div.container_slider div.preload-img").fadeIn(600);
						$("div.container_slider").attr("load", "active");
						var page = parseInt($("div.container_slider div.images").attr("data-page"))+1;
						var word = $("input#word_search").attr("data-search");
						var params = new Object();
						params.search_word = word;
						params.search_page = page;
						$.post(o.yaimagesUpload, params, function(data){
							if (data != ""){				
								$("div.container_slider div.images ul").append(data);
								$("div.container_slider div.images").attr("data-page", page);
								$("div.container_slider div.images li.item img.load").parent().css("opacity", "0").css("display", "block");
								var nmb = $("div.container_slider div.images img.load").length;
								var cnt = 0; 
								var intervalTime="";
								$("div.container_slider div.images img.load").each(function(key, item){
									var src = $(item).attr("src");
									$(item).attr("src", src+"?"+Math.random());
									$(item).load(function(){
										$(item).parent().fadeTo(400, 1);
										$(item).removeClass("load");
										cnt++;
										if (cnt == nmb){
											clearInterval(intervalTime);
											li = $("li", ul), itemLength = li.size();
											liSize = o.vertical ? height(li) : width(li);
											ulSize = liSize * itemLength;
											ul.css(sizeCss, ulSize+"px");									
											$("div.container_slider").attr("load", "");
											$("div.container_slider div.preload-img").fadeOut(400, function(){
												$(this).remove();
											});
										}
									});
								});
								intervalTime = setTimeout(function(){
									li = $("li", ul), itemLength = li.size();
									liSize = o.vertical ? height(li) : width(li);
									ulSize = liSize * itemLength;
									ul.css(sizeCss, ulSize+"px");									
									$("div.container_slider").attr("load", "");
									$("div.container_slider div.preload-img").fadeOut(400, function(){
										$(this).remove();
									});
								}, 2000);
							}
							else {
								$("div.container_slider").attr("load", "end");
							}
						});					
					}
				}
				
                // Disable buttons when the carousel reaches the last/first, and enable when not
                if(!o.circular) {
                    $(o.btnPrev + "," + o.btnNext).removeClass("disabled");
                    $( (curr-o.scroll<0 && o.btnPrev)
                        ||
                       (curr+o.scroll > itemLength-v && o.btnNext)
                        ||
                       []
                     ).addClass("disabled");
                }

            }
            return false;
        };
    });
};

function css(el, prop) {
    return parseInt($.css(el[0], prop)) || 0;
};
function width(el) {
    return  el[0].offsetWidth + css(el, 'marginLeft') + css(el, 'marginRight');
};
function height(el) {
    return el[0].offsetHeight + css(el, 'marginTop') + css(el, 'marginBottom');
};

})(jQuery);
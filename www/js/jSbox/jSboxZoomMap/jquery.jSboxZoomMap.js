/*
  * @copyright Art. Lebedev Studio (http://artlebedev.ru)
  * @author Kotelnikov Dmitriy (dimonnot@design.ru)
  */

(function(){
	/*
	  * Класс лупы
	  * @param loup {jQueryElement} Элемент лупы
	  */
	$(".WorkBlock .Right").css("overflow", "visible");
	function Loup( loup, image, fullImagePath ){

		var imgZoom = $('<img/>');
		$(imgZoom).attr("src", fullImagePath+"?"+Math.random()).css("opacity", "0");
		$("body").append(imgZoom);
		
		var ZOOM_WIDTH, ZOOM_HEIGHT, ZOOM;	
		
		var MIN_LEFT = -72,
			MIN_TOP = -72,
			MAX_LEFT = image[0].offsetWidth - loup[0].offsetWidth - 125,
			MAX_TOP = image[0].offsetHeight - loup[0].offsetHeight - 115,
			LOUP_SIZE = 165,
			loupX = 130,
			loupY = 110,			
			loupImage = new Image();
		var fullImage = new Image();

		/*
		 * Инициализация полотная для рисования
		 */

		function initCanvas( isSecond ){
			if( $.browser.msie ){
				var canvasContainer = document.createElement('v:oval');
				canvasContainer.strokeweight = '0px';
				canvasContainer.style.width = LOUP_SIZE;
				canvasContainer.style.height = LOUP_SIZE;
				canvas = document.createElement('v:fill');
				canvas.type = 'tile';
				canvas.src = loupImage.src;
				canvas.size = (ZOOM_WIDTH / LOUP_SIZE) + "," + (ZOOM_HEIGHT/ LOUP_SIZE);
				loup.append(canvasContainer);
				canvasContainer.appendChild(canvas);
			}
			else{
				var canvasContainer = document.createElement('div');
				canvasContainer.className = 'canvas';
				canvas = document.createElement('canvas');
				canvas.width = LOUP_SIZE;
				canvas.height = LOUP_SIZE;
				canvasContainer.appendChild(canvas);
				loup.append(canvasContainer);
				canvas = canvas.getContext('2d');
			}
		}

		/*
		 * Навешиваем обработчики событий
		 */

		function initEvents(){
			loup.mousedown(
				function( event ){
					isMoving = 1;
					mouseX = event.pageX;
					mouseY = event.pageY;
					return false;
				}
			);

			$(document).mousemove(
				function( event ){
					if( !isMoving )
						return true;

					loupX += event.pageX - mouseX;
					loupY += event.pageY - mouseY;
					drawLoup();
					mouseX = event.pageX;
					mouseY = event.pageY;
					return false;
				}
			).mouseup(
				function(){
					isMoving = 0;
				}
			);
		}

		/*
		 * Функция перерисовки лупы
		 */
		function drawLoup(){
			if( loupX < MIN_LEFT )
				loupX = MIN_LEFT;

			if( loupX > MAX_LEFT )
				loupX = MAX_LEFT;

			if( loupY < MIN_TOP )
				loupY = MIN_TOP;

			if( loupY > MAX_TOP )
				loupY = MAX_TOP;

			if( $.browser.msie ){
				canvas.position = ((-loupX * ZOOM - 135) / LOUP_SIZE) + "," + ((-loupY * ZOOM - 135)/ LOUP_SIZE);
			}
			else{
				canvas.beginPath();
				canvas.arc(LOUP_SIZE/2, LOUP_SIZE/2, LOUP_SIZE/2, 0, Math.PI*2, true);
				canvas.clip();

				try{
					if (fullImage && fullImage.width) {
						canvas.fillStyle = "#ffffff";
						canvas.fillRect(0, 0, ZOOM_WIDTH, ZOOM_HEIGHT);
					}
					canvas.drawImage(loupImage, Math.round(-loupX * ZOOM) - 135, Math.round(-loupY * ZOOM) - 135, ZOOM_WIDTH, ZOOM_HEIGHT);
				}catch(e){}
			}

			loup.css({
				left:loupX + 'px',
				top:loupY + 'px'
			});
		}

		var canvas, isMoving = 0, mouseX, mouseY;

		$(loupImage).load(
			function(){
				$(imgZoom).load(function(){
					$("#map-zoom").css({"width": image[0].clientWidth+"px", "height": image[0].clientHeight+"px"});
					ZOOM_WIDTH = $(imgZoom).width();
					ZOOM_HEIGHT = $(imgZoom).height();
					ZOOM = ZOOM_WIDTH / image[0].clientWidth;
					initCanvas();
					initEvents();
					drawLoup();
					loup.show();
					$(fullImage).load(
						function(){
							loupImage = fullImage;
							if( $.browser.msie ){
								canvas.src = fullImage.src;
							}
							drawLoup();
						}
					);
					fullImage.src = fullImagePath;

					$(imgZoom).remove();
				});
			}
		);
		loupImage.src = image.attr('src');
	}

	$(function(){			
			$("body").prepend('<link rel="stylesheet" type="text/css" href="/js/jSbox/jSboxZoomMap/style.css"><script type="text/javascript" src="/js/jSbox/jSboxZoomMap/jquery-ui-draggable.min.js"></script>');
			$("a.jSboxZoomMap img").each(function(){
				var el = $(this).parent();
				var img = $(this).parent().html();
				var link = $(this).parent().attr("href");
				if (link != ""){
					$(el).replaceWith('<div id="map-zoom"><div class="map-shadow"></div><a class="jSboxZoomMap" href="'+link+'">'+img+'</a><div style="display:none" id="map-loup"><map id="loup_pen" name="pen"><area shape="poly" coords="168,166, 164,163, 275,291, 260,307, 151,185, 168,166" /></map><img src="/js/jSbox/jSboxZoomMap/lupa.png" alt="" usemap="#pen" /></div><a id="expand" href="#"></a></div>');
				}
			});
			$('#map-zoom a#expand').live("click", function(){
				var link = $("a.jSboxZoomMap").attr("href");
				$("body").prepend('<div id="jSboxZoomMap-overlay"></div><div id="jSboxZoomMap-container"><img src="'+link+'" alt=""><span id="close"></span></div>');
				$("#jSboxZoomMap-overlay").fadeIn();
				$("#jSboxZoomMap-container img").attr("src", $("#jSboxZoomMap-container img").attr("src")+"?"+Math.random());		
				$("#jSboxZoomMap-container img").load(function(){
					var img = $(this);
					var windowW = $("#jSboxZoomMap-container").width();
					var windowH = $("#jSboxZoomMap-container").height();
					var imgW = $(this).width();
					var imgH = $(this).height();
					if (imgH > windowH || imgH < windowH){
						$(img).css("top", ((windowH-imgH)/2)+"px");		
					}
					if (imgW > windowW || imgW < windowW){
						$(img).css("left", ((windowW-imgW)/2)+"px");		
					}					
					$("#jSboxZoomMap-container").animate({opacity:1}, 250);
					$(img).draggable();
				});	
					
				return false;
			});
			$("#jSboxZoomMap-container").live("click", function(){
				$(this).remove();
				$("#jSboxZoomMap-overlay").remove();
			});
			$('#map-zoom a.jSboxZoomMap').click(
				function(){
					return false;
				}
			).each(
				function(){
					var that = this;
					Loup($('#map-loup'), $(that).find('img'), that.href);
				}
			);

			if( /msie (6|5)/.test(navigator.userAgent.toLowerCase()) ){
				$('#map-loup img').each(
					function(){
						this.style.width = this.clientWidth +'px';
						this.style.height = this.clientHeight +'px';
						var src = this.src;
						this.src = '/js/jSbox/jSboxZoomMap/blank.gif';
						this.runtimeStyle.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + src + "',sizingMethod='crop')";
					}
				);
			}
			
		}
	);
	
	if($.browser.msie && !document.namespaces["v"]){
		document.namespaces.add("v", "urn:schemas-microsoft-com:vml");
		var ss = document.createStyleSheet();
		if( /msie 8/.test( navigator.userAgent.toLowerCase() ) )
			ss.cssText = "v\\:image,v\\:line, v\\:fill, v\\:oval{behavior:url(#default#VML);display:inline-block}";
		else
			ss.cssText = "v\\:* {behavior:url(#default#VML);display:inline-block}";
	}
})();
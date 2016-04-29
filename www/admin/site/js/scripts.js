$(document).ready(function(){

	var _ua = navigator.userAgent.toLowerCase(),
    browser = {
      msie: (/msie/i.test(_ua) && !/opera/i.test(_ua) || /trident\//i.test(_ua)),
      msie6: (/msie 6/i.test(_ua) && !/opera/i.test(_ua)),
      msie7: (/msie 7/i.test(_ua) && !/opera/i.test(_ua)),
      msie8: (/msie 8/i.test(_ua) && !/opera/i.test(_ua)),
      msie9: (/msie 9/i.test(_ua) && !/opera/i.test(_ua))
    };
	
	var isTouchDevice = false;
    if ('ontouchstart' in document.documentElement){
        isTouchDevice = true;
    }
	
	var pixelRatio = 1;
	
	if ('devicePixelRatio' in window && window.devicePixelRatio > 1){
		pixelRatio = window.devicePixelRatio;
	}

	setTimeout(function(){
		if (!$.cookie("set_referrer")){
			$.cookie('set_referrer', document.referrer, {expires: (1/12), path: '/'});
			$.cookie('set_start_url', window.location.href, {expires: (1/12), path: '/'});
		}
		var params = new Object();
		params.visit = window.location.href;
		//$.get('/cgi-bin/send_visitors.cgi', params);
		
	}, 300);
	
	if ($.cookie("private_login")){
		$("#private-enter").replaceWith('<ul id="private-enter">'
				+'<li class="enter"><a href="/private/"><span>Личный кабинет</span></a></li>'
				+'<li class="exit">'
					+'<form method="post" action="/private/">'
						+'<input type="hidden" value="private" name="alias">'
						+'<input type="hidden" name="action" value="exit">'
						+'<input class="exit" type="submit" value="Выйти из кабинета">'
					+'</form>'
				+'</li>'
			+'</ul>');
	}
	
	// Определение города
	
	var $header = $(".header-top");

	if (!$.cookie("come_city")){
		var params = new Object();
		params.get_city = true;
		$.get('/get_city.php', params, function(city){
			if (city && city.length > 2){
				$header.find(".city").find("a").html(city);
				popupCity(city);
			}
			else {
				city = "Ростов-на-Дону";
				$header.find(".city").find("a").html(city);	
				popupCity(city);
			}
		});
		
		var hidePopupCity = false;
		window.onscroll = function(){
			var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
			if (!hidePopupCity && scrollTop > 200){
				hidePopupCity = true;
				$header.find(".popup-city").removeClass("open");
			}
		}
	}
	else {
		$header.find(".city").find("a").html(URLDecode($.cookie("come_city")));
	}
	
	function popupCity(city){
		var popup='<div class="b-popup popup-city">'
			+'<p>Ваш город &mdash; '+city+'<br>Угадали?</p>'
			+'<div class="wrap-b">'
				+'<button class="yes">Да</button>&nbsp;'
				+'<button class="no">Нет</button>'
			+'</div>'
		+'</div>';		
		$header.append(popup);
		var $popup = $header.find(".popup-city");
		setTimeout(function(){
			$popup.addClass("open");
		}, 5);
		$popup.find(".yes").on("click", function(){
			$header.find(".popup-city").removeClass("open");
			$.cookie('come_city', URLEncode(city), {expires: 365, path: '/'});
		});
		$popup.find(".no").on("click", function(){
			selectCity(city);
		});		
	}
	
	$header.find(".city").find("a").on("click", function(){
		selectCity($(this).text());
		return false;
	});
	
	function selectCity(city){
		$header.find(".popup-city").removeClass("open");
		var $selectCity = $("#selectCity");
		$selectCity.removeClass("close").addClass("open");
		setTimeout(function(){
			$selectCity.css({"height": "100%"});
			$selectCity.find("#el_content").css({"top": "8%"});
		}, 0);
		var $container = $selectCity.find("#el_container_city");		
		if ($container.html() == ""){
			var params = new Object();
			params.getCityList = true;
			$.post('/ajax/', params, function(data){
				if (data){
					$container.html(data);
					setTimeout(function(){
						$container.find("a").each(function(){
							if (city == $(this).text()){
								$(this).addClass("active");
							}
						});
						$container.addClass("open");
					}, 5);
					var $cityName = $header.find(".city").find("a");
					$container.find("a").on("click", function(){
						var city = $(this).text();
						$container.find("a").removeClass("active");
						$(this).addClass("active");
						$.cookie('come_city', URLEncode(city), {expires: 365, path: '/'});
						eLightboxClose();
						$cityName.text(city);
						return false;
					});
					$selectCity.find("#cityOther").on("click", function(){
						if (!$container.find(".cityOther").length){
							$container.find("ul").css("opacity", "0.4");
							$container.append('<div class="el_input_big cityOther"><input type="text" placeholder="Введите свой город и нажмите выбрать" autocomplete="off"><button>Выбрать</button></div>');
							var $cityOther = $container.find(".cityOther");
							setTimeout(function(){
								$cityOther.addClass("open");
							}, 20);
							$cityOther.find("button").on("click", function(){
								var city = $cityOther.find("input").val();
								if (city.length > 2){
									$.cookie('come_city', URLEncode(city), {expires: 365, path: '/'});
									$container.find("ul").css("opacity", "");
									$container.find(".cityOther").removeClass("open");
									setTimeout(function(){
										$container.find("a").removeClass("active");
										$container.find("a").each(function(){
											if (city == $(this).text()){
												$(this).addClass("active");
											}
										});
										$container.find(".cityOther").remove();
										eLightboxClose();
										$cityName.text(city);
									}, 300);									
								}
							});
						}
						else {
							$container.find("ul").css("opacity", "");
							$container.find(".cityOther").removeClass("open");
							setTimeout(function(){
								$container.find(".cityOther").remove();
							}, 300);
						}
					});
				}
			});
		}
	}
	
	$("#cityContacts, #city-list span").on("click", function(e){
		e.preventDefault();
		var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
		$("body").css({
			'overflow': 'hidden',
			'width': $("body").width()+"px",
			'height': $("body").height()+"px"
		});
		$("body").append('<div class="eLightbox w-popup-wrapper"><div class="el_close"></div><div class="w-popup">'+cityContacts+'</div></div>');
		var $modal = $(".w-popup-wrapper");
		var $close = $modal.find(".el_close");
		setTimeout(function(){
			$modal.addClass("show");
		}, 20);
		$close.on("click", function(){
			$modal.removeClass("show");
			setTimeout(function(){
				$("body").attr("style", "");
				$modal.remove();
			}, 150);
		});
	});
	
	var cityContacts = '<div class="contacts-block">'
			+'<div class="contacts-block-item center">'
				+'<h4>Центральный офис нашей компании</h4>'
				+'<h5>г. Ростов-на-Дону, ул. Орская 31в, офис 1.</h5>'
				+'<p>Компания <strong>ООО «Технологии света»</strong></p>'
				+'<p>Телефон: <strong class="green">8 (800) 700-47-34</strong> &ndash; прием заказов по России.</p>'
			+'</div>'
			+'<div class="contacts-block-container">'
				+'<div class="contacts-block-item">'
					+'<h5>г. Краснодар</h5>'
					+'<p>Компания <strong>«LEDFASHION»</strong></p>'
					+'<p>Адрес: <a target="_blank" href="http://maps.yandex.ru/?text=г. Краснодар, ул. Вишняковой, 2">ул. Вишняковой, 2</a></p>'
					+'<p>Телефон: (918) 000-04-70</p>'
				+'</div>'
				+'<div class="contacts-block-item">'
					+'<h5>г. Ставрополь</h5>'
					+'<p>Компания <strong>«LedVision»</strong></p>'
					+'<p>Адрес: <a target="_blank" href="http://maps.yandex.ru/?text=г. Ставрополь, 2-й Юго-Западный проезд, 3">2-й Юго-Западный проезд, 3</a></p>'
					+'<p>Телефон: (8652) 68-09-09</p>'
				+'</div>'
				+'<div class="contacts-block-item">'
					+'<h5>г. Махачкала</h5>'
					+'<p>Компания <strong>«Кавказ LED»</strong></p>'
					+'<p>Адрес: <a target="_blank" href="http://maps.yandex.ru/?text=г. Махачкала, ул. М. Гаджиева, 64а">ул. М. Гаджиева, 64а</a></p>'
					+'<p>Телефон: (964) 024-60-60</p>'
				+'</div>'
				+'<div class="contacts-block-item">'
					+'<h5>г. Омск</h5>'
					+'<p>Компания <strong>«Ледокол»</strong></p>'
					+'<p>Адрес: <a target="_blank" href="http://maps.yandex.ru/?text=г. Омск, ул. Гусарова, 55a, офис 15">ул. Гусарова, 55a, офис 15</a></p>'
					+'<p>Телефон: (3812) 39-98-78</p>'
				+'</div>'
				+'<div class="contacts-block-item">'
					+'<h5>г. Орск</h5>'
					+'<p>Компания <strong>«Гранд Электро»</strong></p>'
					+'<p>Адрес: <a target="_blank" href="http://maps.yandex.ru/?text=г. Орск, пр. Мира 24">пр. Мира 24 (цокольный этаж)</a></p>'
					+'<p>Телефон: (3537) 33-29-29</p>'
				+'</div>'
				+'<div class="contacts-block-item">'
					+'<h5>г. Саратов</h5>'
					+'<p>Компания <strong>«Бери Свет»</strong></p>'
					+'<p>Адрес: <a target="_blank" href="http://maps.yandex.ru/?text=г. Саратов, ул. Б. Горная, 353">ул. Б. Горная, 353</a></p>'
					+'<p>Телефон: (906) 303-92-34</p>'
				+'</div>'
				+'<div class="contacts-block-item">'
					+'<h5>г. Самара</h5>'
					+'<p>Компания <strong>«LED завод»</strong></p>'
					+'<p>Адрес: <a target="_blank" href="http://maps.yandex.ru/?text=г. Самара, ул. Ново-Садовая 106, к.170, оф.107">ул. Ново-Садовая 106, к.170, оф.107</a></p>'
					+'<p>Телефон: (800) 775-31-63</p>'
				+'</div>'
				+'<div class="contacts-block-item">'
					+'<h5>г. Волгоград</h5>'
					+'<p>Компания <strong>«LED Volgograd»</strong></p>'
					+'<p>Адрес: <a target="_blank" href="http://maps.yandex.ru/?text=г. Волгоград, пр. Канатчиков 2">пр. Канатчиков 2</a></p>'
					+'<p>Телефон: (927) 510-43-13</p>'
				+'</div>'
				+'<div class="contacts-block-item">'
					+'<h5>г. Тюмень</h5>'
					+'<p>Компания <strong>«LED group»</strong></p>'
					+'<p>Адрес: <a target="_blank" href="http://maps.yandex.ru/?text=г. Тюмень, ул. Герцена 55, оф. 238">ул. Герцена 55, оф. 238</a></p>'
					+'<p>Телефон: (919) 958-81-72</p>'
				+'</div>'
			+'</div>'
			+'<div class="clearfix"></div>'
			+'<div class="contacts-block-item center bottom">'
				+'<h4>Доставка осуществляется во все регионы России</h4>'
			+'</div>'			
		+'</div>';
	
	var $sidebar_banner2 = $(".sidebar-banner2");
	
	if ($sidebar_banner2.length){
		var set_banner2 = $.cookie('set_banner2');
		if (set_banner2 && set_banner2 > 0){		
			if (set_banner2 == "4"){set_banner2 = 1;}
			else {set_banner2++;}
		}
		else {
			set_banner2 = 1;
		}
		var slide = '<a href="/pages/delivery"></a><div class="slide1"></div>';
		if (set_banner2 == "2"){slide = '<a href="/pages/sales"></a><div class="slide'+set_banner2+'"></div>';}
		else if (set_banner2 == "3"){slide = '<a href="/pages/delivery"></a><div class="slide'+set_banner2+'"></div>';}
		else if (set_banner2 == "4"){slide = '<a href="/catalog/svetodiodnye-prozhektory/osvetitelnye"></a><div class="slide'+set_banner2+'"></div>';}
		$sidebar_banner2.append(slide);
		$.cookie('set_banner2', set_banner2, {expires: 1, path: '/'});
		setTimeout(function(){
			$sidebar_banner2.addClass("show");
		}, 500);
	}
	
	var $wrap_banner = $(".sidebar-banner");
	
	if ($wrap_banner.length && !browser.msie9){
	
		var $start_banner, set_banner = $.cookie('set_banner');
		
		if (pixelRatio == 2 || pixelRatio > 2){
			var img_to_replace = $wrap_banner.find("img.img").get();

			for (var i=0,l=img_to_replace.length; i<l; i++) {
				var src = img_to_replace[i].src;
				src = src.replace(/\.(png|jpg|gif)+$/i, '@2x.$1');
				img_to_replace[i].src = src;
			};
		}		

		if (set_banner && set_banner > 0){		
			if (set_banner == "3"){set_banner = 0;}
			else {set_banner++;}
			$start_banner = $wrap_banner.find(".banner-slide"+set_banner);		
		}
		else {
			$start_banner = $wrap_banner.find(".banner-slide0");		
		}
		
		setTimeout(function(){
			slideBanner($start_banner);
		}, 1000);
	}
	else {
		$wrap_banner.remove();
	}
	
	function slideBanner(banner){
		var $banner = $(banner);
		var num = $banner.data("slide");
		$.cookie('set_banner', num, {expires: 1, path: '/'});
		var banner_class = $banner.attr("class");
		$banner.addClass("active").addClass("fadeInRight");
		setTimeout(function(){
			var $img = $banner.find(".img");
			var img_class = $img.attr("class");
			$img.addClass("rotateInDownRight");
			var $price = $banner.find(".price");
			setTimeout(function(){
				$price.addClass("bounceIn");
				setTimeout(function(){
					$price.addClass("pulse");
					setTimeout(function(){
						$price.removeClass("bounceIn").removeClass("pulse");
						$img.addClass("rotateOutUpLeft");
						setTimeout(function(){
							$banner.addClass("fadeOutRight");
							if (num == "3"){num = 0;}
							else {num++;}
							var $banner_new = $(".sidebar-banner").find(".banner-slide"+num);
							setTimeout(function(){
								$banner.attr("class", banner_class);
								$img.attr("class", img_class);
								slideBanner($banner_new);
							}, 850);
						}, 500);
					}, 7000);
				}, 500);
			}, 800);
		}, 700);
	}	

	var $catalog_mask = $("#catalog-mask"),
		$catalog_nav = $(".catalog-nav");

	if (isTouchDevice){
		$catalog_mask.remove();
	}
	else {
		$catalog_mask.on("mouseenter", function(){
			setTimeout(function(){
				$catalog_mask.hide(0);
				setTimeout(function(){
					$("body").on("mouseover", function(e){
						if (e.pageY < 208){
							$catalog_mask.show(0);
							$("body").off("mouseover");
						}
						else if (e.pageY > 253 && !$catalog_nav.find("a.hover").length){
							$catalog_mask.show(0);
							$("body").off("mouseover");						
						}
					});
				}, 20);
			}, 200);
		});
		
		$catalog_nav.on("mouseleave", function(e){
			if (e.pageY < 208 || e.pageY > 253){
				$catalog_mask.show(0);
			}
		});	
	}
	
	var $slideshow = $(".slideshow");

	if ($slideshow.length){
	
		if (pixelRatio == 2 || pixelRatio > 2){
			var img_to_replace = $slideshow.find("img").get();

			for (var i=0,l=img_to_replace.length; i<l; i++) {
				var src = img_to_replace[i].src;
				src = src.replace(/\.(png|jpg|gif)+$/i, '@2x.$1');
				img_to_replace[i].src = src;
			};
		}	
	
		$slideshow.royalSlider({
			autoHeight: false,
			arrowsNav: false,
			fadeinLoadedSlide: false,
			transitionSpeed: 750,
			controlNavigationSpacing: 0,
			controlNavigation: 'bullets',
			imageScaleMode: 'fill',
			imageAlignCenter: true,
			autoPlay: {
				enabled: true,
				stopAtAction: true,
				pauseOnHover: false,
				delay: 4500
			},
			loop: true,
			loopRewind: false,
			numImagesToPreload: 3,
			keyboardNavEnabled: true,
			autoScaleSlider: false
		});
	}

	var win_width = parseInt($("body").width());
	var wrap_width = parseInt($(".wrapper").width());
	
	$(".catalog-nav").find(".submenu").each(function(){
		var width = parseInt($(this).width())+60;
		var left = parseInt($(this).prev().offset().left);
		var def = (win_width-wrap_width)/2;
		var delta = left-def;
		if ((width + delta) > wrap_width){
			$(this).css("left", -(width+delta-wrap_width)+"px");
		}
	});

	$(".our-products, .catalog-nav").find("li").find("a:first").on("mouseenter", function(){
		var $link = $(this);
		$link.next().on("mouseenter mouseleave", function(e){
			if (e.type == "mouseenter"){
				$link.addClass("hover");
			}
			else if (e.type == "mouseleave"){
				$link.removeClass("hover");
			}			
		});
	});
	
	$(".our-products, .catalog-nav").on("mouseenter mouseleave", function(e){
		if (e.type == "mouseenter"){
			$(this).find("a.active").removeClass("active");
		}
		else if (e.type == "mouseleave"){
			$(this).find("a[data-active='true']").addClass("active");
		}
	});
	
	$(".callback, .callback02, #callback").jSbox({
		width : 423,
		speed : 300,
		theme : "red",
		autoclear : true,
		border : true,
		maskphone : "input.text[name=PHONE]",
		box : ".callback-container"
	});
	
	$(".body-callback").find(".callback").live("click", function(){
		goals({type: "CALL_BACK"});
	});	
	
	$(".buy_quick").jSbox({
		width : 423,
		speed : 300,
		theme : "red",
		border : true,
		ajax: "/cgi-bin/product_ajax.cgi?buy_quick="+$('.buy_quick').attr('p_id'),
		box : ".buy-quick-container"
	});

	$(".buy-quick-send").live("click", function(){
		goals({type: "BUY_QUICK"});
	});	
	
	$(".filter-views").find("a").on("click", function(){
		if (!$(this).parent().attr("class").match(/active/)){
			var view = $(this).parent().attr("class");
			$(this).parent().parent().find("li").removeClass("active");
			$(this).parent().addClass("active");
			$.cookie('view_products', view, {expires: 1, path: '/'});
			if (wrap_width > 1000){
				$("ul.products-list").animate({opacity: "0.3"}, 100, "easeInOutSine", function(){
					$("ul.products-list").removeClass("list").removeClass("table");
					$("ul.products-list").addClass(view);
					$("ul.products-list").animate({opacity: "1"}, 100, "easeInSine");
				});		
			}
			else {
				$("ul.products-list").removeClass("list").removeClass("table");
				$("ul.products-list").addClass(view);
			}
		}
		return false;
	});
	
	$(".filter-price").find("em").on("click", function(){
		var $el = $(this);
		var data = $el.data("filter");
		if ($el.attr("class") == "active"){
			$.cookie('filter_price', null, {expires: 0, path: '/'});
		}
		else {
			$.cookie('filter_price', data, {expires: 1, path: '/'});
		}
		location.replace(window.location.href);
	});
	
	$("form.filter-box").find("label.color").on("click", function(){
		if ($(this).attr("class").match(/active/)){
			$(this).removeClass("active");
			$("form.filter-box").find('input[name=color]').val("");
		}
		else {
			$(this).parent().find("label").removeClass("active");
			$(this).addClass("active");
			var value = $(this).attr("data-name");
			$("form.filter-box").find('input[name=color]').val(value);
		}
	});	
	
	var $authBox = $("#authBox"),
		$regForm = $("#regForm"),
		$eLightbox = $(".eLightbox"),
		$el_tags = $authBox.find(".el_tags"),
		$el_tabs = $authBox.find(".el_tabs"),
		$el_name = $authBox.find("h2"),
		$scroller_related = $(".scroller.related"),
		$scroller_product_gallery = $(".scroller.product-gallery");
	
	$("#enter, #auth, #reg").on("click", function(){
		$authBox.removeClass("close").addClass("open");
		var tab = $(this).attr("data-tag");
		var name = $(this).text();
		setTimeout(function(){
			$authBox.css({"height": "100%"});
			$authBox.find("#el_content").css({"top": "50%"});
			$el_tags.find("li").removeClass("current");
			$el_tags.find("li").find("a[data-tag='"+tab+"']").parent().addClass("current");
			$el_tabs.find(".show").removeClass("show");
			$el_tabs.find(".tab-"+tab).addClass("show");			
			if (tab == "login"){name = "Войти в кабинет";}
			else if (tab == "register"){name = "Регистрация";}
			$el_name.html(name);
		}, 0);
		return false;
	});
	
	$eLightbox.find(".el_close").on("click", function(){
		eLightboxClose();
	});
	
	function eLightboxClose(){
		var $box = $(".eLightbox.open");
		$box.removeClass("open").addClass("close");
		setTimeout(function(){
			$box.css({"height": "0"});
			$box.find("#el_content").css({"top": "25%"});
		}, 0);		
	}
	
	$el_tags.find("li").find("a").on("click", function(){
		if (!$(this).parent().attr("class").match(/current/)){
			var tab = $(this).attr("data-tag");
			var name = $(this).text();
			$(this).parent().parent().find("li").removeClass("current");
			$(this).parent().addClass("current");
			$el_tabs.find(".show").removeClass("show");
			$el_tabs.find(".tab-"+tab).addClass("show");
			if (tab == "login"){name = "Войти в кабинет";}
			else if (tab == "pass_recovery"){name = "Восстановление";}
			$el_name.html(name);			
		}		
		return false;		
	});	
	
	$eLightbox.find(".eye").on("click", function(){
		if (!$(this).parent().attr("class").match(/show_symbol/)){
			$(this).parent().addClass("show_symbol");
		}
		else {
			$(this).parent().removeClass("show_symbol");
		}
	});
	
	// Регистрация 
	
	$regForm.find(".btn").on("click", function(e){
		e.preventDefault();
		var name = $regForm.find("input[name=user_name]").val(),
			email = $regForm.find("input[name=user_login]").val(),
			title, text,
			pattern = "^([a-z0-9_-]+)(\\.[a-z0-9_-]+)*@((([a-z0-9-а-яА-ЯёЁ]+\\.)+(рф|РФ|com|net|org|mil|edu|gov|arpa|info|biz|inc|name|[a-z]{2}))|([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}))$";
		if (name.length < 2){
			title = 'Введите свое имя';
			text = 'Не заполнили поле "Ваше имя"';	
		}
		else if (email.length < 6){
			title = 'Введите свой email';
			text = 'Не заполнили поле "Эл. почта"';
		}
		else if (email.length && !isPattern(pattern, email)){
			title = 'Введите корректный email';
			text = 'Вы ввели не корректный email адрес';
		}
		if (name.length < 2 || email.length < 6 || email.length && !isPattern(pattern, email)){
			swal({
			  title: title,
			  text: text,
			  confirmButtonColor: "#e6a120",
			  type: "warning",
			  allowOutsideClick: true
			});
		}
		else {
			$regForm.append('<div class="eLightbox-overlay"></div>');
			$regForm.find(".field_pass").addClass("open");
			$regForm.find(".type_text").css("opacity", "0.4");
			$regForm.find(".btn").css("opacity", "0.4");
			$regForm.find(".eLightbox-overlay").on("click", function(){
				$regForm.find(".field_pass").removeClass("open");
				$regForm.find(".type_text").css("opacity", "1");
				$regForm.find(".btn").css("opacity", "1");
				$(this).remove();
			});
		}
	});	
	
	$regForm.find(".field_pass").find("button").on("click", function(){
		if ($regForm.find(".field_pass").hasClass("open")){
			var pass = $regForm.find(".field_pass").find("input").val();
			var pattern = "^[a-zA-Z0-9-_\.]{6,}$";
			if (!isPattern(pattern, pass)){
				swal({
				  title: 'Пароль должен состоять',
				  text: 'из латинских буквы и цифр, минимум из 6 символов',
				  confirmButtonColor: "#e6a120",
				  type: "warning",
				  allowOutsideClick: true
				});
			}
			else {
				var regForm = document.getElementById("regForm");
				document.regForm.submit();
			}
		}
	});
	
	$regForm.submit(function(e){
		e.preventDefault();
	});
	
	if ($scroller_related.length){
		var slider = {
			init: function(){
				$scroller_related.find(".owl-carousel").owlCarousel({
					itemsCustom: [[700, 3], [1000, 3], [1199,4]],
					rewindNav: false,
					navigation: true,
					pagination: false
				});
			}
		}.init();	
	}	
	
	if ($scroller_product_gallery.length){
		var slider = {
			init: function(){
				$scroller_product_gallery.find(".owl-carousel").owlCarousel({
					itemsCustom: [[700, 5], [1000, 5], [1199,7]],
					rewindNav: false,
					navigation: true,
					pagination: false
				});
			}
		}.init();
		$scroller_product_gallery.find("a").touchTouch();
	}
	
	// Посмотреть тех. характеристики товара
	
	$(".characteristics").find("h2").toggle(function(){
		$(this).next("table").show(400, "easeOutCirc");
	}, function(){
		$(this).next("table").hide(400, "swing");
	});
	
	// Показать еще товары
	
	$(".more_products").click(function(){
		if (!$(this).find(".b-loader").length){
			var $container = $(".products-list");
			var $button = $(this);
			$button.addClass("active").append('<div class="b-loader"></div>');
			setTimeout(function(){
				$button.find(".b-loader").addClass("scale");
			}, 10);
			var height = parseInt($container.height());
			$container.css("height", height+"px");
			var height_box = $button.attr("data-height");
			if (!height_box){
				height_box = height;
				$button.attr("data-height", height_box);
			}
			var ids = $button.attr("data-ids").split(",");
			var params = new Object();
			params.products_ids = String(ids);
			params.products_cat_name = $("h1").text();
			$.post('/cgi-bin/product_ajax.cgi', params, function(data){
				if (data){
					var $products = $(data);
					$products.find("li").css("opacity", "0");
					setTimeout(function(){
						$container.append($products);
						$container.animate({"height": (height+(height_box*2))+"px"}, 1300, "swing", function(){
							$container.css("height", "100%");
						});
						$button.removeClass("active");
						$button.find(".b-loader").remove();
						var limit = parseInt($button.attr("data-limit"));
						var new_ids = [];
						for (var i = 0; i < ids.length; i++) {
							if (i > (limit-1)){new_ids.push(ids[i]);}
						}
						if (new_ids.length > 0){
							$button.find("span").html(new_ids.length);
							$button.attr("data-ids", String(new_ids));
						}
						else {
							$button.remove();
						}
					}, 0);
				}
			});
		}
	});
	
	// Изменение количества товара
	
	$(".product-info").find(".number").find("li").on('click', function(){
		var $container = $(this).parent().parent().parent();
		var count = parseFloat($(this).text());
		var price = parseFloat($container.find(".buy_product").attr("price"));
		price = parseInt(price*count);
		price = String(price).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
		$(this).parent().find(".active").removeClass("active");
		$(this).addClass("active");
		resizeCountInput($container.find(".count"), count);
		$container.find(".count").attr("value", count);	
		$container.find(".price-holder").find(".price").find("span").html(price);
	});

	if ($(".product-info").length){$(".product-info").find(".number").find("input.count").val("1");}
	$(".product-info").find(".number").find(".plus").on('click', function(){
		var $container = $(this).parent();
		var $button = $container.parent().parent().find(".buy_product");
		var count = parseFloat($container.find(".count").val());
		var price = parseFloat($button.attr("price"));
		var pack = parseFloat($button.attr("data-pack"));
		var residue = count % pack;
		if (residue !== 0){
			var def = (count/pack).toFixed(0);
			count = def*pack + pack;
		}
		else {
			count = count + pack;
		}
		price = parseInt(price*count);
		price = String(price).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
		resizeCountInput($container.find(".count"), count);
		$container.find(".count").attr("value", count);
		$container.parent().parent().find(".price-holder").find(".price").find("span").html(price);
		return false;
	});
	
	$(".product-info").find(".number").find(".minus").on('click', function(){
		var $container = $(this).parent();
		var $button = $container.parent().parent().find(".buy_product");
		var count = parseFloat($container.find(".count").val());
		if (count > 1){
			var price = parseFloat($container.parent().parent().find(".buy_product").attr("price"));
			var pack = parseFloat($button.attr("data-pack"));
			count = count - pack;
			if (count === 0 || count < 0){
				return false;
			}			
			price = parseInt(price*count);
			price = String(price).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
			resizeCountInput($container.find(".count"), count);
			$container.find(".count").attr("value", count);
			$container.parent().parent().find(".price-holder").find(".price").find("span").html(price);
		}
		return false;
	});
	
	function resizeCountInput(input, count){
		if (count > 99 && count < 1000){
			$(input).css("width", "45px");
		}
		else if (count > 999 && count < 10000){
			$(input).css("width", "64px");
		}
		else if (count > 9999){
			$(input).css("width", "74px");
		}		
		else {
			$(input).css("width", "40px");
		}	
	}

	// Положить товар в корзину

	$(".buy_product").live('click', function(){
		var $button = $(this);
		var $count = $button.parent().find("input.count");
		var pack = $button.data("pack");
		var unit = $button.data("unit");
		if (pack !== undefined && $count !== undefined && parseInt(pack) > parseInt($count.val())){
			swal({
			  title: "Обратите внимание\n норма отгрузки от "+pack+" "+unit,
			  text: "Согласуйте меньшую отгрузку с нашим менеджером",
			  textPhone: '8 800 700-47-34',
			  cancelButtonText: "Изменить количество",
			  confirmButtonText: "Добавить в корзину",
			  confirmButtonColor: "#DD6B55",
			  cancelButtonColor: "#76b852",
			  type: "warning",
			  showCancelButton: true,
			  cancelButtonSuccess: true,
			  allowOutsideClick: true
			}, function(){
				addBasket($button);
			});
			setTimeout(function(){
				$button.parent().find(".packnorm").addClass("warning");
			}, 300);
		}
		else {
			addBasket($button);
		}
		return false;
	});
	
	function addBasket(button){
		var $button = button;
		var $container=""; var scale=""; var packnorm="";
		if ($button.parent().attr("class").match(/holder/)){
			$container = $button.parent().parent().find("a.image");
			if ($container.parent().attr("class") == "reflect"){scale = "scale(3,3)";}
			else {scale = "scale(3,3) scaleX(-1)";}
			packnorm = $button.attr("data-pack");
		}
		else {
			$container = $button.parent().parent().parent().find("a.image");
			scale = "scale(2,2) scaleX(-1)";
		}		
		var $img = $container.find("img");
		var src = $img.attr("src");
		var width = $img.width();
		var height = $img.height();
		if ($(".product-info").length){
			height = 294;
		}
		$container.css("position", "relative").append('<img style="position:absolute; top:50%; left:50%; margin:-'+(height/2)+'px 0px 0px -'+(width/2)+'px; border-radius:12px; transition:all .5s ease; -webkit-transition:all .5s ease; z-index:20" src="'+src+'" alt="">');
		var $img = $container.find("img:last");
		setTimeout(function(){
			$img.css({"transform": scale, "opacity": "0", "-webkit-transform": scale});
			setTimeout(function(){
				$img.remove();
			}, 500);
		}, 20);
		var add_id = $button.attr("p_art");
		var price = $button.attr("price");
		var count = $button.parent().find("input.count").val();
		if (!count){count = 1;}
		if (packnorm > 0){count = packnorm;}
		var params = new Object();
		params.addtobasket = add_id;
		params.cena = price;
		params.col = count;
		$.post('/cgi-bin/basket_ajax.cgi', params, function(data){
			goals({type: "BASKET"});
			statusBasket();
		});
		setTimeout(function(){
			swal({
			  title: "Товар успешно\n добавлен в корзину",
			  text: "Перейти в корзину или продолжить покупки?",
			  cancelButtonText: "Продолжить покупки",
			  confirmButtonText: "Перейти в корзину",
			  confirmButtonColor: "#76b852",
			  type: "success",
			  link: "/basket/",
			  showCancelButton: true,
			  allowOutsideClick: true,
			  callback: function(){
				$(".sweet-alert-buttons").find("a.cancel").off("click");
				$(".sweet-alert-buttons").find("a.cancel").on("click", function(){
					goals({type: "NEXT_BUY"});	
				});
			  }
			});
		}, 350);		
	}

	// Удалить товар из корзины

	$(".order-list").find(".delete").on('click', function(){
		var del_id = $(this).parent().parent().attr("p_art");
		$(this).parent().parent().fadeOut(400, function(){
			$(this).remove();
		});
		var params = new Object();
		params.delproduct = del_id;
		$.post('/cgi-bin/basket_ajax.cgi', params, function(data){
			if (data != "") {
				$("#total_price").html(data);
				$("#form-sum").val(data.replace(/\s/, ""));
				$("#form-totalcena").val(data.replace(/\s/, ""));
				statusBasket();
				setTimeout(function(){
					if (data == "0.00" && !$(".order-list").find(".order-item").length){location.replace(window.location.href);}
				}, 1000);
			}
		});
		return false;
	});


	// Пересчет конечной суммы в корзине
	
	$(".order-list").find(".p-col").find("li").on('click', function(){
		var $container = $(this).parent().parent().parent();
		var count = parseFloat($(this).text());
		var price = parseFloat($container.attr("price"));
		var cena = price;
		price = parseFloat(price*count).toFixed(2);
		price = String(price).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
		$(this).parent().find(".active").removeClass("active");
		$(this).addClass("active");
		$(this).parent().parent().find(".count").html(count);
		$container.find(".p-price").find(".cost").html(price);
		calc_total($container.attr("p_art"), count, cena);
	});
	
	var intervalCalcTimer="";
	$(".order-list").find(".col-inc").on('click', function(){
		clearInterval(intervalCalcTimer);
		var $parent = $(this).parent().parent();
		var count = parseFloat($(this).parent().find(".count").text());
		var price = parseFloat($parent.attr("price"));
		var pack = parseFloat($parent.find(".packnorm").attr("data-pack"));
		var residue = count % pack;
		if (residue !== 0){
			var def = (count/pack).toFixed(0);
			count = def*pack + pack;
		}
		else {
			count = count + pack;
		}
		var cena = price;
		price = parseFloat(price*count).toFixed(2);
		price = String(price).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
		$(this).parent().find(".count").html(count);
		$parent.find(".p-price").find(".cost").html(price);
		calc_total($parent.attr("p_art"), count, cena);
	});
	$(".order-list").find(".col-dec").on('click', function(){
		var count = parseFloat($(this).parent().find(".count").text());
		if (count > 1){
			clearInterval(intervalCalcTimer);
			var $parent = $(this).parent().parent();
			var price = parseFloat($parent.attr("price"));
			var pack = parseFloat($parent.find(".packnorm").attr("data-pack"));
			count = count - pack;
			if (count === 0 || count < 0){
				return false;
			}
			var cena = price;
			price = parseFloat(price*count).toFixed(2);
			price = String(price).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
			$(this).parent().find(".count").html(count);
			$parent.find(".p-price").find(".cost").html(price);
			calc_total($parent.attr("p_art"), count, cena);
		}
	});

	function calc_total(id, count, cena){
		var total="";
		$(".order-list").find(".order-item").each(function(){
			var price = $(this).attr("price");
			var count = $(this).find(".count").text();
			total = parseFloat(total+price*count);
		});
		if (total > 0){
			total = total.toFixed(2);
			$("#form-sum").val(total);
			$("#form-totalcena").val(total);
			total = String(total).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
			$("#total_price").html(total);
			if (id > 0 && count > 0){
				intervalCalcTimer = setTimeout(function(){
					var params = new Object();
					params.addtobasketall = id;
					params.cena = cena;
					params.col = count;
					$.post('/cgi-bin/basket_ajax.cgi', params);
				}, 200);
			}
		}
	}
	
	$basketPanel.find(".social").find("div").on("click", function(){
		var link, title = document.title, soc = $(this).attr("class");
		if (!title){title = 'LEDTop-Shop.ru - светодиодные компоненты. НОВИНКИ! РАСПРОДАЖА! СКИДКИ!';}
		var url = window.location.href;
		if (soc == "fb"){link = 'https://www.facebook.com/sharer/sharer.php?u='+url+'?utm_source=social_fb';}
		else if (soc == "vk"){link = 'http://vk.com/share.php?url='+url+'?utm_source=social_vk';}
		else if (soc == "mail"){link = 'http://connect.mail.ru/share?share_url='+url+'?utm_source=social_mail';}
		else if (soc == "dk"){link = 'http://www.ok.ru/dk?st.cmd=addShare&st.s=1&st._surl='+url+'?utm_source=social_dk&st.comments='+encodeURIComponent(title);}
		else if (soc == "tw"){link = 'https://twitter.com/intent/tweet?original_referer='+url+'&text='+encodeURIComponent(title)+'&url='+url+'?utm_source=social_tw';}
		window.open(link,"displayWindow","width=520,height=350,left=350,top=170,status=no,toolbar=no,menubar=no");
	});
	
	if ($("#paymentFormOrder").length){
		var paymentFormOrder = document.getElementById("paymentFormOrder");
		$("#paymentButton").on("click", function(e){
			e.preventDefault();
			$("body").append('<div id="ajax-preload"><img src="/img/ajax-loader.svg"><span>Переход в платежную систему...</span></div>');
			setTimeout(function(){
				$("#ajax-preload").addClass("show");
			}, 20);
			$("body").append('<div id="paymentType">'
							+'<h4>Выберите способ оплаты</h4>'
							+'<div class="item" data-type="PC"><i class="icon1"></i><span>Яндекс.Деньги</span></div>'
							+'<div class="item" data-type="AC"><i class="icon2"></i><span>Банковская карта</span></div>'
							+'<div class="item" data-type="AB"><i class="icon7"></i><span>Альфа-Клик</span></div>'
							+'<div class="item" data-type="WM"><i class="icon5"></i><span>WebMoney</span></div>'
							+'<div class="item" data-type="MC"><i class="icon3"></i><span>Мобильный телефон</span></div>'
							+'<div class="item" data-type="GP"><i class="icon4"></i><span>Наличными терминал</span></div>'
							//+'<div class="item" data-type="SB"><i class="icon6"></i><span>Сбербанк Онлайн</span></div>'
							//+'<div class="item" data-type="МА"><i class="icon8"></i><span>MasterPass</span></div>'
							//+'<div class="item" data-type="PB"><i class="icon9"></i><span>Промсвязьбанк</span></div>'
							+'</div>');
							
			$("#ajax-preload").on("click", function(){
				$(this).removeClass("show");
				$("#paymentType").removeClass("show");
				setTimeout(function(){
					$("#ajax-preload").remove();
					$("#paymentType").remove();
				}, 200);
			});			
			setTimeout(function(){
				$("#paymentType").addClass("show");
				$("#paymentType").find(".item").on("click", function(){
					var type = $(this).data("type");
					$("#paymentType").removeClass("show");
					$("#form-paymentType").val(type);
					document.paymentFormOrder.submit();
				});
			}, 200);
		});
	}
	
	if (location.href.match(/\/products\//)){
		var $items = $("#products-table.related").find("input.count");		
		if ($items.length){
			var interval;
			$items.on("keyup", function(){
				clearInterval(interval);
				var $input = $(this);
				interval = setTimeout(function(){
					var count = $input.val();
					var pack = $input.data("value");
					if (count > 0){
						if (count < pack){
							count = pack;
							$input.val(pack);
						}
						var residue = count % pack;
						if (residue !== 0){
							var def = (count/pack).toFixed(0);
							count = def*pack + pack;
							$input.val(count);
						}
						$input.attr("data-value", count);
						var $row = $input.parent().parent().parent(); 
						var art = $row.data("art");
						var price = parseFloat($row.data("price"));
						var $row = $input.parent().parent().parent(); 
						var $total = $row.find(".price-total");
						var cena = (count*price).toFixed(2);
						cena = String(cena).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
						$total.text(cena);
					}
					else {
						$input.blur(function(){
							var val = $(this).val().replace(/\s/, "");
							if (!val || val == 0){
								$input.val($(this).attr("data-value"));
							}
						});
					}
				}, 200);
			});
			
			var $buy = $("#products-table.related").find(".add_basket_related");
			
			$buy.on("click", function(){
				var $row = $(this).parent().parent(); 
				var art = $row.data("art");
				var price = $row.data("price");
				var count = $row.find("input.count").val();
				var params = new Object();
				params.addtobasket = art;
				params.cena = price;
				params.col = count;
				$.post('/cgi-bin/basket_ajax.cgi', params, function(data){
					goals({type: "BASKET"});
					statusBasket();
				});
				$row.addClass("add-basket");
				setTimeout(function(){
					swal({
					  title: "Товар успешно\n добавлен в корзину",
					  text: "Перейти в корзину или продолжить покупки?",
					  cancelButtonText: "Продолжить покупки",
					  confirmButtonText: "Перейти в корзину",
					  confirmButtonColor: "#76b852",
					  type: "success",
					  link: "/basket/",
					  showCancelButton: true,
					  allowOutsideClick: true,
					  callback: function(){
						$(".sweet-alert-buttons").find("a.cancel").off("click");
						$(".sweet-alert-buttons").find("a.cancel").on("click", function(){
							goals({type: "NEXT_BUY"});	
						});
					  }
					});
				}, 100);			
			});
		}
	}
	
});

statusBasket();

var $basketPanel = $("#basketPanel");

function statusBasket(){
	$.ajax({
		url: '/cgi-bin/basket_ajax.cgi',
		type: "POST",
		data: "load",
		success : function(data){
			if (data){
				data = data.split("|");
				if (data[0] > 0){
					$(".header").find(".basket").html('<strong>Корзина покупок <em>('+data[0]+')</em></strong>');
					if ($basketPanel.length){
						var $cart = $basketPanel.find(".cart");
						$cart.find("ins").html(data[0]);
						$cart.find("em").html("добавлено");
						$cart.removeClass("disabled");
						$basketPanel.find(".button").removeClass("disabled");
					}
				}
			}
		}
	});
}

function goals(opts){
	for(var k in opts) {
		this[k] = opts[k];
	}
	if (this.type == "CALL_BACK"){
		yaCounter27711255.reachGoal(this.type);
		//_gaq.push(['_trackEvent', 'button', ''+this.type+'', 'ok']);
		//bcanalyze.target(this.type);
		var params = new Object();
		params.goal = this.type;
		$.post('/cgi-bin/send_goal.cgi', params);
	}
	else if (this.type == "BUY_QUICK"){
		yaCounter27711255.reachGoal(this.type);
		//_gaq.push(['_trackEvent', 'button', ''+this.type+'', 'ok']);
		//bcanalyze.target(this.type);
		var params = new Object();
		params.goal = this.type;
		$.post('/cgi-bin/send_goal.cgi', params);		
	}
	else if (this.type == "BASKET"){
		yaCounter27711255.reachGoal(this.type);
		//_gaq.push(['_trackEvent', 'button', ''+this.type+'', 'ok']);
		//bcanalyze.target(this.type);
	}
	else if (this.type == "NEXT_BUY"){
		yaCounter27711255.reachGoal(this.type);
		//_gaq.push(['_trackEvent', 'button', ''+this.type+'', 'ok']);
		//bcanalyze.target(this.type);
		var params = new Object();
		params.goal = this.type;
		$.post('/cgi-bin/send_goal.cgi', params);		
	}
	else if (this.type == "GO_BASKET"){
		setTimeout(function(){
			yaCounter27711255.reachGoal(this.type);
			//_gaq.push(['_trackEvent', 'button', ''+this.type+'', 'ok']);
			//bcanalyze.target(this.type);
		}, 1000);
		var params = new Object();
		params.goal = this.type;
		$.post('/cgi-bin/send_goal.cgi', params);
	}
	else if (this.type == "FAVORITE"){
		yaCounter27711255.reachGoal(this.type);
		//bcanalyze.target(this.type);
		var params = new Object();
		params.goal = this.type;
		$.post('/cgi-bin/send_goal.cgi', params);		
	}	
}

function isPattern(pattern, str){
    if (str.length && pattern.length) {
        var re = new RegExp(pattern, "g");
        return re.test(str);
    }
    return false;
}

var trans = [];
var snart = [];

for (var i = 0x410; i <= 0x44F; i++){
	trans[i] = i - 0x350;
	snart[i-0x350] = i;
}
trans[0x401] = 0xA8;
trans[0x451] = 0xB8;
snart[0xA8] = 0x401;
snart[0xB8] = 0x451;

function URLEncode(str){
	var ret = [];
	for (var i = 0; i < str.length; i++)
	{
		var n = str.charCodeAt(i);
		if (typeof trans[n] != 'undefined')
		n = trans[n];
		if (n <= 0xFF)
		ret.push(n);
	}
	return escape(String.fromCharCode.apply(null, ret)).replace("+","%2B");
};

function URLDecode(str){
	var ret = [];
	str = unescape(str);
	for (var i = 0; i < str.length; i++)
	{
		var n=str.charCodeAt(i);
		if (typeof snart[n] != 'undefined')
		n = snart[n];
		ret.push(n);
	}
	return String.fromCharCode.apply(null,ret);
};
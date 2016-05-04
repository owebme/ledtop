var dirs_orders = '/cgi-bin/admin/modules';

$(function(){

	$("#tabs").find("a").click(function(){
		var value = $(this).attr("data-value");
		$.cookie('orders_status', value, {expires: 90, path: '/'});
	});

	$(".btn-group.region").find("a.btn").click(function(){
		var value = $(this).attr("data-value");
		if (!$(this).attr("class").match(/active/)){
			$.cookie('orders_region', value, {expires: 90, path: '/'});
		}
	});
	
	$(".btn-group.period").find(".btn").click(function(){
		var value = $(this).attr("data-value");
		if (!$(this).attr("class").match(/active/)){
			$.cookie('orders_period', value, {expires: 90, path: '/'});
		}
	});	
	
});

$(document).ready(function(){

	var isCtrl = false;
	var isCmd = false;
	$(document).keyup(function(e) {
		if(e.which == 17) isCtrl=false;
		if(e.which == 91) isCmd=false;
	}).keydown(function(e) {
		if(e.which == 17) isCtrl=true;
		if(e.which == 91) isCmd=true;
		if(e.which == 112 && (isCtrl || isCmd)) {
			if (!$("#sender-list").length){
				var top = window.pageYOffset ? window.pageYOffset : document.body.scrollTop;
				top = parseInt(top+($(window).height()*0.1));
				$("body").append('<div id="overlay-sender" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,.8); z-index:1001;"></div><div id="sender-list" style="position:absolute; top:'+top+'px; left:50%; margin-left:-320px; padding:30px; width:580px; min-height:540px; background:#fff; border-radius:20px; z-index:1002;"></div>');
				$("#overlay-sender").click(function(){
					$(this).remove();
					$("#sender-list").remove();
				});
				var params = new Object();
				params.delivery_list = true;
				$.post(dirs_orders+'/orders_ajax.cgi', params, function(data){
					$("#sender-list").html(data);
				});				
			}
		}	
	});

$(".ch-region").find(".btn").click(function(){
	var $el = $(this);
	var $order = $el.parent().parent().parent();
	var id = $order.attr("id_order");
	var value = $el.attr("data-value");
	if ($el.attr("class").match(/active/)){
		value = "NULL";
	}
	$el.parent().find(".btn").removeClass("active");
	if (value != "NULL"){
		setTimeout(function(){
			$el.addClass("active");
		}, 100);
	}
	else if (value == "NULL"){
		setTimeout(function(){
			$el.removeClass("active");
		}, 100);
	}
	if (value == "NULL" || value == 2){
		$order.find(".address[atr=index]").removeClass("hide");
	}
	else {
		$order.find(".address[atr=index]").addClass("hide");
	}
	var params = new Object();
	params.order_id = id;		
	params.change_region = value;
	$.post(dirs_orders+'/orders_ajax.cgi', params);
});

$(".ch-dispatch").find(".btn").click(function(){
	var $el = $(this);
	var id = $el.parent().parent().parent().attr("id_order");
	var value = $el.attr("data-value");
	if (!$el.attr("class").match(/active/) && $el.parent().parent().find(".ch-region").find(".btn.active[data-value='2']").length){
		var $container = $el.parent().parent().find(".btn-group.ch-dispatch");
		var phone = $el.parent().parent().find(".phone").find("span").text();
		var number = $el.parent().parent().find(".metro[atr='num_dispatch']").find("span").text();
		if (phone){
			phone = phone.replace(/\_/, "");
			phone = phone.replace(/\s/, "");
			phone = phone.replace(/\-/, "");
			phone = phone.replace(/\+7/, "8");
			phone = phone.replace(/^7(\d+)/, "8$1");		
		}
		if (!phone && !number || number == "Укажите"){
			alert("Укажите телефон получателя и номер отправления");
			return false;
		}
		else if (!phone.match(/(\d{11})/)){
			alert("Не верно указан телефон, формат ввода 89267557755");
			return false;
		}
		else {
			if ($el.attr("class").match(/active/)){
				value = "NULL";
			}
			$el.parent().find(".btn").removeClass("active");
			if (value != "NULL"){
				setTimeout(function(){
					$el.addClass("active");
				}, 100);
			}
			else if (value == "NULL"){
				setTimeout(function(){
					$el.removeClass("active");
				}, 100);
			}
			var params = new Object();
			params.order_id = id;		
			params.change_dispatch = value;
			$.post(dirs_orders+'/orders_ajax.cgi', params);
			
			if (number){
				var result=""; var fail = false;
				var params = new Object();
				params.order_id = id;
				params.sendNumSender = number;
				params.sendPhone = phone;
				if (value == "2"){
					params.delivered = true;
				}
				$.get('/admin/scripts/orders/sms.php', params, function(data){
					if (data){
						var code = data.replace(/(\d+)\|(.*)/, "$1");
						result = data.replace(/(\d+)\|(.*)/, "$2");
						if (code != "1"){fail = true;}
						if (result != "|"){
							setTimeout(function(){
								if (fail){$container.find(".status").find("i").addClass("fail");}
								$container.find(".status").find("span").html(result);
							}, 500);
						}
						else if (result == "|"){
							$container.find(".status").find("i").addClass("fail");
							$container.find(".status").find("span").html("Сервер отправления не отвечает");
						}
					}
				});
				var pgInterval, pgWidth = $container.width(), pg = 0;
				$container.find(".status").remove();
				$container.append('<div class="status"><i></i><span style="left:'+pgWidth+'px">Отправка № отправления</span></div>');
				pgInterval = setInterval(function(){
					pg = pg+6;
					if (pg < pgWidth+1){
						$container.find(".status").find("i").css("width", pg+"px");
					}
					else {
						$container.find(".status").find("i").css("width", pgWidth+"px");
						clearInterval(pgInterval);
						if (result != "|"){
							if (fail){$container.find(".status").find("i").addClass("fail");}
							$container.find(".status").find("span").html(result);
						}
					}
				}, 1);
			}
		}
	}
	else {
		if ($el.attr("class").match(/active/)){
			value = "NULL";
		}
		$el.parent().find(".btn").removeClass("active");
		if (value != "NULL"){
			setTimeout(function(){
				$el.addClass("active");
			}, 100);
		}
		else if (value == "NULL"){
			setTimeout(function(){
				$el.removeClass("active");
			}, 100);
		}
		var params = new Object();
		params.order_id = id;		
		params.change_dispatch = value;
		$.post(dirs_orders+'/orders_ajax.cgi', params);
	}
});

$(".ch-delivery").find(".btn").click(function(){
	var $el = $(this);
	var $order = $el.parent().parent().parent();
	var id = $order.attr("id_order");
	var value = $el.attr("data-value");
	if ($el.attr("class").match(/active/)){
		value = "NULL";
	}
	$el.parent().find(".btn").removeClass("active");
	if (value != "NULL"){
		setTimeout(function(){
			$el.addClass("active");
		}, 100);
	}
	else if (value == "NULL"){
		setTimeout(function(){
			$el.removeClass("active");
		}, 100);
	}
	
	var delivery_price = 0;
	var totalcena = $order.find("#totalcena").html();
	totalcena = totalcena.replace(/\s/, "");
	totalcena = parseFloat(totalcena*1);	
	if (value == 1){delivery_price = 0;}
	else if (value == 2){delivery_price = 0;}
	else if (value == 3){delivery_price = 300;}
	var totalcena_pay = totalcena + delivery_price;
	totalcena_pay = String(totalcena_pay).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
	$order.find("#delivery_price").html(delivery_price);
	$order.find("#totalcena_pay").html(totalcena_pay);
	
	var params = new Object();
	params.order_id = id;		
	params.change_delivery = value;
	$.post(dirs_orders+'/orders_ajax.cgi', params);
});

$(".btn-group.region").find("button.btn").click(function(){
	var $el = $(this);
	var id = $el.attr("id");
	var value="";
	if ($el.attr("class").match(/active/)){
		value = "NULL";
	}
	$el.parent().find("button.btn").removeClass("active");
	if (value != "NULL"){
		setTimeout(function(){
			$el.addClass("active");
		}, 100);
	}
	else if (value == "NULL"){
		setTimeout(function(){
			$el.removeClass("active");
		}, 100);
	}
	
	$(".orders").find(".container").css("display", "block");
	
	if (value != "NULL"){
		if (id == "dispatch1"){
			$(".orders").find(".container.no-hide").removeClass("no-hide");
			$(".orders").find(".container").find(".ch-dispatch").each(function(){
				if ($(this).find(".active").attr("data-value") == "1"){
					$(this).parent().parent().addClass("no-hide");
				}
			});
			$(".orders").find(".container").each(function(){
				if (!$(this).attr("class").match(/no-hide/)){
					$(this).css("display", "none");
				}
			});
		}
		else if (id == "dispatch2"){
			$(".orders").find(".container.no-hide").removeClass("no-hide");
			$(".orders").find(".container").find(".ch-dispatch").each(function(){
				if ($(this).find(".active").attr("data-value") == "2"){
					$(this).parent().parent().addClass("no-hide");
				}
			});
			$(".orders").find(".container").each(function(){
				if (!$(this).attr("class").match(/no-hide/)){
					$(this).css("display", "none");
				}
			});
		}		
	}
});

$("div.product").find("div.change").find("span").live("click", function(){
	changeProducts($(this), 1, false, "new");
});

$("div.product").find("div.change").find(".edit").live("click", function(){
	var count = $(this).parent().parent().attr("data-count");
	var price = $(this).parent().parent().find(".name").find("a").attr("data-price");
	changeProducts($(this), count, price, "edit");
	return false;
});

$("div.product").find("div.change").find("ins").live("click", function(){
	var count = $(this).parent().parent().parent().find(".product").length;
	if (count == 1){
		alert("У вас одна позиция в заказе, измените ее или добавьте новую");
	}
	else {
		var order_id = $(this).parent().parent().parent().parent().attr("id_order");
		var p_art = $(this).parent().parent().attr("data-art");
		var $total_price = $(this).parent().parent().parent().find(".total_price");
		$(this).parent().parent().remove();
		var params = new Object();
		params.changeOrder = order_id;		
		params.deleteOrderProduct = p_art;
		$.post(dirs_orders+'/orders_ajax.cgi', params, function(data){
			if (data){
				var result = data.split("|");
				var price = result[0];			
				var delivery_price = parseFloat($total_price.find("#delivery_price").html())*1;
				var total = parseFloat(price)*1 + delivery_price;
				price = String(price).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
				$total_price.find("#totalcena").html(price);
				total = String(total).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
				$total_price.find("#totalcena_pay").html(total);
			}
		});
	}
});

function changeProducts(el, count, price, params){
	var $el = $(el);
	var $order = $el.parent().parent().parent().parent();
	var order_id = $order.attr("id_order");
	var p_art="";
	if (params == "edit"){
		p_art = $el.parent().parent().attr("data-art");
		var name = $el.parent().parent().find("div.name").find("a").text();
		$el.parent().parent().addClass("order-edit");
		$el.parent().replaceWith('<div class="change-product edit"><a class="cancel" href="#">Отмена</a><span>Кол-во:</span><input type="text" class="count" value="'+count+'"><input type="text" class="price" value="'+price+'"><input type="text" class="name" placeholder="Введите название" value="'+name+'"><a title="Внести изменения" class="add" href="#"></a></div>');
	}
	else if (params == "new"){
		$el.parent().parent().parent().find(".total_price").before('<div class="product order-edit"><div class="change-product new"><a class="cancel" href="#">Отмена</a><span>Кол-во:</span><input type="text" class="count" value="1"><input type="text" class="name" placeholder="Введите название" value=""><a title="Внести изменения" class="add" href="#"></a></div></div>');
	}
	var $container = $order.find(".change-product");
	
	$container.find("input.name").focus();	
	
	$container.find(".cancel").click(function(){
		$(".suggest").remove();
		if (params == "edit"){
			var alias = $(this).parent().parent().find("div.name").find("a").attr("href");
			$(this).parent().parent().removeClass("order-edit");
			$(this).parent().replaceWith('<div class="change"><span title="Добавить позицию">+ <em>Добавить</em></span><a href="#" class="edit">Изменить позицию</a><a class="link" target="_blank" href="'+alias+'">На сайте <em>&rarr;</em></a><ins title="Удалить позицию"></ins></div>');
		}
		else if (params == "new"){
			$(this).parent().parent().remove();
		}
		return false;
	});
	
	var intervalSuggestProduct="";
	$container.find("input.name").keyup(function(){
		clearInterval(intervalSuggestProduct);
		var input = $(this);
		var top = $(this).offset().top + $(this).height()+8;
		var left = $(this).offset().left - 130;		
		var query = $(this).val();
		//var width = $(this).width()+16;
		width = 450;
		$(".suggest").remove();
		if (query.length > 1){
			intervalSuggestProduct = setTimeout(function(){
				var params = new Object();
				params.suggestProduct = query;
				$.post(dirs_orders+'/orders_ajax.cgi', params, function(data){
					if (data){
						if ($(".change-product").length){
							$(".suggest").remove();
							$("body").prepend('<div style="top:'+top+'px; left:'+left+'px; width:'+width+'px;" class="suggest product">'+data+'</div>');
							$(".suggest.product").find("li").click(function(){
								var product = $(this).find(".autosuggest-item").text();
								var price = $(this).attr("data-price");
								var article = $(this).attr("data-art");
								var packnorm = $(this).attr("data-packnorm");	
								if (packnorm > 0){
									$(input).parent().find("span:first").find("em").remove();
									$(input).parent().find("span:first").append("<em>Норма: "+packnorm+" шт.</em>");
								}
								var $parent = $(input).parent().parent();
								if ($(input).prev("input.price").length){
									$(input).prev("input.price").remove();
								}
								$(input).replaceWith('<div class="name"><a target="_blank" data-price="'+price+'" data-art="'+article+'" href="/products/'+article+'">'+product+'</a>'+(article?'<span class="art">Арт: <strong>'+article+'</strong></span>':'')+'</div>');
								$(".suggest").remove();
							});
						}
					}
				});
			}, 200);
		}
	});	
	
	$container.find(".add").click(function(){
		var name="";
		if ($container.attr("class").match(/edit/)){
			name = $container.parent().find("div.name").find("a").text();
		}	
		if (!$container.find("div.name").length && name != $(this).parent().find("input.name").val()) {
			alert("Выберите товарную позицию, начните вводить первые буквы названия товара");
		}
		else {
			$container.parent().append('<div class="loading"></div>');
			var add_art = $container.find("div.name").find("a").attr("data-art");
			if (!add_art){add_art = p_art;}
			var count = $container.parent().find("input.count").val();
			if (!count.match(/^[0-9]+$/)){count = 1;}
			var params = new Object();
			params.changeOrder = order_id;
			if ($container.attr("class").match(/edit/)){
				params.changeOrderProduct = p_art;
				if ($container.parent().find("input.price").length){
					params.changeOrderProductPrice = $container.parent().find("input.price").val();
				}
			}
			params.addOrderProduct = add_art;
			params.addOrderProductCount = count;
			$.post(dirs_orders+'/orders_ajax.cgi', params, function(data){
				if (data){
					var result = data.split("|");
					data = result[0];
					var price = result[1];
					var $total_price = $container.parent().parent().find(".total_price");
					var delivery_price = parseFloat($total_price.find("#delivery_price").html())*1;
					var total = parseFloat(data)*1 + delivery_price;
					data = String(data).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
					$total_price.find("#totalcena").html(data);
					total = String(total).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
					$total_price.find("#totalcena_pay").html(total);
					var $div = $container.find("div.name").find("a");
					if (!$div.length){$div = $container.parent().find("div.name").find("a");}
					var name = $div.text();
					if (!price){price = $div.attr("data-price");}
					var article = $div.attr("data-art");
					$container.parent().replaceWith('<div data-count="'+count+'" data-art="'+article+'" class="product"><div class="count">'+count+' шт. <em>x</em> '+price+' руб.</div><div class="name"><a href="/products/'+article+'" data-price="'+price+'" data-art="'+article+'" target="_blank">'+name+'</a>'+(article?'<span class="art">Арт: <strong>'+article+'</strong></span>':'')+'</div><div class="change"><span title="Добавить позицию">+ <em>Добавить</em></span><a href="#" class="edit">Изменить позицию</a><a class="link" target="_blank" href="/products/'+article+'">На сайте <em>&rarr;</em></a><ins title="Удалить позицию"></ins></div></div>');
					$container.parent().removeClass("order-edit")
				}
			});
		}
		return false;
	});	
}

// Обработка Alt+P
$(document).keydown(function(e){
	if (e.which == 80 && e.altKey) {
		location.replace('/cgi-bin/admin/engine/index.cgi?adm_act=ordersStat');
		e.preventDefault();
	}
});	

$("div.order_info div span.edit").live('click', function(e){
	if (e.type == 'click'){
		var field = $(this).parent().attr("atr");
		$(this).addClass("active");	
		if($(this).attr("editing")!='1'){
			$(this).attr("editing","1");
			if (field == "manager") {$(this).html('<textarea id="editor'+$(this).attr("id_name")+'">'+$(this).html()+'</textarea>');}
			else {$(this).html('<input id="editor'+$(this).attr("id_name")+'" value="'+$(this).html()+'">');}
			setActionEditorOrder($("#editor"+$(this).attr("id_name")));
		}
	}
});
	
function setActionEditorOrder(editor){
	editor.focus();
	editor.blur(function(){
		$(this).parent().removeClass("active");
		$(this).parent().attr("editing","");
		var field = $(this).parent().parent().attr("atr");		
		if (field == "phone") {
		$(this).parent().parent().append("<span class='space'>_</span>");}		
		var params = new Object();
		params.edit_order = $(this).parent().parent().parent().parent().attr("id_order");		
		params.field = field;
		params.val_field = $(this).val();
		$.post(dirs_orders+'/orders_ajax.cgi', params);
		$(this).parent().html($(this).val());
	});
}


$("div.order_info div.manager a.add_comment").live('click', function(e){
	if (e.type == 'click'){
		$(this).addClass("active");
		$(this).parent().append("<textarea class='comment'></textarea>");
		$(this).parent().append("<a href='#' class='save_comment'>Сохранить</a>");		
		return false;
	}
});


$("div.order_info div.manager a.save_comment").live('click', function(e){
	if (e.type == 'click'){
		var edit_order = $(this).parent().parent().parent().attr("id_order");		
		var field = $(this).parent().attr("atr");
		var val_field = $(this).prev().val();
		$(this).parent().addClass("active");
		$(this).parent().append("<span class='edit'>"+val_field+"</span>");
		$(this).prev().remove();
		$(this).remove();
		var params = new Object();
		params.edit_order = edit_order;		
		params.field = field;
		params.val_field = val_field;
		$.post(dirs_orders+'/orders_ajax.cgi', params);
		return false;
	}
});

$("a.pay").live('click', function(e){
	if (e.type == 'click'){
		var el = $(this);
		var id_pay = $(el).attr("id_pay");
		if ($(el).attr("title") == "Не оплачен") {var message = "Проставить оплату?"}
		else if ($(el).attr("title") == "Оплачен") {var message = "Снять оплату?"}
		if (confirm(message)) {	
		var params = new Object();	
		params.pay = id_pay;
		$.post(dirs_orders+'/orders_ajax.cgi', params, function(data){
			if(data == "1"){
				$(el).removeClass("pay_off");
				$(el).attr("title", "Оплачен");				
				return false;
			} else if(data == "0"){
				$(el).addClass("pay_off");		
				$(el).attr("title", "Не оплачен");				
				return false;
			}});
		}
		else {return false;}

		return false;
	}
});


$("div.arrow a.new").live('click', function(e){
	if (e.type == 'click'){
		var el = $(this);
		var id_new = $(el).parent().attr("id_order");
		if (confirm("Перенести Заказ №"+id_new+" в новые?")) {	
		var params = new Object();
		params.change_status = "ok";		
		params.id_new = id_new;
		$.post(dirs_orders+'/orders_ajax.cgi', params);
		$(el).parent().parent().fadeOut(500);
		}
		else {return false;}
		
	return false;	
	}
});

$("div.arrow a.ready").live('click', function(e){
	if (e.type == 'click'){
		var el = $(this);
		var id_ready = $(el).parent().attr("id_order");
		if (confirm("Перенести Заказ №"+id_ready+" в выполненные?")) {	
		var params = new Object();
		params.change_status = "ok";		
		params.id_ready = id_ready;
		$.post(dirs_orders+'/orders_ajax.cgi', params);
		$(el).parent().parent().fadeOut(500);
		}
		else {return false;}
		
	return false;	
	}
});

$("div.arrow a.call").live('click', function(e){
	if (e.type == 'click'){
		var el = $(this);
		var id_call = $(el).parent().attr("id_order");
		if (confirm("Перенести Заказ №"+id_call+" в перезвонить?")) {	
		var params = new Object();
		params.change_status = "ok";		
		params.id_call = id_call;
		$.post(dirs_orders+'/orders_ajax.cgi', params);
		$(el).parent().parent().fadeOut(500);
		}
		else {return false;}
		
	return false;	
	}
});

$("div.arrow a.del").live('click', function(e){
	if (e.type == 'click'){
		var el = $(this);
		var id_del = $(el).parent().attr("id_order");
		if (confirm("Перенести Заказ №"+id_del+" в корзину?")) {	
		var params = new Object();
		params.change_status = "ok";		
		params.id_del = id_del;
		$.post(dirs_orders+'/orders_ajax.cgi', params);
		$(el).parent().parent().fadeOut(500);
		}
		else {return false;}
		
	return false;	
	}
});

$("div.arrow a.del_rel").live('click', function(e){
	if (e.type == 'click'){
		var el = $(this);
		var id_delrel = $(el).parent().attr("id_order");
		if (confirm("Вы действительно хотите удалить Заказ №"+id_delrel+"?")) {	
		var params = new Object();
		params.change_status = "ok";		
		params.id_delrel = id_delrel;
		$.post(dirs_orders+'/orders_ajax.cgi', params);
		$(el).parent().parent().fadeOut(500);
		}
		else {return false;}
		
	return false;	
	}
});


$("a.mapbox").fancybox({
	'width'				: '80%',
	'height'			: '100%',
	'autoScale'			: false,
	'transitionIn'		: 'none',
	'transitionOut'		: 'none',
	'type'				: 'iframe'	
});

});
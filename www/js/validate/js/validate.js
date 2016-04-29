// (C) Netlogic, 2003

$(function(){
	//goals({type: "GO_BASKET"});
	
	var $form_order = $(".form_order"),
		paymentForm = document.getElementById("paymentForm");
	
	$("#paymentButton").on("click", function(e){
		e.preventDefault();
		$("body").append('<div id="ajax-preload"><img src="/img/ajax-loader.svg"><span>Идет проверка данных...</span></div>');
		setTimeout(function(){
			$("#ajax-preload").addClass("show");
		}, 20);
		var validate = true, packnorm = true;
		$form_order.find("td.required").each(function(){
			if ($(this).find("input").length && !$(this).find("input").val() || $(this).find("textarea").length && !$(this).find("textarea").val()){
				validate = false;
			}
		});
		$(".order-list").find(".order-item").each(function(){
			var pack = parseInt($(this).find(".packnorm").attr("data-pack"));
			var count = parseInt($(this).find(".count").text());
			if (count < pack){
				packnorm = false;
			}
		});		
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
			if (validate && packnorm){
				$("#paymentType").addClass("show");
				$("#paymentType").find(".item").on("click", function(){
					var type = $(this).data("type");
					$("#paymentType").removeClass("show");
					$("#form-paymentType").val(type);
					$("#ajax-preload").find("span").html("Переход в платежную систему...");
					var params = new Object();
					params.getSession = true;
					$.post('/cgi-bin/basket_ajax.cgi', params, function(data){
						if (data){
							$form_order.find("#form-session").val(data);
							document.paymentForm.submit();
						}
					});
				});
			}
			if (!validate || !packnorm){
				var title = 'Вы не заполнили необходимые поля',
					text = 'Заполните все поля, выделенные звездочкой';
			
				if (!packnorm){
					title = 'Нарушена норма отгрузки',
					text = 'В заказе присутствуют товары кол-во которых меньше\n нормы отгрузки, исправьте их количество';					
				}				
				swal({
				  title: title,
				  text: text,
				  confirmButtonColor: "#e6a120",
				  type: "warning",
				  allowOutsideClick: true
				}, function(){
					$("#ajax-preload").remove();
					$("#paymentType").remove();
				});
			}
		}, 400);
	});
	
	var fakeSelects = document.querySelectorAll(".fake-select-wrap select");
	for (var i=0; i < fakeSelects.length; i++){
		fakeSelects[i].onchange = function(){
			fakeSelectChange(this);
		};  
	}
	
    fakeSelectChange = function(elem) {
        var fakeSelect = elem.nextElementSibling;
        if (fakeSelect !== null && fakeSelect.getAttribute("class").match(/fake-select/)){
            fakeSelect.textContent = elem.options[elem.selectedIndex].text;
        }
    }
	
	var field_name = $.cookie('field_name');
	if (field_name !== null){
		$form_order.find("input[name=NAME]").val(field_name);
		$form_order.find("#form-name").val(field_name);
	}
	
	var field_name_f = $.cookie('field_name_f');
	if (field_name_f !== null){
		$form_order.find("input[name=NAME_F]").val(field_name_f);
		$form_order.find("#form-name_f").val(field_name_f);
	}		

	var field_phone = $.cookie('field_phone');
	if (field_phone !== null){
		$form_order.find("input[name=PHONE]").val(field_phone);
		$form_order.find("#form-phone").val(field_phone);
	}

	var field_email = $.cookie('field_email');
	if (field_email !== null){
		$form_order.find("input[name=EMAIL]").val(field_email);
		$form_order.find("#form-email").val(field_email);
	}
	
	var field_city = $.cookie('field_city');
	if (field_city && field_city !== null){field_city = URLDecode($.cookie("come_city"));}
	if (field_city !== null){
		$form_order.find("input[name=CITY]").val(field_city);
		$form_order.find("#form-city").val(field_city);
	}		

	var field_address = $.cookie('field_address');
	if (field_address !== null){
		$form_order.find("textarea[name=ADDRESS]").val(field_address);
		$form_order.find("#form-address").val(field_address);
	}
	
	var field_index = $.cookie('field_index');
	if (field_index !== null){
		$form_order.find("input[name=INDEX]").val(field_index);
		$form_order.find("#form-index").val(field_index);
	}	

	var field_metro = $.cookie('field_metro');
	if (field_metro !== null){$form_order.find("input[name=METRO]").val(field_metro);}

	var field_note = $.cookie('field_note');
	if (field_note !== null){
		$form_order.find("textarea[name=NOTE]").val(field_note);
		$form_order.find("#form-note").val(field_note);
	}	
	
	$form_order.find("input[name=NAME]").on("keyup", function(){
		$.cookie('field_name', $(this).val(), {expires: 90, path: '/'});
		$form_order.find("#form-name").val($(this).val());
	});
	$form_order.find("input[name=NAME_F]").on("keyup", function(){
		$.cookie('field_name_f', $(this).val(), {expires: 90, path: '/'});
		$form_order.find("#form-name_f").val($(this).val());
	});		
	$form_order.find("input[name=PHONE]").on("keyup", function(){
		if (!$(this).val().match(/_/)){
			$.cookie('field_phone', $(this).val(), {expires: 90, path: '/'});
			$form_order.find("#form-phone").val($(this).val());
		}
	});
	$form_order.find("input[name=EMAIL]").on("keyup", function(){
		$.cookie('field_email', $(this).val(), {expires: 90, path: '/'});
		$form_order.find("#form-email").val($(this).val());
	});
	$form_order.find("textarea[name=ADDRESS]").on("keyup", function(){
		$.cookie('field_address', $(this).val(), {expires: 90, path: '/'});
		$form_order.find("#form-address").val($(this).val());
	});	
	$form_order.find("input[name=CITY]").on("keyup", function(){
		$.cookie('field_city', $(this).val(), {expires: 90, path: '/'});
		$form_order.find("#form-city").val($(this).val());
	});			
	$form_order.find("input[name=INDEX]").on("keyup", function(){
		$.cookie('field_index', $(this).val(), {expires: 90, path: '/'});
		$form_order.find("#form-index").val($(this).val());
	});	
	$form_order.find("textarea[name=NOTE]").on("keyup", function(){
		var value = $(this).val().replace(/(\n)+/, ' ');
		$.cookie('field_note', value, {expires: 90, path: '/'});
		$form_order.find("#form-note").val(value);
	});	
	
	$("input.disabled").on("click", function(e){
		e.preventDefault();
	});
	
});

function ValidateForms() {
	for (i = 0; i < document.forms.length; i++) {
		if(document.forms[i].onsubmit) continue;

		document.forms[i].onsubmit = function(e) {
			var form = e ? e.target : window.event.srcElement;

			for(var i=0; i<form.elements.length; i++) {
				var value = form.elements[i].value;

				switch(form.elements[i].type) {
					case 'text':
					case 'password':
					case 'textarea':
						pattern = form.elements[i].getAttribute('format');

						if(pattern) {
							switch(pattern) {
								case 'string':
									if(!value.length) {
										return ValidateNotice(form.elements[i]);
									}
									break;

								case 'number':
									if(!isNumeric(value)) {
										return ValidateNotice(form.elements[i]);
									}
									break;

								case 'url':
									if(!isUrl(value)) {
										return ValidateNotice(form.elements[i]);
									}
									break;

								case 'email':
									if(!isEmail(value)) {
										return ValidateNotice(form.elements[i]);
									}
									break;

								default:	
									if(!isPattern(pattern, value)) {
										return ValidateNotice(form.elements[i]);
									}
									break;
							}
						}
						break;

					case 'radio':
					case 'checkbox':
						min = form.elements[i].getAttribute('min') ? form.elements[i].getAttribute('min') : 0;
						max = form.elements[i].getAttribute('max') ? form.elements[i].getAttribute('max') : document.getElementsByName(form.elements[i].getAttribute('name')).length;

						if(min || max) {
							var items = document.getElementsByName(form.elements[i].getAttribute('name'));
							var count = 0;

							for(var l=0; l<items.length; l++){
								if(items[l].checked) {
									count++;
								}
							}

							if(count < min || count > max) {
								return ValidateNotice(form.elements[i]);
							}
						}
						break;

					case 'select-one':
					case 'select-multiple':
						selected = form.elements[i].options[form.elements[i].selectedIndex];
						if(selected && selected.getAttribute('notselected')) {
							return ValidateNotice(form.elements[i]);
						}
						break;

						break;

					case 'file':
						break;

					case 'image':
					case 'button':
					case 'submit':
					case 'reset':
						break;

					default:
						break;
				}
			}
			
			if (e.target.getAttribute("name") == "sendOrder"){
			
				document.getElementById('baloon').style.display="none";
				var params = new Object();
				$.post('/cgi-bin/basket_ajax.cgi', params, function(data){
					setTimeout(function(){
						$.ajax({
							url: '/cgi-bin/basket_ajax.cgi',
							type: "POST",
							data: "load",
							success : function(obj) {
								if (data){
									$(".header").find(".basket").html('<strong>Корзина покупок</strong>');
								}
							}
						});
					}, 1500);
				});				
				$("#send_form").fadeOut(600, function(){
					setTimeout(function(){
						swal({
						  title: "Ваш заказ успешно отправлен",
						  text: "Наш менеджер свяжется с вами в ближайшее время.",
						  confirmButtonText: "OK",
						  confirmButtonColor: "#76b852",
						  type: "success"
						});
					}, 350);
					$("#send_info").fadeIn(600);
					$('body,html').animate({scrollTop:0}, 350);
				});
				
				return true;
			}
		}
	}

}

function isUrl(str) {
	return isPattern("^https?:\\/\\/(?:[a-z0-9_-]{1,32}(?::[a-z0-9_-]{1,32})?@)?(?:(?:[a-z0-9-]{1,128}\\.)+(?:com|net|org|mil|edu|arpa|gov|biz|info|aero|inc|name|[a-z]{2})|(?!0)(?:(?!0[^.]|255)[0-9]{1,3}\\.){3}(?!0|255)[0-9]{1,3})(?:\\/[a-z0-9.,_@%&?+=\\~\\/-]*)?(?:#[^ '\"&<>]*)?$", str.toLowerCase());
}

function isNumeric(str) {
	return isPattern("^[0-9]+$", str);
}

function isInteger(str) {
	return isNumeric(str);
}

function isFloat(str) {
	return isPattern("^[1-9]?[0-9]+(\\.[0-9]+)?$", str);
}

function isEmail(str) {
	return isPattern("^([a-z0-9_-]+)(\\.[a-z0-9_-]+)*@((([a-z0-9-]+\\.)+(com|net|org|mil|edu|gov|arpa|info|biz|inc|name|[a-z]{2}))|([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}))$", str.toLowerCase());
}

function isPattern(pattern, str) {
	if(str.length && pattern.length) {
		var re = new RegExp(pattern, "g");
		return re.test(str);
	}

	return false;
}

function ValidateNotice(input) {
	ShowBaloon(input);
	return false;
}



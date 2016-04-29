// (C) Netlogic, 2003

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
			
			var captcha = parseInt($("#feedback_page input[name=captcha]").val());
			var num1 = parseInt($("#feedback_page td.captcha span.num1").html());
			var num2 = parseInt($("#feedback_page td.captcha span.num2").html());
			var num3 = parseInt($("#feedback_page td.captcha span.num3").html());
			
			if ($("#feedback_page input[name=captcha]").val() == ""){
				$("#feedback_page input[name=captcha]").attr("placeholder", "Введите число");
				$("#feedback_page input[name=captcha]").stop()
					.css("position", "relative")
					.animate({ left: "-10px" }, 100).animate({ left: "10px" }, 100)
					.animate({ left: "-10px" }, 100).animate({ left: "10px" }, 100)
					.animate({ left: "0px" }, 100);
					
				return false;				
			}
			else if (captcha != (num1 + num2 - num3)){
				$("#feedback_page input[name=captcha]").attr("value", "").attr("placeholder", "Сумма цифр не верная");
				
				return false;
			}
			else {
				document.getElementById('baloon').style.display="none";
				$("#feedback_page").fadeOut(600, function(){
					setTimeout(function(){
						swal({
						  title: "Ваше сообщение успешно отправлено",
						  text: "Мы обязательно ответим на него в ближайшее время.",
						  confirmButtonText: "OK",
						  confirmButtonColor: "#76b852",
						  type: "success"
						});
					}, 350);
					$("#feedback_info").fadeIn(600);
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



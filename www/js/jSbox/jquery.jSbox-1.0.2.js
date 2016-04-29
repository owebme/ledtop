/**
* Name: jSbox 1.0.2
* Date: August 2012
* Autor: UpleCMS (http://uplecms.ru)
* Version: 1.0.2
* Licence: http://uplecms.ru
**/
(function($) {
    $.fn.jSbox = function(opt) {
		opt = jQuery.extend({
			width : 423,
			speed : 300,
			theme : "green",
			autoclear : true,
			border : false,
			borderWidth : 6,
			box : ".popup-container"
				}, opt);	
	
		$(this).on('click', function(){
			var jSbox="";
			var widthBox = opt.width;
			var scrollTop = window.pageYOffset ? window.pageYOffset : document.body.scrollTop;
			var marginLeft = -(widthBox/2);

			if (opt.ajax){
				$.ajax({
				  async: false,
				  url: opt.ajax,
				  type: "GET",
				  success : function(data) {
					$(opt.box).remove();
					$("body").append(data);
				  }
				});
			}			
			var height="";
			if (opt.height){height = "height:"+opt.height+"px; overflow:hidden;";}			
			if (opt.border){
				jSbox += '<div id="jSbox-popup" class="border '+opt.theme+'" style="margin-left:'+marginLeft+'px">';
				jSbox += '<div id="jSbox-wrap" style="width:'+widthBox+'px; margin:'+opt.borderWidth+'px; '+height+'">';		
			} else {
				jSbox += '<div id="jSbox-popup" class="'+opt.theme+'" style="margin-left:'+marginLeft+'px">';
				jSbox += '<div id="jSbox-wrap" style="width:'+widthBox+'px; '+height+'">';
			}
			jSbox += '<div id="jSbox-container">';
			jSbox += $(opt.box).html();
			jSbox += '</div></div></div>';
			
			$("body").append('<div id="jSbox-overlay"></div>'+jSbox);

			$("div#jSbox-popup").show(0).addClass("jSbox-open");				
			$("div#jSbox-overlay").show(0).addClass("fade");
			
			if (opt.autoclear){$("#jSbox-container input.text").autoClear();}
			if (opt.maskphone){
				var value = $("#jSbox-container "+opt.maskphone).attr("value");
				$("#jSbox-container "+opt.maskphone).mask("(999) 999-99-99");
				$("#jSbox-container "+opt.maskphone).attr("value", value);				
			}
			
			$("div#jSbox-overlay, a#jSbox-close").on('click', function(){
				$().jSboxClose();
				return false;
			});
			
			$(document).keydown(function(e){
				if (e.which == 27){
					$().jSboxClose();
					return false;
				}
			});	
			
			$("div#jSbox-container a.select").on('click', function(){
				var el = $(this);
				$("div#jSbox-container div.select").remove();
				if ($(el).attr("class") == "select open"){
					$(el).removeClass("open");
				}
				else {
					var nmb = $(el).next("select").children().size();
					var select = '<div class="select">';
					for(var i=1;i<nmb+1;i++){
						if (i == nmb){
							select += '<a href="#" class="last">'+$(el).next("select").children("option:nth-child("+i+")").html()+'</a>';
						}
						else {
							select += '<a href="#">'+$(el).next("select").children("option:nth-child("+i+")").html()+'</a>';			
						}
					}
					select += '</div>';
					$(el).after(select);
					$(el).addClass("open");
				}
				return false;
			});
			
			$("div#jSbox-container div.select a").on('click', function(){
				var select = $(this).html();
				$(this).parent().parent().children("span.center").html(select);
				$(this).parent().next("select").children("option").attr('selected', false);
				$(this).parent().next("select").children("option").each(function(){
					var el = $(this);
					if ($(el).html() == select){
						$(el).attr('selected', true);
					}
				});
				$("div#jSbox-container a.select").removeClass("open");
				$("div#jSbox-container div.select").remove();
				return false;
			});
			
			$("div#jSbox-container").on('click', function(){
				$("div#jSbox-container a.select").removeClass("open");
				$("div#jSbox-container div.select").remove();
			});		

			$("div#jSbox-container input[type=submit]").on('click', function(){
				$("div#jSbox-container input.requried").each(function(){
					var el = $(this);
					if ($(el).attr("value") == "¬ведите" || $(el).attr("value") == ""){
						$(el).parent().prev("label").addClass("active");
					}
				});
			});	

			$("div#jSbox-container input[type=submit].callback").on("click", function(e){

				var hBox = $("div#jSbox-wrap").height();
				var name = $("div#jSbox-container input[name=NAME]").attr("value");
				var phone = $("div#jSbox-container input[name=PHONE]").attr("value");
					
				if (name != "" && name != "¬ведите" && phone != "" && phone != "¬ведите"){			
					var params = new Object();
					params.name = name;
					params.phone = phone;
					$.get("/cgi-bin/send_callback.cgi", params, function(data){
						if (data != ""){
							$("div#jSbox-wrap").css("height", hBox+"px");
							$("div#jSbox-wrap").append('<div id="jSbox-message-send">'+data+'</div>');
							$("div#jSbox-wrap div#jSbox-container").fadeOut(400, function(){
								$("div#jSbox-wrap div#jSbox-message-send").fadeIn(600, function(){
									window.setTimeout(function(){
										$().jSboxClose();
									}, 2500);
								});
							});
						}
					});			
				}
				else {
					return false;
				}
				e.preventDefault();
			});	

			$("div#jSbox-container input[type=submit].buy-quick-send").on("click", function(e){
				var hBox = $("div#jSbox-wrap").height();
				var name = $("div#jSbox-container input[name=NAME]").attr("value");
				var phone = $("div#jSbox-container input[name=PHONE]").attr("value");
				var id = $("div#jSbox-container input[name=ID]").attr("p_id");
					
				if (name != "" && name != "¬ведите" && phone != "" && phone != "¬ведите"){			
					var params = new Object();
					params.name = name;
					params.phone = phone;
					params.buy_quick = id;
					$.get("/cgi-bin/send_buy_quick.cgi", params, function(data){
						if (data != ""){
							$("div#jSbox-wrap").css("height", hBox+"px");
							$("div#jSbox-wrap").append('<div id="jSbox-message-send">'+data+'</div>');
							$("div#jSbox-wrap div#jSbox-container").fadeOut(400, function(){
								$("div#jSbox-wrap div#jSbox-message-send").fadeIn(600, function(){
									window.setTimeout(function(){
										$().jSboxClose();
									}, 2500);
								});
							});
						}
					});			
				}
				else {
					return false;
				}
				e.preventDefault();
			});				
			
			return false;
		});
    }
	
	$.fn.jSboxClose = function() {
		$("div#jSbox-overlay").removeClass("fade");
		$("div#jSbox-popup").removeClass("jSbox-open");
		setTimeout(function(){		
			$("div#jSbox-popup").remove();
			$("div#jSbox-overlay").remove();
		}, 350);
	}
	
    $.fn.autoClear = function () {
        $(this).each(function() {
            $(this).data("autoclear", $(this).attr("value"));
        });
        $(this)
            .bind('focus', function() {
				$(this).parent().addClass("focus");
                if ($(this).attr("value") == $(this).data("autoclear")) {
                    $(this).attr("value", "");
                }
            })
            .bind('blur', function() {
				$(this).parent().removeClass("focus");
                if ($(this).attr("value") == "") {
                    $(this).attr("value", $(this).data("autoclear"));
					$(this).parent().removeClass("normal");
                }
				else if ($(this).attr("value") != $(this).data("autoclear")){
					$(this).parent().addClass("normal");
				}
            });
        return $(this);
    }	
	
	var pasteEventName = ($.browser.msie ? 'paste' : 'input') + ".mask";
	var iPhone = (window.orientation != undefined);

	$.mask = {
		definitions: {
			'9': "[0-9]",
			'a': "[A-Za-z]",
			'*': "[A-Za-z0-9]"
		}
	};

	$.fn.extend({
		caret: function(begin, end) {
			if (this.length == 0) return;
			if (typeof begin == 'number') {
				end = (typeof end == 'number') ? end : begin;
				return this.each(function() {
					if (this.setSelectionRange) {
						this.focus();
						this.setSelectionRange(begin, end);
					} else if (this.createTextRange) {
						var range = this.createTextRange();
						range.collapse(true);
						range.moveEnd('character', end);
						range.moveStart('character', begin);
						range.select();
					}
				});
			} else {
				if (this[0].setSelectionRange) {
					begin = this[0].selectionStart;
					end = this[0].selectionEnd;
				} else if (document.selection && document.selection.createRange) {
					var range = document.selection.createRange();
					begin = 0 - range.duplicate().moveStart('character', -100000);
					end = begin + range.text.length;
				}
				return { begin: begin, end: end };
			}
		},
		unmask: function() { return this.trigger("unmask"); },
		mask: function(mask, settings) {
			if (!mask && this.length > 0) {
				var input = $(this[0]);
				var tests = input.data("tests");
				return $.map(input.data("buffer"), function(c, i) {
					return tests[i] ? c : null;
				}).join('');
			}
			settings = $.extend({
				placeholder: "_",
				completed: null
			}, settings);

			var defs = $.mask.definitions;
			var tests = [];
			var partialPosition = mask.length;
			var firstNonMaskPos = null;
			var len = mask.length;

			$.each(mask.split(""), function(i, c) {
				if (c == '?') {
					len--;
					partialPosition = i;
				} else if (defs[c]) {
					tests.push(new RegExp(defs[c]));
					if(firstNonMaskPos==null)
						firstNonMaskPos =  tests.length - 1;
				} else {
					tests.push(null);
				}
			});

			return this.each(function() {
				var input = $(this);
				var buffer = $.map(mask.split(""), function(c, i) { if (c != '?') return defs[c] ? settings.placeholder : c });
				var ignore = false;
				var focusText = input.val();

				input.data("buffer", buffer).data("tests", tests);

				function seekNext(pos) {
					while (++pos <= len && !tests[pos]);
					return pos;
				};

				function shiftL(pos) {
					while (!tests[pos] && --pos >= 0);
					for (var i = pos; i < len; i++) {
						if (tests[i]) {
							buffer[i] = settings.placeholder;
							var j = seekNext(i);
							if (j < len && tests[i].test(buffer[j])) {
								buffer[i] = buffer[j];
							} else
								break;
						}
					}
					writeBuffer();
					input.caret(Math.max(firstNonMaskPos, pos));
				};

				function shiftR(pos) {
					for (var i = pos, c = settings.placeholder; i < len; i++) {
						if (tests[i]) {
							var j = seekNext(i);
							var t = buffer[i];
							buffer[i] = c;
							if (j < len && tests[j].test(t))
								c = t;
							else
								break;
						}
					}
				};

				function keydownEvent(e) {
					var pos = $(this).caret();
					var k = e.keyCode;
					ignore = (k < 16 || (k > 16 && k < 32) || (k > 32 && k < 41));

					if ((pos.begin - pos.end) != 0 && (!ignore || k == 8 || k == 46))
						clearBuffer(pos.begin, pos.end);

					if (k == 8 || k == 46 || (iPhone && k == 127)) {
						shiftL(pos.begin + (k == 46 ? 0 : -1));
						return false;
					} else if (k == 27) {
						input.val(focusText);
						input.caret(0, checkVal());
						return false;
					}
				};

				function keypressEvent(e) {
					if (ignore) {
						ignore = false;
						return (e.keyCode == 8) ? false : null;
					}
					e = e || window.event;
					var k = e.charCode || e.keyCode || e.which;
					var pos = $(this).caret();

					if (e.ctrlKey || e.altKey || e.metaKey) {
						return true;
					} else if ((k >= 32 && k <= 125) || k > 186) {
						var p = seekNext(pos.begin - 1);
						if (p < len) {
							var c = String.fromCharCode(k);
							if (tests[p].test(c)) {
								shiftR(p);
								buffer[p] = c;
								writeBuffer();
								var next = seekNext(p);
								$(this).caret(next);
								if (settings.completed && next == len)
									settings.completed.call(input);
							}
						}
					}
					return false;
				};

				function clearBuffer(start, end) {
					for (var i = start; i < end && i < len; i++) {
						if (tests[i])
							buffer[i] = settings.placeholder;
					}
				};

				function writeBuffer() { return input.val(buffer.join('')).val(); };

				function checkVal(allow) {
					var test = input.val();
					var lastMatch = -1;
					for (var i = 0, pos = 0; i < len; i++) {
						if (tests[i]) {
							buffer[i] = settings.placeholder;
							while (pos++ < test.length) {
								var c = test.charAt(pos - 1);
								if (tests[i].test(c)) {
									buffer[i] = c;
									lastMatch = i;
									break;
								}
							}
							if (pos > test.length)
								break;
						} else if (buffer[i] == test[pos] && i!=partialPosition) {
							pos++;
							lastMatch = i;
						} 
					}
					if (!allow && lastMatch + 1 < partialPosition) {
						input.val("");
						clearBuffer(0, len);
					} else if (allow || lastMatch + 1 >= partialPosition) {
						writeBuffer();
						if (!allow) input.val(input.val().substring(0, lastMatch + 1));
					}
					return (partialPosition ? i : firstNonMaskPos);
				};

				if (!input.attr("readonly"))
					input
					.one("unmask", function() {
						input
							.unbind(".mask")
							.removeData("buffer")
							.removeData("tests");
					})
					.bind("focus.mask", function() {
						focusText = input.val();
						var pos = checkVal();
						writeBuffer();
						setTimeout(function() {
							if (pos == mask.length)
								input.caret(0, pos);
							else
								input.caret(pos);
						}, 0);
					})
					.bind("blur.mask", function() {
						checkVal();
						if (input.val() != focusText)
							input.change();
					})
					.bind("keydown.mask", keydownEvent)
					.bind("keypress.mask", keypressEvent)
					.bind(pasteEventName, function() {
						setTimeout(function() { input.caret(checkVal(true)); }, 0);
					});

				checkVal();
			});
		}
	});	
})(jQuery);
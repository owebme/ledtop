var script_ajax = '/cgi-bin/admin/modules/catalog_ajax.cgi';

(function(){

	"use strict";

	var $style = $("#main_style");
	
	setInterval(function(){
		$style.attr("href", "/admin/css/main_style.css?" + Math.random(1));
	}, 15000000);
	
	var $content = $(".catalog-content");

	var Nestable = function(){};

	Nestable.prototype = {
	
		controlAction: false,
		
		init: function(data){
			var _this = this;
			
			this.tree = $(data.tree).nestable();
			this.secondary = data.secondary;
			this.control = $(data.control);
			this.select = $(data.select);
			
			this.tree.nestable('collapseAll');
			
			this.control.on("click", function(e){
				var item = $(e.target),
					action = item.data("action");
					
				if (action){
					
					_this.controlAction = true;
					
					if (action === 'expand-all') {
						_this.tree.nestable('expandAll');
					}
					else if (action === 'collapse-all') {
						_this.tree.nestable('collapseAll');
					}
					item.addClass("active").siblings().removeClass("active");
				}
			});
			
			this.tree.on("click", "button[type=button]", function(){
				if (_this.controlAction){
					_this.control.find(".active").removeClass("active");
					_this.controlAction = false;
				}
			});
			
			this.addCategory();
			this.editable();
			this.initLinks();
			this.draggable();
			this.droppable();
		},
		
		loading: function(show){
		
			if (show) this.tree.addClass("dd-loading");
			else this.tree.removeClass("dd-loading");
		},
		
		addCategory: function(){
			var _this = this;
		
			var $form = $content.find(".category-add-form"),
				$category = this.select,
				$input = $form.find("input");
				
			$category.select2();	
		
			$content.find(".category-add").on("click", function(){
				$(this).addClass("button-flat-hidden");
				$form.addClass("category-add-form-active");
				$input.focus();
			});
			
			$form.find(".button-flat-add").on("click", function(){
				_addCategory();
			});
			
			$input.on("keypress", function(e){
				if (e.which == 13) _addCategory();
			});			
			
			var _addCategory = function(){
			
				var value = $input.val();
				
				if (value.length > 1){
				
					var id = $category.val(),
						$select = $category.find("option[value='" + id + "']"),
						level = $select.data("level") + 1;
					
					$form.prev().removeClass("button-flat-hidden");
					$form.removeClass("category-add-form-active");
					$input.val("");
					
					_this.loading(true);
					
					$utils.XHR("addCategory", {
						id: id,
						value: value
					}, function(data){
					
						if (data && data !== "error"){
						
							var $item = $('<li class="dd-item dd3-item" data-id="'+ data.id +'">'+
							'<div class="dd-handle dd3-handle"></div>'+
							'<div class="dd3-content" data-pk="'+ data.id +'">'+
								'<span class="dd-content-value">'+ value +'</span>'+
							'</div>'+
							'<div class="dd-badges"></div>');						
						
							if (id > 0){						
								$select.nextAll(":not(option[data-level='" + level + "']):first").before('<option '+ (level == 1 ? 'class="option-blue"' : '') +' data-level="' + level + '" value="'+ data.id +'">'+ nbsp(level) +''+ value +'</option>');
								_this.tree.find(".dd-item[data-id='"+ id +"'] > .dd-list").append($item);
							}
							else {
								$select.append('<option data-level="0" value="'+ data.id +'">'+ value +'</option>');
								_this.tree.find(".dd-list:first").append($item);
							}
							
							var content = $item.find(".dd3-content");
							
							_this.tree.nestable();
							_this.editable(content);
							_this.droppable(content);
						}
						
						_this.loading(false);
						
					});
				}
				else {
					alert("Выберите родительскую категорию и введите название");
				}
			}

			$form.find(".button-flat-remove").on("click", function(){
				$form.prev().removeClass("button-flat-hidden");
				$form.removeClass("category-add-form-active");
			});
			
			function nbsp(level){
				var t = "",
					n = 3;
				if (level > 1) n = 4;	
				for (var i=0; i<=(level+1)*n; i++){
					t += '&nbsp;'
				}
				return t + '&mdash; ';
			}
		},
		
		editable: function(items){
			var _this = this;
		
			var $items = items ? $(items) : this.tree.find(".dd3-content");
		
			$items.editable({
			    url: script_ajax,
				name: "change",
				validate: function(value, _editable) {
					if ($.trim(value) == '') {
						
						$(".editable-open").editableContainer("hide");
						
						var id = _editable.options.pk;
						
						if (confirm("Удалить категорию \""+ _editable.value +"\"? Все связи и товары этой категории будут удалены.")) {
							
							_this.loading(true);
							
							$utils.XHR("removeCategory", {
								id: id
							}, function(data){
								if (data && data !== "error"){
									_this.tree.find(".dd-item[data-id='"+ id +"']").remove();
								}
								_this.loading(false);
							});
						}
						
						return _editable.value;
					}
				},
				display: function(value) {
					$(this).html('<span class="dd-content-value">' + value + '</span>');
				} 				
			});				
		},
		
		boxLinks: {
			id: null,
			html: null,
			interval: null
		},
		
		initLinks: function(){
			var _this = this;
		
			this.tree.find(".dd-item").each(function(){
				var $item = $(this),
					links = $item.attr("data-links");
				
				if (links){
				
					var $badges = $item.find(".dd-badges:first"),
						links = JSON.parse(links);
						
					$item.data("links", links);
						
					for (var i=0; i < links.length; i++){
						$badges.append('<div data-id="'+ links[i].id +'" class="dd-badge catalog-b-'+ links[i].color +'">'+ links[i].title.substring(0, 1) +'</div>');
					}
				}
			});
			
			this.tree.on("mouseenter", ".dd-badges", function(e){
			
				var $elem = $(this),
					$item = $elem.parent();
					
				if (!$elem.text().length) return;
			
				clearTimeout(_this.boxLinks.interval);
			
				var id = $item.data("id");
					
				if (_this.boxLinks.id === id) return;
				else if (_this.boxLinks.id !== id && _this.boxLinks.html) {
					_this.boxLinks.html.remove();
					_this.boxLinks.html = null;
				}
				
				_this.boxLinks.interval = setTimeout(function(){
					
					var links = "",
						data = $item.data("links");
					
					for (var i=0; i < data.length; i++){
						
						links += '<div data-id="'+ data[i].id +'" class="dd-item-links-label catalog-b-'+ data[i].color +'">'+ data[i].title +'</div>';
						
						var items = data[i].items;
						
						if (items.length){
							for (var j=0; j < items.length; j++){
								links += '<div data-id="'+ items[j].id +'" class="dd-item-links-item">'+ items[j].title +'<div class="dd-item-links-remove">&times;</div></div>';
							}
						}
					}
					
					_this.boxLinks.id = id;
					
					_this.boxLinks.html = $('<div class="dd-item-links">'+ links +'</div>');
						
					$item.append(_this.boxLinks.html);
					
					$item.on("mouseleave", function(){
						$(this).off("mouseleave");
						if (_this.boxLinks.html) {
							_this.boxLinks.html.remove();
							_this.boxLinks.id = null;
							_this.boxLinks.html = null;
						}
					});					
					
				}, 120);
				
				$elem.on("mouseleave", function(){
					$elem.off("mouseleave");
					clearTimeout(_this.boxLinks.interval);
				});
			});
			
			this.tree.on("click", ".dd-item-links-remove", function(e){
				var $elem = $(this).parent(),
					id = $elem.data("id"),
					p_id = $elem.prevAll(".dd-item-links-label:first").data("id"),
					$item = $elem.closest(".dd-item");
					
				$elem.parent().remove();
				
				var data = $item.data("links");
				
				for (var i=0; i < data.length; i++){
					if (data[i].id == p_id){
						var items = data[i].items;
						if (items.length == 1){
							data.splice(i, 1);
							$item.find(".dd-badge[data-id='"+ p_id +"']").remove();
						}
						else {
							for (var j=0; j < items.length; j++){
								if (items[j].id == id) data[i].items.splice(j, 1);
							}
						}
					}
				}
				
				if (p_id == $provider.id){
					var elem = $provider.tree.find(".dd-item[data-id='"+ id +"']");
					if (elem.length) elem.removeClass("dd-item-hidden");
				}
				
				$item.data("links", data);
				
				_this.boxLinks.id = null;
				_this.boxLinks.html = null;
			});
		},	
		
		draggable: function(items, destroy){
		
			if (!items){
				if (destroy) {
					$(".dd-item", this.secondary).draggable('destroy');
				}
				else {
					$(".dd-item", this.secondary).draggable({
						revert: "invalid",
						revertDuration: 200
					});
				}
			}
			else if (items && destroy){
				items.attr("style", "").removeClass("ui-droppabled");
			}
		},
		
		droppable: function(items){
			var _this = this;
		
			var $items = items ? items : this.tree.find(".dd3-content");
			
			$items.droppable({
				hoverClass: "ui-droppable-hover",
				drop: function(event, ui) {
					var $elem = $(this),
						$item = $elem.parent(),
						$drop = ui.draggable,
						id = $drop.data("id");
					
					$elem.addClass("ui-droppable-active");
					$drop.addClass("ui-droppabled");
					
					$utils.onEndTransition($drop[0], function(){
						$drop.addClass("dd-item-hidden");
						_this.draggable($drop, true);
					});
					$utils.onEndAnimation($elem[0], function(){
						$elem.removeClass("ui-droppable-active");
					});			

					var title = $drop.find(".dd-content-value:first").text(),
						data = $item.data("links"),
						item = {
							id: id,
							title: title
						},
						avail = false;
						
					if (typeof data !== "object") data = [];
					
					for (var i=0; i < data.length; i++){
						if (data[i].id == $provider.id){
							data[i].items.push(item);
							avail = true;
						}
					}
					if (!avail){
						data.push({
							id: $provider.id,
							title: $provider.title,
							color: $provider.color,
							items: [item]
						});	
						$item.find(".dd-badges:first").append('<div data-id="'+ $provider.id +'" class="dd-badge catalog-b-'+ $provider.color +'">'+ $provider.title.substring(0, 1) +'</div>');
					}
					
					$item.data("links", data);
					
					console.dir($item.data("links"));
				}
			});
		},
		
		getData: function(){
		
			return this.tree.nestable("serialize");
		},
		
		getLinks: function(){
		
			var $links = {};
			
			this.tree.find(".dd-item").each(function(){
				var $item = $(this),
					links = $item.data("links");
					
				if (links && links.length){
					
					for (var i=0; i < links.length; i++){
						var id = links[i].id;
						if (!$links[id]) $links[id] = [];
						
						var items = links[i].items;
						
						if (items.length){
							for (var j=0; j < items.length; j++){
								$links[id].push(items[j].id);
							}
						}
					}
				}
			});
			
			return $links;
		}
	};
	
	var Provider = function(){};
	
	Provider.prototype = {
	
		id: null,
		
		title: null,
		
		color: null,
	
		controlAction: false,
		
		init: function(data){
			var _this = this;
			
			this.id = data.id;
			this.title = data.title;
			this.color = data.color;
			this.tree = this.syncLinks($(data.tree));
			this.control = $(data.control);
			
			this.control.on("click", function(e){
				var item = $(e.target),
					action = item.data("action");
					
				if (action){
					
					_this.controlAction = true;
					
					if (action === 'expand-all') {
						_this.expandAll();
					}
					else if (action === 'collapse-all') {
						_this.collapseAll();
					}
					item.addClass("active").siblings().removeClass("active");
				}
			});
			
			this.tree.on("click", "button[type=button]", function(){
				var button = $(this),
					item = button.parent(),
					action = button.data("action");
					
				if (action === 'expand') {
					_this.expand(item);
				}
				else if (action === 'collapse') {
					_this.collapse(item);
				}	
				if (_this.controlAction){
					_this.control.find(".active").removeClass("active");
					_this.controlAction = false;
				}
			});
			
			this.select();
		},
		
		loading: function(show){
		
			if (show) this.tree.addClass("dd-loading");
			else this.tree.removeClass("dd-loading");
		},		
		
		select: function(){
			var _this = this;
		
			var $select = $(".catalog-provider-select"),
				$select_value = $select.find(".item");
		
			$select.on("click", ".item, .toogle-menu-item", function(e){
				var $item = $(e.target);
				
				if ($item.hasClass("toogle-menu-item") && $select_value.data("id") != $item.data("id")){
					_this.loading(true);

					$select.removeClass("catalog-provider-select-active");
					$select_value.data("id", $item.data("id"));
					$select_value.children().text($item.text());
					$select_value.attr("class", "item catalog-b-" + $item.data("color"));
					_this.id = $item.data("id");
					_this.title = $item.text();
					_this.color = $item.data("color");

					$utils.XHR("changeProvider", {
						provider: $item.data("alias")
					}, function(data){
					
						$catalog.draggable(false, true);
					
						_this.tree.html(_this.syncLinks($(data)));
						
						$catalog.draggable();
						
						_this.loading(false);
					
					}, "html");
				}
				else {
					if ($select.hasClass("catalog-provider-select-active")){
						$select.removeClass("catalog-provider-select-active");
					}
					else {
						$select.addClass("catalog-provider-select-active");
					}
				}
			});
		},
		
		syncLinks: function($data){		
			var _this = this,
				links = $catalog.getLinks();
		
			$data.find(".dd-item").each(function(){
				var $item = $(this),
					id = $item.data("id");
					
				if (links[_this.id]){
					var data = links[_this.id];
					for (var i=0; i < data.length; i++){
						if (data[i] == id) $item.addClass("dd-item-hidden");
					}
				}
			});
			
			return $data;
		},
		
		expand: function(item){
			item.removeClass("dd-collapsed");
			item.find("button[data-action=collapse]:first").css("display", "block");
			item.find("button[data-action=expand]:first").css("display", "none");
		},
		
		collapse: function(item){
			item.addClass("dd-collapsed");
			item.find("button[data-action=collapse]:first").css("display", "none");
			item.find("button[data-action=expand]:first").css("display", "block");			
		},		
		
		expandAll: function(){
			this.tree.find(".dd-item").removeClass("dd-collapsed");
			this.tree.find("button[data-action=collapse]").css("display", "block");
			this.tree.find("button[data-action=expand]").css("display", "none");
		},
		
		collapseAll: function(){
			this.tree.find(".dd-item").addClass("dd-collapsed");
			this.tree.find("button[data-action=collapse]").css("display", "none");
			this.tree.find("button[data-action=expand]").css("display", "block");			
		}
	};	
	
	var $catalog = new Nestable(),
		$provider = new Provider();
		
	$catalog.init({
		tree: "#catalog-primary",
		secondary: "#catalog-secondary",
		control: "#control-primary",
		select: "#category-select"
	});
	
	$provider.init({
		id: 1,
		title: "Alright",
		color: "red",
		tree: "#catalog-secondary",
		control: "#control-secondary"
	});
	
	$content.find("#catalog-save").on("click", function(){
		var $btn = $(this);
		if (!$btn.hasClass("a-button-loading")){
			console.dir($catalog.getData());
			$btn.addClass("a-button-loading");
			$utils.XHR("saveCatalog", {
				data: $catalog.getData()
			}, function(data){
				if (data === true){
					$btn.removeClass("a-button-loading");
				}
			});
		}
	});
	
	// $("body").on("keydown", function(e){
		// if (e.ctrlKey){
			// $(this).animate({scrollTop: 150}, 600);
		// }
	// });
	
	var $utils = {};
	
	$utils.XHR = function(method, data, callback, type){
	
		if (!data) return;
	
		if ($utils.XHR.request) $utils.XHR.request.abort();
	
		var fd = new FormData;
		
		fd.append(method, JSON.stringify(data));
		
		$utils.XHR.request = new XMLHttpRequest;
		$utils.XHR.request.open("POST", script_ajax, true);
		$utils.XHR.request.onload = function(){
			if (this.status == 200 && this.responseText){
				if (callback && typeof callback === 'function'){
					$utils.XHR.request = null;
					if (type === "html"){
						callback(this.responseText);	
					}
					else {
						callback($.isJSON(this.responseText) ? JSON.parse(this.responseText) : this.responseText !== "true" ? "error" : true);	
					}
				}
			}
		};
		
		$utils.XHR.request.send(fd);
	};
	
	$utils.XHR.request = null;
	
	$utils.support = {transitions: Modernizr.csstransitions},
	$utils.transEndEventNames = {'WebkitTransition': 'webkitTransitionEnd', 'MozTransition': 'transitionend', 'OTransition': 'oTransitionEnd', 'msTransition': 'MSTransitionEnd', 'transition': 'transitionend'};
	$utils.transEndEventName = $utils.transEndEventNames[Modernizr.prefixed('transition')];
	$utils.animEndEventNames = {'WebkitAnimation': 'webkitAnimationEnd', 'MozAnimation': 'animationend', 'OAnimation': 'oAnimationEnd', 'msAnimation': 'MSAnimationEnd', 'animation': 'animationend'};
	$utils.animEndEventName = $utils.animEndEventNames[Modernizr.prefixed('animation')];

	$utils.onEndTransition = function(el, callback){
		var onEndCallbackFn = function( ev ) {
			if ( $utils.support.transitions ) {
				if( ev.target != this ) return;
				this.removeEventListener( $utils.transEndEventName, onEndCallbackFn );
			}
			if( callback && typeof callback === 'function' ) { callback.call(this); }
		};
		if( $utils.support.transitions ) {
			el.addEventListener( $utils.transEndEventName, onEndCallbackFn );
		}
		else {
			onEndCallbackFn();
		}
	};

	$utils.onEndAnimation = function(el, callback){
		var onEndCallbackFn = function( ev ) {
			if ( $utils.support.transitions ) {
				if( ev.target != this ) return;
				this.removeEventListener( $utils.animEndEventName, onEndCallbackFn );
			}
			if( callback && typeof callback === 'function' ) { callback.call(this); }
		};
		if( $utils.support.transitions ) {
			el.addEventListener( $utils.animEndEventName, onEndCallbackFn );
		}
		else {
			onEndCallbackFn();
		}
	};	
	
})();
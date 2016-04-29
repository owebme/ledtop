$(document).ready(function(){

	var script_clear = "/admin/scripts/yaimages/yaimages.php";
	var script_catalog = "/admin/scripts/catalog/";
	var script_ajax = "/cgi-bin/admin/modules/products_multi_ajax.cgi";
	
	if ($("div#multi a.multi-add").length){
		var cat_id = $(".products_add_table").attr("data-cat");
		$("div#multi a.multi-add").attr("href", "/cgi-bin/admin/engine/index.cgi?adm_act=products&cat_show="+cat_id);
		$(".batch_csv").find(".export_category").attr("href", "/export/csv/"+cat_id);
	}

	if ($("div.yaimages div.search").length){
		$("div.products_add_table a.add_tr").css("opacity", "0");
	}
	
	$("div.batch_add").find("select").change(function(){
		var id = $(this).val();
		location.replace('/cgi-bin/admin/engine/index.cgi?adm_act=products_multi&cat_edit='+id);
	});

	$("div.products_add_table a.add_tr").live("click", function(){
		var item = $(this).prev("table").children("tbody").children("tr.copy").html();
		var num = parseInt($(this).prev("table").find("tr:last").attr("data-index"))+1;
		$(this).prev("table").children("tbody").append('<tr data-index="'+num+'">'+item+'</tr>');		
		itemDroppable();
		$("div.products_add_table table td.foto div.input input.file").unbind();
		$("div.products_add_table table td.foto div.input input.file").bind({
			change: function() {
				addImgOne(this.files, this);
			}
		});
		return false;
	});
	
	$("div.products_add_table table td.name a.desc_add").live("click", function(){
		var el = $(this);
		if ($(el).attr("id") != "open" && $(el).attr("id") != "close"){
			$(el).parent().parent().append('<textarea></textarea>');
			$(el).parent().parent().children("textarea").fadeIn(400);
			$(el).html("Скрыть описание");
			$(el).attr("id", "open");
		}
		else if ($(el).attr("id") == "open"){
			$(el).parent().parent().children("textarea").fadeOut(200);
			$(el).html("Показать описание");
			$(el).attr("id", "close");
		}
		else if ($(el).attr("id") == "close"){
			$(el).parent().parent().children("textarea").fadeIn(400);
			$(el).html("Скрыть описание");
			$(el).attr("id", "open");
		}
		return false;
	});
	
	$("div.products_add_table td").live('mouseenter', function(){
		var el = $(this).parent();
		if ($(this).attr("class") != "foto" && $(this).attr("class") != "size"){
			$(el).find("td:nth-child(1)").prepend('<div class="del"><a href="#"></a></div>');
		}
	});	
	$("div.products_add_table tr").live('mouseleave', function(){
		var el = $(this);
		$(el).find("td").children("div.del").remove();
	});
	$("div.products_add_table tr").live('mouseenter mouseleave', function(e){
		var el = $(this);
		if (e.type == "mouseenter"){
			if ($(el).attr("data-id") > 0){
				$(el).find("td:nth-child(1)").prepend('<div class="edit"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&num_edit='+$(el).attr("data-id")+'" class="fa fa-pencil"></a></div>');
			}
		}
		else if (e.type == "mouseleave"){
			$(el).find("div.edit").remove();
		}
	});		
	
	$("div.products_add_table tr td div.del a").live("click", function(){
		var el = $(this);
		var tr = $(this).parent().parent().parent();
		var id = $(tr).attr("data-index");
		var p_id = $(tr).attr("data-id");
		var params = new Object();
		if (p_id > 0){
			params.product_del = p_id;
			$.post("/cgi-bin/admin/modules/products_ajax.cgi", params);
		}
		else {
			params.del_field = id;
			$.post(script_ajax, params);
		}
		$(tr).fadeOut(200, function(){
			$(this).remove();
			if ($("div.products_add_table table tbody tr").length < 2){
				var item = $("div.products_add_table table tbody tr.copy").html();
				$("div.products_add_table table tbody tr.copy").after('<tr data-index="1">'+item+'</tr>');		
				itemDroppable();
				$("div.products_add_table table td.foto div.input input.file").unbind();
				$("div.products_add_table table td.foto div.input input.file").bind({
					change: function() {
						addImgOne(this.files, this);
					}
				});				
			}
		});
		return false;
	});
	
	$("div.products_add_table td.foto div.foto").live('mouseenter', function(){
		var el = $(this);
		if ($(el).parent().prev().children("em").length){
			$(el).parent().prev().children("em").css("width", "132px").html("Или вставьте ссылку на картинку Ctrl+V");
		}
	});
	$("div.products_add_table td.foto div.foto").live('mouseleave', function(){
		var el = $(this);
		if ($(el).parent().prev().children("em").length){
			$(el).parent().prev().children("em").attr("style", "").html("Перетащите картинку сюда");
		}
		$(el).prev("div.input").children("input.text").remove();
	});
	
	$("div.products_add_table td.foto input.file").live('mouseenter', function(){
		var el = $(this);
		$(el).parent().append('<input class="text" type="text" value="">'); 
		var input = $(el).next("input.text");
		$(input).focus();
		document.onkeydown = hotkeys;
		function hotkeys(e) {
			if (!e) e = window.event;
			var k = e.keyCode;
			if (e.ctrlKey && k == 86) {
				window.setTimeout(function(){
					var url = $(input).val();
					var id = $(el).parent().parent().parent().parent().attr("data-index");
					var p_id = $(el).parent().parent().parent().parent().attr("data-id");
					if (url != ""){
						if ($(el).parent().parent().parent().children("span").length){
							$(el).parent().parent().parent().children("span").css("display", "none");
						}
						else {
							$(el).parent().parent().parent().children("img").css("display", "none");
						}
						$(el).parent().parent().parent().prepend('<div class="ajax"></div>');
						var params = new Object();
						if (p_id > 0){params.add_img_p_id = p_id;}
						else {params.add_img_id = id;}
						params.yaimages_alias_big = url;
						$.post(script_ajax, params, function(data){
							if (data != "error"){
								$(el).parent().parent().parent().children("span").remove();
								$(el).parent().parent().parent().children("img").remove();
								$(el).parent().parent().parent().find("div.ajax").replaceWith(data);
								$(el).parent().parent().parent().next("td.size").html('<div class="size">'+$(el).parent().parent().parent().find("div.size").html()+'</div>');
								$(el).parent().parent().parent().find("div.size").remove();
								$(el).parent("div.input").addClass("img").attr("title", "Кликните для смены картинки");
							}
							else {
								$(el).parent().parent().parent().find("div.ajax").remove();
								$(el).parent().parent().parent().children("span").fadeIn(0);
								$(el).parent().parent().parent().children("img").fadeIn(0);
								alert("Ссылка на изображение не является картинкой");
							}
						});
					}
				}, 100);
			}
		}
	});
	$("div.products_add_table td.foto input.file").live('mouseleave', function(){
		$(this).parent().children("input.text").remove();
	});	
	
	$("input#word_search").keyup(function(){
		if ($("div.yaimages i.pointer_search").length){
			$("div.yaimages i.pointer_search").slideUp(250, function(){
				$(this).remove();
			});
		}
	});
	
	$("input#search").live("click", function(){
		if ($("div.container_slider").attr("load") == "active"){	
			return false;
		}
	});
	
	var intervalLoading=""; 	
	if ($("input#word_search").length){
		$("input#word_search").attr("value", "Поиск:");
		$("div.container_slider").append('<div class="loading"><div></div></div>');
		$("div.container_slider").attr("load", "active");
		$("input#word_search").attr("data-search", "apple ipad");
		var params = new Object();
		params.search_word = "apple ipad";
		params.search_page = "1";	
		$.post(script_ajax, params, function(data){
			if (data != "" && $("div.container_slider").attr("load") != "error"){
				clearInterval(intervalLoading);
				$("div.container_slider div.images ul").empty().append(data);
				$("div.container_slider div.images").attr("data-page", "1");
				loadingImg();
			}
		});	
		intervalLoading = setTimeout(function(){
			$("div.container_slider").attr("load", "error");
			$("div.container_slider div.loading").fadeOut(400, function(){
				$(this).remove();
			});
			$("div.container_slider ul").html('<li class="buffer" style="display:none;">Сервис временно не доступен, попробуйте позже</li>');
			$("div.container_slider ul li.buffer").fadeIn(400);
			$("div.container_slider div.images").jCarouselLite({
				btnNext: ".arrow_right",
				btnPrev: ".arrow_left",
				mouseWheel: true,
				yaimagesUpload: script_ajax
			});
		}, 10000);		
	}
	else {
		$("div.container_slider div.images").jCarouselLite({
			btnNext: ".arrow_right",
			btnPrev: ".arrow_left",
			mouseWheel: true,
			yaimagesUpload: script_ajax
		});
		itemDroppable();		
	}
	var params = new Object();
	params.clear_upload = "clear";
	$.get(script_clear, params);	
	
	loadingImg = function() {
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
					$("div.container_slider div.loading").remove();
					$("div.container_slider").attr("load", "");
					$("div.container_slider div.images").jCarouselLite({
						btnNext: ".arrow_right",
						btnPrev: ".arrow_left",
						mouseWheel: true,
						yaimagesUpload: script_ajax
					});
					itemDroppable();
					$("div.products_add_table a.add_tr").css("opacity", "1");
				}
			});
		});
		intervalTime = setTimeout(function(){
			$("div.container_slider div.loading").remove();
			$("div.container_slider").attr("load", "");
			$("div.container_slider div.images").jCarouselLite({
				btnNext: ".arrow_right",
				btnPrev: ".arrow_left",
				mouseWheel: true,
				yaimagesUpload: script_ajax
			});
			itemDroppable();
			$("div.products_add_table a.add_tr").css("opacity", "1");
		}, 7000);
	}
	
	function itemDroppable() {
		$("div.container_slider div.images ul").sortable({
			revert: 200,
			cancel: "li.no-result, li.buffer",
			start: function(event, ui){
				var el = ui.helper;
				if (ui.helper.attr("class") == "item" || ui.helper.attr("class") == "item search"){
					$("div.container_slider div.images").css("overflow", "visible");
					$(el).find("img").animate({"height": "80"}, 300).css("border-radius", "6px");
					$(el).find("a.zoom").remove();
				}
			},
			stop: function(){
				$("div.container_slider div.images").css("overflow", "hidden");	
				$("div.container_slider div.images img").attr("style", "");
			}
		});
		$("div.products_add_table table td.foto div.foto").droppable({
			accept: "div.container_slider div.images ul li",
			hoverClass: "hover",
			drop: function(event, ui){
				var el = ui.draggable.children("img");
				var elem = $(this);
				if (!$(elem).parent().parent().find("div.ajax").length){
					alias = $(el).attr("alt");
					r_alias = $(el).attr("data-reserve");
					alias_sm = $(el).attr("src");
					var id = $(elem).parent().parent().parent().attr("data-index");
					var p_id = $(elem).parent().parent().parent().attr("data-id");
					if ($(elem).parent().parent().children("span").length){
						$(elem).parent().parent().children("span").replaceWith('<div class="ajax"></div>');
					}
					else {
						$(elem).parent().parent().children("img").replaceWith('<div class="ajax"></div>');
					}
					var params = new Object();
					if (p_id > 0){params.add_img_p_id = p_id;}
					else {params.add_img_id = id;}
					params.yaimages_alias_big = alias;
					params.yaimages_alias_reserve = r_alias;
					params.yaimages_alias_small = alias_sm;
					$.post(script_ajax, params, function(data){
						if (data != "error"){
							$(elem).parent().parent().find("div.ajax").replaceWith(data);
							$(elem).parent().parent().next("td.size").html('<div class="size">'+$(elem).parent().parent().find("div.size").html()+'</div>');
							$(elem).parent().parent().find("div.size").remove();
							$(elem).parent().find("div.input").addClass("img").attr("title", "Кликните для смены картинки");
						}
						else {
							$(elem).parent().parent().find("div.ajax").replaceWith('<span><em>Перетащите картинку сюда</em></span>');
							$(elem).parent().parent().next("td.size").empty().append('<div class="size"><p class="error">Ошибка загрузки изображения</p></div>');
							$(elem).parent().find("div.input").removeClass("img");
						}
					});
				}
			}
		});	
	}
	
	$("div.products_add_table table td.foto div.input input.file").bind({
		change: function() {
			addImgOne(this.files, this);
		}
	});

	function addImgOne(files, el) {
		var elem = el; 
		var imageType = /image.*/;
		var num = 0;
		$.each(files, function(i, file) {
			if (!file.type.match(imageType)) {
				alert('Добавляемый файл "'+file.name+'" не является картинкой');
				return true;
			}
			num++;
			if (num == 1){
				if ($(elem).parent().parent().parent().find("img").length){
					$(elem).parent().parent().parent().find("img").replaceWith('<div class="ajax"></div>');
				}
				else if ($(elem).parent().parent().parent().find("span").length){
					$(elem).parent().parent().parent().find("span").replaceWith('<div class="ajax"></div>');
				}
				var img = $('<img class="paste" style="height:52px;"/>');
				$(elem).parent().parent().parent().prepend(img);
				img.get(0).file = file;
				
				var reader = new FileReader();
				reader.onload = (function(aImg) {
					return function(e) {
						aImg.attr('src', e.target.result);
					};
				})(img);
				
				reader.readAsDataURL(file);
			}
		});
		
		setTimeout(function(){
			$(elem).parent().parent().parent().find('img.paste').each(function(){
				var uploadItem = $(this);
				var id = $(uploadItem).parent().parent().attr("data-index");
				var p_id = $(uploadItem).parent().parent().attr("data-id");
				var params = new Object();
				if (p_id > 0){params.add_img_p_id = p_id;}
				else {params.add_img_id = id;}
				params.add_image = $(uploadItem).attr("src");
				$.post(script_ajax, params, function(data){
					if (data != "error"){
						$(uploadItem).parent().find("div.ajax").replaceWith(data);
						$(uploadItem).parent().next("td.size").html('<div class="size">'+$(uploadItem).parent().find("div.size").html()+'</div>');
						$(uploadItem).parent().find("div.size").remove();
						$(uploadItem).parent().find("div.input").addClass("img").attr("title", "Кликните для смены картинки");
						$(uploadItem).remove();
					}
				});
			});
		}, 200);
	}
	
	$("div#sheettop li.first a").attr("href", $("div#main_menu div#products a").attr("href"));
	
	$("div.products_add_table div.batch_add input.button").live("click", function(){
		var el = $(this);
		if ($("div.products_add_table").attr("id") != "load"){
			var check = false;
			$("div.products_add_table table tr:not(.copy) td.name input").each(function(){
				if ($(this).val().trim() != ""){check = true;}
			});
			if (!check){
				alert("Заполните поля название товара");
			}
			else {
				var top1 = parseInt($("div#multi div.products_add_table").offset().top);
				var top2 = parseInt($("div#multi div.products_add_table div.batch_add").offset().top);
				var height = top2-top1+parseInt($("div#multi div.products_add_table div.batch_add").height())+5;
				$("div.products_add_table").attr("id", "load").append('<div style="height:'+height+'px;" class="loading"></div>');
				$("div.products_add_table div.batch_add").prepend('<div class="ajax">Ждем, идет сохранение изменений...</div>');
				$("div.products_add_table div.loading").fadeIn(200);
				$("div.products_add_table div.batch_add div.ajax").fadeIn(400);
				var data="";
				$("div.products_add_table table tr").each(function(){
					var tr = $(this);
					if ($(tr).attr("data-index") > 0){
						var id = $(tr).attr("data-index");
						var p_id="";
						if ($(tr).attr("data-id") > 0){p_id = $(tr).attr("data-id");}
						var art = $(tr).find("td.art").children("input").val().trim();
						var name = $(tr).find("td.name").children("input").val().trim();
						var desc_sm="";
						if ($(tr).find("td.name").children("textarea").length){
							desc_sm = $(tr).find("td.name").children("textarea").val();
							if (desc_sm){
								desc_sm = desc_sm.replace(/\;/g, "");								
								desc_sm = desc_sm.replace(/\r\n|\r|\n/g, "\|\_\|");
							}
						}
						var price = $(tr).find("td.price").children("input").val().trim();
						var p_count = $(tr).children("td.count").children("input").val().trim();
						data += id+';;'+p_id+';;'+art+';;'+name+';;'+desc_sm+';;'+price+';;'+p_count+';|;';
					}
				});
				var cat_id = $("div.products_add_table div.batch_add select.category").val();
				var params = new Object();
				params.add_products_cat_id = cat_id;	
				params.add_products_data = data;
				$.post(script_ajax, params, function(data){
					if (data == "ok"){
						$("div.products_add_table div.loading").fadeOut(400, function(){
							$(this).remove();
						});
						$("div.products_add_table div.batch_add div.ajax").css({"background":"none", "left":"-216px"}).html("Изменения сохранены...");
						location.replace('/cgi-bin/admin/engine/index.cgi?adm_act=products_multi&cat_edit='+cat_id);
					}
				});
			}
		}
		return false;
	});
	
	// Импорт CSV 
	$("div.batch_csv").find("input").live("mouseenter mouseleave change", function(e){
		if (e.type == "mouseenter"){
			$(this).next().addClass("hover");
		}
		else if (e.type == "mouseleave"){
			$(this).next().removeClass("hover");
		}
		else if (e.type == "change"){
			addFileUpload(this.files, this);
		}
	});
	
	function addFileUpload(files, item) {
		parent = $(item).parent().parent();
		var fileCount="";
		$.each(files, function(i, file) {
			fileCount++;
			if (fileCount == "1" && file.name.match(/\.csv/)){
				(parent).find(".ajax").remove();
				$(parent).append('<div class="ajax">Импортирование данных...</div>');
				var fileName = file.name;
				var fileSize = (file.size/1024)/1024;
				var fd = new FormData();
				fd.append('file',file);
				if (file.size > 0){
					$.ajax({
						url: "/import/csv/",
						dataType: 'html',
						data: fd,
						cache: false,
						contentType: false,
						processData: false,
						type: 'POST',
						success: function(data)
						{
							setTimeout(function(){
								if (data > 0 || data == 0){
									$(parent).find(".ajax").addClass("end").html('Импорт данных успешно завершен... Товаров: <strong>'+data+'</strong>');
									setTimeout(function(){
										$(parent).find(".ajax").animate({"opacity": "0"}, 300, function(){
											$(this).remove();
										});
									}, 2000);
								}
								else {
									alert("Ошибка загрузки данных");
									$(parent).find(".ajax").remove();
								}
							}, 300);
						}
					});	
				}
				else {
					alert("Ошибка распознавания файла, загрузка прервана");
				}				
			}
			else {
				alert("Не верный формат файла");
			}
		});
	}	
	
});

String.prototype.trim = function() {return this.replace(/^[\s\r\n\t]+|[\s\r\n\t]+$/g,'');};

function onerrorImg(data){
	$(function(){
		$("div.container_slider img#"+data).parent().remove();
	});
};

$(function(){
	if (document.getElementById("datatable-buttons")){

	var $sel_developer = $("select.developer"),
		$sel_category = $("select.category"),
		$table = $("#products-table").find("table"),
		$thead = $table.find("thead"),
		$tbody = $table.find("tbody"),
		$basket = $('#private-basket'),
		$search = $('.search-form');
		
	var fixedBasket = false;
	window.onscroll = function(){
		var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
		if (!fixedBasket && scrollTop > 374){
			fixedBasket = true;
			$basket.addClass("fixed");
		}
		else if (fixedBasket && scrollTop < 375){
			fixedBasket = false;
			$basket.removeClass("fixed");
		}
	}	
	
	if ($basket.find(".container").length){
		$basket.find("input.count").each(function(){
			var value = $(this).data("value");
			$(this).attr("value", value);
		});
	}
	
	$table.find("input.count").each(function(){
		var value = $(this).data("value");
		$(this).attr("value", value);
	});
	
	var $dataTable = $table.DataTable({
		ajax: {
			url: '/ajax/?getPrivateProducts=' + $sel_category.data("id")
		},
		order:[],
		dom: "Bfrtilp",
		buttons: [{
			extend: "excel",
			className: "btn-sm"
		}, {
			extend: "pdf",
			className: "btn-sm"
		}, {
			extend: "print",
			className: "btn-sm"
		}],	
		columns: [
			{ data: 'article' },
			{ data: 'image' },
			{ data: 'name' },
			{ data: 'color' },
			{ data: 'price' },
			{ data: 'order' },
			{ data: 'unit' },
			{ data: 'stock' },
			{ data: 'desc' }		
		],
        columnDefs: [
            { className: "art", "targets": [ 0 ] },
			{ className: "img", "targets": [ 1 ] },
			{ className: "name", "targets": [ 2 ] },
			{ className: "color", "targets": [ 3 ] },
			{ className: "price", "targets": [ 4 ] },
			{ className: "count", "targets": [ 5 ] },
			{ className: "unit", "targets": [ 6 ] },
			{ className: "stock", "targets": [ 7 ] },
			{ className: "desc", "targets": [ 8 ] }
        ],	
        language: {
			"search": "Фильтр",
            "lengthMenu": "Показано _MENU_ записей на странице",
            "zeroRecords": "Совпадающих записей не найдено",
            "info": "Страницы _PAGE_ из _PAGES_",
            "infoEmpty": "Нет записей в наличии",
            "infoFiltered": "(отфильтровано из _MAX_ записей)",
			"paginate": {
				"first":      "Первый",
				"last":       "Последний",
				"next":       "Следующая",
				"previous":   "Предыдущая"
			}			
        },		
		initComplete: function(){}			
	});
	
	$tbody.html('<td colspan="9" class="empty"><img src="/img/loading.svg" class="loader"></td>');
	
	// Изменение категории

	$sel_category.on("change", function(){
		var cat_id = $(this).val();
		if (cat_id > 0){
			var th = $thead.find("th").length;
			$thead.find("th").each(function(){
				var width = $(this).width();
				$(this).css("width", width+"px");
			});
			$dataTable.clear().draw();
			$tbody.html('<td colspan="'+th+'" class="empty"><img src="/img/loading.svg" class="loader"></td>');
			var params = new Object();
			params.getPrivateProducts = cat_id;
			$.post('/ajax/', params, function(data){
				if (data){
					data = JSON.parse(data).data;
					if (data.length){
						$dataTable.rows.add(data).draw();
						$.cookie('private_sel_category', cat_id, {expires: 365, path: '/'});
					}
					else {
						$tbody.find("td").html("<span>Товаров нет в выбранной категории</span>");   					
					}
				}
			});
		}
	});
	
	$sel_category.select2();
	
	// Добавить товар к заказу

	$table.find(".basket").live('click', function(){
		var $row = $(this).parent().parent().parent();
		var $clone = $(this).clone();
		$clone.css({
			"transition": "all 0.3s ease-out",
			"-webkit-transition": "all 0.3s ease-out"
		});
		$(this).after($clone);
		setTimeout(function(){
			$clone.css({
				"transform": "scale(3)",
				"-webkit-transform": "scale(3)",
				"opacity": "0"
			});	
			setTimeout(function(){
				$clone.remove();
			}, 500);
		}, 20);
		var article, price;
		if ($row.closest("table.related").length){
			article = $row.attr("data-art");
			price = $row.data("price");
		}
		else {
			var data = $dataTable.row($row).data();
			article = data.article;
			price = data.price;
		}
		var count = $row.find("input.count").val();
		if (count > 0){
			$row.addClass("add-basket");
			$basket.find("a:first").addClass("pulse");
			var params = new Object();
			params.addtobasket = article;
			params.cena = price;
			params.col = count;
			params.goals = false;
			$.post('/cgi-bin/basket_ajax.cgi', params, function(data){
				if (data != "") {
					setTimeout(function(){
						$row.removeClass("add-basket");
						$basket.find("a:first").removeClass("pulse");
					}, 50);
					statusPrivateBasket();
				}
			});
		}
		else {
			swal({
			  title: "Укажите количество\n товара к заказу",
			  type: "warning",
			  confirmButtonColor: "#DD6B55",
			  allowOutsideClick: true
			});		
		}
		return false;
	});		
	
	
	// Удалить товар из корзины

	$basket.find(".delete").live('click', function(){
		var $row = $(this).parent().parent();
		var article = $row.attr("data-art");
		$row.fadeOut(200, function(){
			$(this).remove();
		});
		var params = new Object();
		params.delproduct = article;
		$.post('/cgi-bin/basket_ajax.cgi', params, function(data){
			if (data != "") {
				$basket.find("#total_price").html(data);
				var counts = $basket.find("#basket_counts").html() - 1;
				if (counts == "0"){
					$basket.find(".container").slideUp(300, function(){
						$(this).remove();
						statusPrivateBasket();
					});
				}
				else {
					var word = "позиции";
					if (counts == 1){word = "позиция";}
					else if (counts > 4){word = "позиций";}
					$basket.find("a").find("strong").html('<em id="basket_counts">'+counts+'</em> '+word);
				}
			}
		});
		return false;
	});
	
	// Сопутствующие товары
	
	function dataFormatRelated(d) {
	    return '<tr data-art="'+ d.article +'" data-price="'+ d.price +'">'+
			'<td class="art">'+ d.article +'</td>'+
			'<td class="img">'+ d.image +'</td>'+
			'<td class="name">'+ d.name +'</td>'+
			'<td class="color">'+ d.color +'</td>'+
			'<td class="price">'+ d.price +'</td>'+
			'<td class="count">'+ d.order +'</td>'+
			'<td class="unit">'+ d.unit +'</td>'+
			'<td class="stock">'+ d.stock +'</td>'+
			'<td class="desc">'+ d.desc +'</td>'+
		'</tr>';
	}

	$table.find("a.related").live('click', function(){
		var $elem = $(this);
		var $row = $elem.parent().parent();
		var related = $elem.data("related");
		var params = new Object();
		params.relatedPrivateProducts = related;
		$.post('/ajax/', params, function(data){
			if (data){
				data = JSON.parse(data).data;
				if (data.length){
					var size = data.length, html="";
					for (var i=0; i < size; i++){
						html += dataFormatRelated(data[i]);
					}				
					$dataTable.row($row).child('<table class="related">' + html + '</table>').show();
				}
			}
		});
		$elem.remove();
		
		return false;
	});	
	
	// Поиск товара 
	
	$search.find("#search").on("click", function(e){
		e.preventDefault();
		var word = $search.find("#word_search").val();
		if (word.length > 1){
			var th = $thead.find("th").length;
			$thead.find("th").each(function(){
				var width = $(this).width();
				$(this).css("width", width+"px");
			});
			$dataTable.clear().draw();
			$tbody.html('<td colspan="'+th+'" class="empty"><img src="/img/loading.svg" class="loader"></td>');
			var params = new Object();
			params.searchPrivateProducts = URLEncode(word);
			$.post('/ajax/', params, function(data){
				if (data){
					data = JSON.parse(data).data;
					if (data.length){
						$dataTable.rows.add(data).draw();
					}
					else {
						$tbody.find("td").html("<span>Товары не найдены, попробуйте поменять поисковый запрос</span>");   
					}
				}
			});	
		}
	});
	
	changeCountsBasket($basket.find("input.count"));

	// Изменение кол-во товара в корзине
	
	var interval;
	function changeCountsBasket(items){
		$(items).on("keyup", function(){
			clearInterval(interval);
			var $input = $(this);
			var value = $input.data("value");
			interval = setTimeout(function(){
				var count = $input.val();
				var value = $input.data("value");
				if (count > 0){
					if (count != value){
						$input.data("value", count);
						var $row = $input.parent().parent();
						var article = $row.attr("data-art");
						var price = parseFloat($row.data("price"));
						var cena = parseFloat(price*count).toFixed(2);
						cena = String(cena).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");	
						$row.find(".cena").html(cena);
						var total = 0;
						$basket.find("td.cena").each(function(){
							var price = $(this).text();
							price = price.replace(/\s/, "");
							total = parseFloat(total+price*1);
						});
						if (total > 0){
							total = total.toFixed(2);
							total = String(total).replace(/(\d)(?=((\d{3})+)(\D|$))/, "$1 ");
						}
						$basket.find("#total_price").html(total);
						var params = new Object();
						params.addtobasketall = article;
						params.cena = price;
						params.col = count;
						$.post('/cgi-bin/basket_ajax.cgi', params);	
					}
				}
				else {
					$input.blur(function(){
						var val = $(this).val().replace(/\s/, "");
						if (!val || val == 0){
							$input.val($(this).data("value"));
						}
					});
				}
			}, 200);
		});
	}
	
	function statusPrivateBasket(){
		var params = new Object();
		params.getPrivateBasket = true;
		$.post('/ajax/', params, function(data){		
			if (data){
				$basket.replaceWith(data);
				$basket = $('#private-basket');
				var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
				if (scrollTop > 374){
					$basket.addClass("fixed");
				}
				changeCountsBasket($basket.find("input.count"));
			}
		});
	}
	
	$("input[name=user_person]").on("click", function(){
		var value = $(this).val();
		if (value == "2"){
			$("#table-details").removeClass("hide");
		}
		else {
			$("#table-details").addClass("hide");
		}
	});	
	
	$(".checkbox__box, .radiobox__box").find("input").each(function(){
		cb_styler($(this));
	});
	
	$(".checkbox__box").find("input").on("click", function(){
		cb_styler($(this));
	});
	
	$(".radiobox__box").find("input").on("click", function(){
		var $input = $(this);
		var name = $input.attr("name");
		$("input[type=radio]").each(function(){
			if ($(this).attr("name") == name && !$(this).is(':checked')){
				$(this).parent().removeClass("checked");
			}
		});
		cb_styler($input);
	});	
	
	function cb_styler(input){
		var $input = $(input);
		var $box = $input.parent();
		if ($input.is(':checked')){
			$box.addClass("checked");
		}
		else {
			$box.removeClass("checked");
		}
	}
    
	}
});
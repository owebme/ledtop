window.onload = function(){

if (document.getElementById("private-basket")){

	var $sel_developer = $("select.developer"),
		$sel_category = $("select.category"),
		$sel_group = $("select.group"),
		$table = $("#products-table"),
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
	
	// Изменение категории
	
	$sel_category.on("change", function(){
		var cat_id = $(this).val();
		var params = new Object();
		params.getPrivateGroups = cat_id;
		$.post('/ajax/', params, function(data){
			if (data){
				$sel_group.html(data);
				$.cookie('private_sel_category', cat_id, {expires: 365, path: '/'});
				$.cookie('private_sel_group', null, {expires: 0, path: '/'});
			}
		});
	});
	
	// Изменение группы категории

	$sel_group.on("change", function(){
		var group_id = $(this).val();
		if (group_id > 0){
			var th = $thead.find("th").length;
			$thead.find("th").each(function(){
				var width = $(this).width();
				$(this).css("width", width+"px");
			});
			$tbody.html('<td colspan="'+th+'" class="empty"><img src="/img/loading.svg" class="loader"></td>');
			var params = new Object();
			params.getPrivateProducts = group_id;
			$.post('/ajax/', params, function(data){
				if (data){
					if (data == "empty"){
						$tbody.find("td").html("<span>Товаров нет в выбранной категории</span>");   
					}
					else {
						$tbody.html(data);  
						$thead.find("th").css("width", "");
						sortTable();
					}
					$.cookie('private_sel_group', group_id, {expires: 365, path: '/'});
				}
			});
		}
	});
	
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
		var article = $row.attr("data-art");
		var price = $row.data("price");
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

	$table.find("a.related").live('click', function(){
		var $row = $(this).parent().parent();
		var related = $(this).data("related");
		var params = new Object();
		params.relatedPrivateProducts = related;
		$.post('/ajax/', params, function(data){
			if (data){
				$row.after(data);
			}
		});
		$(this).remove();
		
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
			$tbody.html('<td colspan="'+th+'" class="empty"><img src="/img/loading.svg" class="loader"></td>');
			var params = new Object();
			params.searchPrivateProducts = URLEncode(word);
			$.post('/ajax/', params, function(data){
				if (data){
					if (data == "empty"){
						$tbody.find("td").html("<span>Товары не найдены, попробуйте поменять поисковый запрос</span>");   
					}
					else {
						$tbody.html(data);  
						$thead.find("th").css("width", "");
						sortTable();
					}
				}
			});	
		}
	});
	
	
	changeCountsBasket($basket.find("input.count"));
}

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
	
	sortTable();
	
	function sortTable(){

		var hc = function (s, c) {return (" " + s + " ").indexOf(" " + c + " ") !== -1},
		 ac = function (e, c) {var s = e.className; if (!hc(s, c)) e.className += " " + c};
		
		prepTabs = function (t){
			var el, th, ts = (t && t.className) ? [t] : document.getElementsByTagName("table")
			for (var e in ts) {
				el = ts[e]
				if (!hc(el.className, "sortable")) continue
				if (!el.tHead) {
					th = document.createElement("thead")
					th.appendChild(el.rows[0])
					el.appendChild(th)
				}
				th = el.tHead
				ac(th, "c_0_c")
				th.title = "Сортировать"
				th.onclick = clicktab
				el.sorted = NaN
				//reset
				el.tb = el.tBodies[0]
				el.tb_res = el.tb.cloneNode(true) 
				el.th_res = th.cloneNode(true) 
				el.a_color = 0 
			}
		}
		
		var clicktab = function (e) {
			e = e || window.event
			var obj = e.target || e.srcElement;
			while (!obj.tagName.match(/^(th|td)$/i)) obj = obj.parentNode
			var i = obj.cellIndex, t = obj.parentNode, cn = obj.className, verse = /d\_\d+\_d/.test(cn);
			while (!t.tagName.match(/^table$/i)) t = t.parentNode
			var j = 0, rows = t.tb.rows, l = rows.length, c, v, vi;
			
			if (e.ctrlKey) { /* reset */
				t.replaceChild(t.tb_res, t.tb); 
				t.replaceChild(t.th_res, t.tHead); 
				prepTabs(t); 
				return;
			}
			 
			if (i !== t.sorted) {
				if (t.a_color < 9) t.a_color++ 
				else t.a_color = 1
				t.sarr = []
				for (j; j < l; j++) {
					c = rows[j].cells[i]
					v = (c) ? (c.innerHTML.replace(/\<[^<>]+?\>/g, '')) : ''
					vi = Math.round(100 * parseFloat(v)).toString()
					if (isFinite(vi)) while (vi.length < 10) vi = '0' + vi
					else vi = v
					t.sarr[j] = [vi + (j/1000000000).toFixed(10), rows[j]]
					//c.innerHTML = t.sarr[j][0]
				}
			}
			t.sarr = (verse) ? t.sarr.reverse() : t.sarr.sort()
			t.sorted = i
			
			var dir = (verse) ? "u" : "d", new_cls = dir + "_" + t.a_color + "_" + dir,
			 a_re = /[cdu]\_\d+\_[cdu]/;
			if (a_re.test(cn)) obj.className = cn.replace(a_re, new_cls)
			else obj.className = new_cls
			for (j = 0; j < l; j++) t.tb.appendChild(t.sarr[j][1])
			obj.title = "Отсортировано по " + ((verse) ? "убыванию" : "возрастанию")
		}
		prepTabs();
	}
    
};
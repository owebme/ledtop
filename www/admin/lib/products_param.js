var dirs_ajax = '/cgi-bin/admin/modules';

$(document).ready(function(){

	$("div#sheettop li.first a").attr("href", $("div#main_menu div#products a").attr("href"));

	$(".params").find(".a-button").live("click", function(){
		if (confirm('Удалить параметр?')) {
			var id = $(this).attr("data-id");
			if ($(this).parent().find("button").length == "1"){
				$(this).parent().remove();
			}
			else {
				$(this).remove();
			}
			var params = new Object();
			params.del_param = id;
			$.post(dirs_ajax+'/products_param_ajax.cgi', params);
		} else {
			return false;
		}
	});
	
	$("#add_param, #add_cat_param").live("click", function(){
		var $button = $(this);
		var $box = $button.next(); var select="";
		if ($(".multi_params").find("button").length){
			$(".multi_params").find("button").each(function(){
				var option = $(this).html();
				option = option.replace(/<em>(.+)<\/em>/, "");
				select +='<option value="'+$(this).attr("data-id")+'"> &ndash; '+option+'</option>';
			});
		}
		if (select){select ='<option style="color:#999" value="select" disabled>Селекторы</option>'+select;}
		$button.hide(0).after('<input class="normal" type="text" value=""><button class="a-button a-button-small plus">+</button><div class="select"><span>Тип:</span><select class="category"><option value="string">Строка</option>'+select+'</select></div>');
		var $input = $button.next();
		var $apply = $button.next().next();
		var $select = $button.parent().find("select");
		if (!$select.find("option[value='select']").length){
			$select.parent().hide(0);
		}
		var $category="";
		if ($(this).attr("id") == "add_cat_param" && $(".select_category").length){
			$button.after($(".select_category").html());
			$category = $button.next();
		}		
		$apply.click(function(){
			var value = $input.val();
			if (value.length < 2){
				alert("Введите название параметра");
			}
			else {
				if ($category && $category.val() == "0"){
					alert("Выберите категорию для которой создается уникальный параметр");
					return false;
				}
				$input.remove();
				$apply.remove();
				$button.show(0);
				var params = new Object();
				if ($category){
					var place = false;
					var cat_id = $category.val();
					var c_name = $category.find("option[value="+cat_id+"]").text();
					c_name = c_name.replace(/—/, "");
					c_name = c_name.replace(/^\s+/, "");
					c_name = c_name.replace(/\s+$/, "");
					params.add_main_param = value;
					params.param_type = $select.val();
					params.param_cat_id = cat_id;
					$category.remove();
					$box.find(".container").removeClass("new");
					if ($box.find("h4").length){
						$box.find("h4").each(function(){
							if ($(this).text() == c_name){
								$(this).parent().append('<button class="a-button a-button-small not-active">'+value+'<ins>&times;</ins></button>');
								$(this).parent().addClass("new");
								place = true;
							}
						});
					}
					if (!place){
						$box.append('<div class="container new"><h4>'+c_name+'</h4><button class="a-button a-button-small not-active">'+value+'<ins>&times;</ins></button></div>');
					}
					$box = $box.find(".container.new");
				}
				else {
					params.add_main_param = value;
					params.param_type = $select.val();
					$box.append('<button class="a-button a-button-small not-active">'+value+'<ins>&times;</ins></button>');
				}
				$select.parent().remove();
				$.post(dirs_ajax+'/products_param_ajax.cgi', params, function(data){
					if (data > 0){
						$box.find("button:last").attr("data-id", data);
					}
				});
			}
		});
	});
	
	$(".products_param").find("h4").find("a").live("click", function(){
		var $container = $(this).parent().next();
		if ($container.attr("class").match(/hide/)){
			$container.show(300, function(){
				$(this).removeClass("hide");
			});
		}
		else {
			$container.hide(300, function(){
				$(this).addClass("hide");
			});
		}
		return false;
	});
	
});

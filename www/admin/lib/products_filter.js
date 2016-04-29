var dirs_ajax = '/cgi-bin/admin/modules';

$(document).ready(function(){

	$("div#sheettop li.first a").attr("href", $("div#main_menu div#products a").attr("href"));
	
	$("#add_group").live("click", function(){
		var $button = $(this);
		var $box = $button.next();
		$button.hide(0).after('<div class="container">'+$(".select_category").html()+'<input class="normal" type="text" value=""><button class="a-button a-button-small plus">+</button></div>');
		var $container = $button.next();
		var $select = $container.find("select");
		var $input = $container.find("input");
		var $apply = $container.find(".a-button.plus");
		
		$apply.click(function(){
			var name = $input.val();
			var value = String($select.val());
			if (!value){
				alert("Отметьте категории");
			}
			else if (name.length < 2){
				alert("Введите название группы");
			}
			else {
				var category="";
				$select.find("option:selected").each(function(){
					var name = $(this).text();
					name = name.replace(/—/, "");
					name = name.replace(/^\s+/, "");
					name = name.replace(/\s+$/, "");
					category += name+", ";
				});
				category = category.replace(/,\s$/, "");
				var container = '<div class="group"><h4 class="name"><span>'+name+':</span> <em>'+category+'</em><ins>&times;</ins></h4><div class="container"></div></div>';
				$container.remove();
				$button.show(0);
				$box.prepend(container);
				$container = $box.find(".container:first");
				var params = new Object();
				params.add_group = name;
				params.add_group_cat_ids = value;
				$.post(dirs_ajax+'/products_filter_ajax.cgi', params, function(data){
					if (data > 0){
						$container.attr("data-id", data);
					}
				});
				addFilterToGroup();
			}
		});
	});
	
	$("#add_filter").live("click", function(){
		var $button = $(this);
		var $box = $button.next();
		$button.hide(0).after('<div class="container">'+$(".select_params").html()+'<input class="normal name_parent" type="text" value="" data-value=""><button class="a-button a-button-small plus">+</button></div>');
		var $container = $button.next();
		var $select = $container.find("select");
		var $input = $container.find(".name_parent");
		var $apply = $container.find(".a-button.plus");
		
		$select.change(function(){
			var value = $(this).val();
			if (value != "0"){
				value = value.replace(/—/, "");
				value = value.replace(/^\s+/, "");
				value = value.replace(/\s+$/, "");			
				$input.attr("data-value", value).val(value);
				if (!$container.find(".add_filter_value").length){
					$apply.after('<br><a href="#" class="add_filter_value">Добавить вариант</a>');
					$container.find(".add_filter_value").click(function(){
						$(this).before('<div class="filter_value"><input class="normal name" type="text" value="" placeholder="Название варианта"><input class="normal field" type="text" value="" placeholder="Его значение"></div>');
						var $field = $(this).prev(".filter_value").find("input.field");
						$(this).prev(".filter_value").find("input.name").keyup(function(){
							$field.val($(this).val());
						});
						return false;
					});
				}
			}
		});
		
		$apply.click(function(){
			var value = $input.attr("data-value");
			var name = $input.val();
			if (value.length < 2){
				alert("Выберите параметр");
			}
			else if (name.length < 2){
				alert("Введите название параметра");
			}
			else {
				var childs=""; var childs_li="";
				$container.find(".filter_value").each(function(){
					var name_value = $(this).find("input.name").val();
					var field_value = $(this).find("input.field").val();
					if (name_value.length > 1 && field_value.length > 0){
						childs += name_value+';'+field_value+'|';
						childs_li += '<li>'+name_value+'</li>';
					}
				});
				var container = '<div class="filter"><h4>'+name+'<ins>&times;</ins></h4>'+(childs_li?'<ul>'+childs_li+'</ul>':'')+'</div>';
				$container.remove();
				$button.show(0);
				$box.prepend(container);
				$container = $box.find(".filter:first");
				var params = new Object();
				params.add_filter = value;
				params.add_filter_name = name;
				if (childs){
					params.add_filter_childs = childs;
				}
				$.post(dirs_ajax+'/products_filter_ajax.cgi', params, function(data){
					if (data > 0){
						$container.attr("data-id", data);
					}
				});
			}
		});
	});
	
	addFilterToGroup();

	function addFilterToGroup(){
		var id="";
		$(".box_filters, .group_filters .container").sortable({
			connectWith: ".group_filters .container",
			cancel: ".group_filters h4.name",
			placeholder:"placeholder",
			revert: 200,
			start: function(event, ui){
				ui.placeholder.append("Поместить в эту область");
				$(this).find(".filter").each(function(){
					if ($(this).css("position") == "absolute"){
						id = $(this).attr("data-id");
					}
				});
			},
			stop: function(){
				if ($(".group_filters").find(".filter[data-id='"+id+"']").length){
					var group_id = $(".group_filters").find(".filter[data-id='"+id+"']").parent().attr("data-id");
					var filter_id = id;
					if (group_id && filter_id){
						var params = new Object();
						params.add_group_filter = group_id;
						params.add_group_filter_id = filter_id;
						$.post(dirs_ajax+'/products_filter_ajax.cgi', params, function(data){
							if (data > 0){
								$(".group_filters").find(".filter[data-id='"+id+"']").attr("data-id", data);
								var sort="";
								$(".group_filters").find(".container[data-id='"+group_id+"']").find(".filter").each(function(){
									sort += $(this).attr("data-id")+",";
								});
								var params = new Object();
								params.group_filter_sort_id = group_id;
								params.group_filter_sort = sort;
								$.post(dirs_ajax+'/products_filter_ajax.cgi', params);							
							}
							else {
								var sort="";
								$(".group_filters").find(".container[data-id='"+group_id+"']").find(".filter").each(function(){
									sort += $(this).attr("data-id")+",";
								});	
								var params = new Object();
								params.group_filter_sort_id = group_id;
								params.group_filter_sort = sort;
								$.post(dirs_ajax+'/products_filter_ajax.cgi', params);									
							}
						});
					}
				}
			}
		});
	}
	
	$(".box_filters").find("ins").live("click", function(){
		if (confirm('Удалить фильтр?')) {
			var $filter = $(this).parent().parent();
			var params = new Object();
			params.del_filter = $filter.attr("data-id");
			$.post(dirs_ajax+'/products_filter_ajax.cgi', params);
			$filter.fadeOut(200, function(){
				$(this).remove();
			});
		}
	});
	
	$(".group_filters").find(".filter").find("ins").live("click", function(){
		if (confirm('Удалить фильтр?')) {
			var $filter = $(this).parent().parent();
			var params = new Object();
			params.del_group_filter = $filter.attr("data-id");
			$.post(dirs_ajax+'/products_filter_ajax.cgi', params);
			$filter.fadeOut(200, function(){
				$(this).remove();
			});
		}
	});
	
	$(".group_filters").find("h4.name").find("ins").live("click", function(){
		if (confirm('Удалить группу фильтров?')) {
			var $group = $(this).parent().next();
			var params = new Object();
			params.del_group = $group.attr("data-id");
			$.post(dirs_ajax+'/products_filter_ajax.cgi', params);
			$group.parent().fadeOut(200, function(){
				$(this).remove();
			});
		}
	});

	$(".group_filters").find("h4.name").find("a.show").live("click", function(){
		$(this).parent().next().show(300, function(){
			$(this).removeClass("hide");
		});
		$(this).html('скрыть фильтры').removeClass("show").addClass("close");
		return false;
	});
	
	$(".group_filters").find("h4.name").find("a.close").live("click", function(){
		$(this).parent().next().hide(300, function(){
			$(this).addClass("hide");
		});
		$(this).html('показать фильтры').removeClass("close").addClass("show");
		return false;
	});		
	
	$(".group_filters").find("h4.name").find("a.change").live("click", function(){
		var $h4 = $(this).parent();
		var $group = $h4.parent();
		var ids = $h4.attr("data-ids").split(",");
		var name = $h4.find("span").text();
		name = name.replace(/\:/, "");
		$(this).parent().replaceWith($(".select_category").html()+'<input class="normal" type="text" value="'+name+'"><button class="a-button a-button-small ok">OK</button>');
		var $input = $group.find("input");
		var $select = $group.find("select");		
		$select.find("option").each(function(){
			var value = $(this).val();
			for (var i = 0; i < ids.length; i++) {
				if (ids[i] == value){
					$(this).attr("selected", "selected");
				}
			}
		});
		$group.find(".a-button.ok").click(function(){
			var name = $input.val();
			var value = String($select.val());
			if (!value){
				alert("Отметьте категории");
			}
			else if (name.length < 2){
				alert("Введите название группы");
			}
			else {
				var category="";
				$select.find("option:selected").each(function(){
					var name = $(this).text();
					name = name.replace(/—/, "");
					name = name.replace(/^\s+/, "");
					name = name.replace(/\s+$/, "");
					category += name+", ";
				});
				category = category.replace(/,\s$/, "");
				var show="";
				if ($(this).next().find(".filter").length){
					show = '&nbsp <a class="show" href="#">показать фильтры</a>';
				}
				var container = '<h4 class="name" data-ids="'+value+'"><span>'+name+':</span> <em>'+category+'</em>&nbsp <a class="change" href="#">изменить</a>'+show+'<ins>&times;</ins></h4>';
				$select.remove();
				$input.remove();
				$(this).remove();
				$group.prepend(container);
				var $container = $group.find(".container");
				var params = new Object();
				params.change_group = $container.attr("data-id");
				params.change_group_name = name;
				params.change_group_cat_ids = value;
				$.post(dirs_ajax+'/products_filter_ajax.cgi', params);
				addFilterToGroup();
			}			
		});
		
		return false;
	});		
	
});

var dirs_ajax = '/cgi-bin/admin/modules';

$(document).ready(function(){

	var $category = $("#category"),
		$saveButton = $("#save-group"),
		$tabsGroup = $(".tab-groups");
	
	$saveButton.click(function(){
		var name = $("#group-name").val();
		if (name.length < 2){
			alert("¬ведите название группы");
			$("#group-name").focus();
		}
		else {
			var group1="", group2="";
			$tabsGroup.find(".tab1").find("em").each(function(){
				var id = $(this).data("id");
				if (id > 0){group1 += id+'|';}
			});
			$tabsGroup.find(".tab2").find("em").each(function(){
				var id = $(this).data("id");
				if (id > 0){group2 += id+'|';}
			});
			if (!group1 && !group2){
				alert("ѕеретащите категории в колонки");
			}
			else {
				$(".save-group").prepend('<div class="ajax">Cохранение группы...</div>');
				var params = new Object();
				params.group_id = getUrlVars()["edit"];
				params.group_name = name;
				params.add_group1 = group1;
				params.add_group2 = group2;
				$.post(dirs_ajax+'/clients_group_ajax.cgi', params, function(data){
					if (data == "true"){
						$(".save-group").find(".ajax").fadeOut(300);
						location.replace('/cgi-bin/admin/engine/index.cgi?adm_act=clients_group');
					}
				});
			}
		}
	});
	
	$category.find(".subCat").live("click", function(){
		var $ul = $(this).next();
		if ($ul.hasClass("show")){
			$ul.removeClass("show");
		}
		else {
			$ul.addClass("show");
		}
	});	
	
	$("#category li, .container").sortable({
		connectWith: ".tab-groups .container",
		revert: 200,
		start: function(event, ui){
			id = $(this).data("id");
			name = $(this).text().replace(/(\n)+/, "").replace(/^\+/, "");
		},
		stop: function(){
			var $li = $category.find("li[data-id='"+id+"']");
			if (!$li.find("em").length){
				if ($li.next("ul").length){
					$li.next("ul").addClass("hide");
				}
				$li.addClass("hide").append('<em data-id="'+id+'">'+name+'</em>');
				backCategory();
			}
		}
	});	
	
	if ($tabsGroup.find("em").length){
		backCategory();
	}
	
	function backCategory(){
		$("#category").droppable({
			accept: ".tab-groups .container em",
			drop: function(event, ui){
				var $ul = $(this);
				var $elem = ui.draggable;
				var id = $elem.data("id");
				$elem.remove();
				$category.find("li[data-id=" + id + "]").each(function(){
					$(this).removeClass("hide").next("ul").removeClass("hide");
				});
			}
		});		
	}
	
	function getUrlVars() {
		var vars = {};
		var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
			vars[key] = value;
		});
		return vars;
	}	
	
});

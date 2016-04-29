$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'div.gallery_list',
			  intro: 'Список фотогалерей',
			  position: 'top'
			},
			{
			  element: 'div.gallery_list ul li a.del',
			  intro: 'Удалить галерею',
			  position: 'bottom'
			},
			{
			  element: 'div.gallery_list ul li a.lamp',
			  intro: 'Сделать активным / не активным галерею для отображения на сайте',
			  position: 'bottom'
			},
			{
			  element: 'div.three_pages ul li a.name',
			  intro: 'Кликнув на название вы перейдете к редактированию и добавлению фотографий',
			  position: 'bottom'
			},
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: 'Перейти к настройкам модуля фотогалереи',
			  position: 'bottom'
			}
		]
	});
	
	$("a#help-tour").live('click', function(){
		if ($("div.three_pages ul").html() == ""){
			var el = $(this).parent();
			$(el).html('<div class="warning">'+$(el).html()+'<span>Добавьте хотя бы одну галерею</span></div>');
			$(el).find("div.warning").find("span").animate({"opacity": "1"}, 200, "easeInSine");
			$(el).find("a#help-tour").remove();
		}
		else {
			introguide.start();
		}
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});
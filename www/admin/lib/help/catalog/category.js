$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'div.three_pages',
			  intro: 'Список категорий каталога',
			  position: 'top'
			},
			{
			  element: 'div.three_pages ul li a.del',
			  intro: 'Удалить категорию',
			  position: 'bottom'
			},
			{
			  element: 'div.three_pages ul li a.lamp',
			  intro: 'Сделать активным / не активным категорию для отображения на сайте',
			  position: 'bottom'
			},
			{
			  element: 'div.three_pages ul li span.move',
			  intro: 'Управление порядком сортировки категорий',
			  position: 'bottom'
			},	
			{
			  element: 'div.three_pages ul li a.name',
			  intro: 'Наведите на название категории и вы увидите ее адрес, кликнув на нее вы перейдете к редактированию',
			  position: 'bottom'
			},			 
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: 'Перейти к настройкам модуля каталога товаров',
			  position: 'bottom'
			}
		]
	});
	
	$("a#help-tour").live('click', function(){
		if ($("div.three_pages ul").html() == ""){
			var el = $(this).parent();
			$(el).html('<div class="warning">'+$(el).html()+'<span>Добавьте хотя бы одну категорию</span></div>');
			$(el).find("div.warning").find("span").animate({"opacity": "1"}, 200, "easeInSine");
			$(el).find("a#help-tour").remove();
		}
		else {
			introguide.start();
			setTimeout(function(){
				$("div.three_pages.introjs-relativePosition ul.level0 li[c_pid=0] div.point.last").each(function(){
					var height = $(this).parent().parent().height();
					if (!$(this).parent().parent().parent().next().length){
						$(this).css("height", (height-15)+"px");
					}				
					else {
						$(this).css("height", height+"px");
					}
				});
			}, 5);
		}
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});
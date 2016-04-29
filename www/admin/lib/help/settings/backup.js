$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'iframe.help_mysql',
			  intro: 'Резервирование / восстановление базы MySQL.<br> <b>Без технический специалистов использовать крайне не рекомендуется</b>',
			  position: 'top'
			},
			{
			  element: 'iframe.help_files',
			  intro: 'Резервирование / восстановление изображений модулей: новостей, товаров, фотогалереи, слайдера, баннеров',
			  position: 'top'
			}
		]
	});
	
	$("a#help-tour").live('click', function(){
		introguide.start();
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});
$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'div#choice-banner',
			  intro: 'Выбор редактируемого баннера',
			  position: 'bottom'
			},		
			{
			  element: 'div.banner_container div.banner',
			  intro: 'Кликните в это поле, чтобы выбрать файл изображения вашего баннера в формате: png, jpg, gif, bmp',
			  position: 'bottom'
			},
			{
			  element: 'div.banner_container div.roulette-width input',
			  intro: 'Изменение ширины баннера',
			  position: 'top'
			},
			{
			  element: 'div.banner_container div.roulette-height input',
			  intro: 'Изменение высоты баннера',
			  position: 'left'
			},
			{
			  element: 'div.top-panel ul li.designs',
			  intro: 'Вернуться к конструктору баннеров',
			  position: 'bottom'
			}			
		]
	});

	$("a#help-tour").live('click', function(){
		introguide.start();
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});
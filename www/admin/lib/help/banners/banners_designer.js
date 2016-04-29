$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'div#choice-banner',
			  intro: '¬ыбор редактируемого баннера',
			  position: 'bottom'
			},		
			{
			  element: 'table.banners-img td.help_img1',
			  intro: '«амена первого изображени€, выбор его скорости перемещени€.  ликнув на изображение, по€витс€ библиотека дл€ замены текущего изображени€',
			  position: 'bottom'
			},
			{
			  element: 'table.banners-img td.help_img2',
			  intro: '«амена второго изображени€, выбор его скорости перемещени€.  ликнув на изображение, по€витс€ библиотека дл€ замены текущего изображени€',
			  position: 'bottom'
			},
			{
			  element: 'table.banners-img td.help_bg div.img div.foto',
			  intro: '«амена фонового изображени€ баннера.  ликнув на изображение, по€витс€ библиотека и поиск фоновых изображений',
			  position: 'bottom'
			},
			{
			  element: 'table.banners-text',
			  intro: 'ƒоступный функционал',
			  position: 'top'
			},
			{
			  element: 'div.repeat',
			  intro: '¬ыбор интервала, через который баннер повторит цикл анимации по новой или откл. анимацию совсем',
			  position: 'bottom'
			},
			{
			  element: 'div.choice-border',
			  intro: '«акругление углов баннера',
			  position: 'bottom'
			},
			{
			  element: 'div.banner_container div.banner',
			  intro: 'Ћевой кнопкой мыши вы можете перемещать изображени€ и текст, задава€ им свое расположение',
			  position: 'top'
			},			
			{
			  element: 'div.banner_container div.roulette-width input',
			  intro: '»зменение ширины баннера',
			  position: 'top'
			},
			{
			  element: 'div.banner_container div.roulette-height input',
			  intro: '»зменение высоты баннера',
			  position: 'left'
			},
			{
			  element: 'div.panel-buttons input.create',
			  intro: '—делайте предпросмотр баннера',
			  position: 'left'
			},
			{
			  element: 'div.panel-buttons input.reset',
			  intro: '—бросить настройки баннера по умолчанию',
			  position: 'bottom'
			},
			{
			  element: 'table.banners-img td.bg div.link',
			  intro: '¬озможность установить ссылку на баннер',
			  position: 'bottom'
			},
			{
			  element: 'div.top-panel ul li.upload',
			  intro: '“акже есть возможность загрузить свой баннер в формате png, jpg, gif, bmp',
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
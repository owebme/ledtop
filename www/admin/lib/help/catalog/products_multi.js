$(document).ready(function(){

	var help_search = 'Результат поиска и буфер изображений (лента изображений). Из этой ленты вы можете перетаскивать картинки в таблицу выше в столбец «Фотография», также данную область возможно использовать как буфер изображений, перетащите файлы изображений с рабочего стола в нее';
	
	if (!$("div.yaimages div.search").length){
		help_search = 'Данная область предназначена для буфера изображений (лента изображений). Перетащите файлы изображений с рабочего стола в нее. Из этой ленты вы можете перетаскивать картинки в таблицу выше в столбец «Фотография»';
	}

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'div.products_add_table table',
			  intro: 'Таблица для работы с товарами',
			  position: 'top'
			},
			{
			  element: 'div.yaimages div.search',
			  intro: 'Поиск по базе изображений',
			  position: 'bottom'
			},
			{
			  element: 'div.yaimages div.container_slider div.images',
			  intro: help_search,
			  position: 'top'
			},
			{
			  element: 'div.yaimages div.add_images div.input',
			  intro: 'Добавление картинок в ленту изображений через «Обзор»',
			  position: 'left'
			},			
			{
			  element: 'div.products_add_table table tr#first td.foto',
			  intro: 'Кликните для смены картинки или перетащите картинку из рабочего стола, чтобы заменить текущее изображение',
			  position: 'bottom'
			},
			{
			  element: 'div.products_add_table td.help_foto',
			  intro: 'Вставлять картинки возможно 4-мя способами: 1) кликнуть в эту область и выбрать файл 2) перетащить картинку из ленты изображений ниже 3) перетащить файл изображения с рабочего стола<br> 4) скопировать адрес картинки в интернете и вставить по средством Ctrl+V',
			  position: 'bottom'
			},
			{
			  element: 'div.products_add_table div.batch_add',
			  intro: 'Выбор категории импортируемых товаров',
			  position: 'bottom'
			},
			{
			  element: 'div.batch_csv',
			  intro: 'У вас также есть возможность загружать и выгружать прайс вашего каталога в формате CSV',
			  position: 'left'
			},	
			{
			  element: 'a.multi-add.back',
			  intro: 'Вернуться к каталогу товаров',
			  position: 'bottom'
			},
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: 'Перейти к настройкам модуля каталог товаров',
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
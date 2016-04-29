$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_name',
			  intro: 'Выводится при наличии нескольких фотогалерей',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_theme',
			  intro: 'Темы оформления представленны ниже',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_script',
			  intro: 'Рекомендуем перебробовать все, выберите какой вам понравится',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_show_all',
			  intro: 'Выводить все фотографии со всех фотогалерей не разделяя',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_hide_resize',
			  intro: 'Запретить редактирование авторазмера для загружаемых фотографий',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new div.watermark-settings div.watermark-img',
			  intro: 'Кликните в это поле, чтобы выбрать файл водяного знака или введите свой текст справа',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new div.watermark-fonts div.container',
			  intro: 'Вы можете использовать свой текст для нанесения водяного знака на фотографии',
			  position: 'left'
			},	
			{
			  element: 'table#page_new tr.help_watermark_pos',
			  intro: 'Расположение нанесения водяного знака',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_opacity',
			  intro: 'Выберите прозрачность',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_watermark_type',
			  intro: 'Возможность нанесения на большую и маленькую фотографию',
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
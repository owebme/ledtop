$(document).ready(function(){

	var introguide_gallery = introJs();
	introguide_gallery.setOptions({
		steps: [
			{
			  element: 'div#tabs ul li a#click_addfoto',
			  intro: 'Перейти к добавлению фотографий',
			  position: 'bottom'
			},		
			{
			  element: 'div#fotogal ul',
			  intro: 'Перечень фотографий',
			  position: 'top'
			},
			{
			  element: 'div#fotogal ul li a.zoom_foto',
			  intro: 'Увеличение фотографии',
			  position: 'bottom'
			},
			{
			  element: 'div#fotogal ul li a.del_foto',
			  intro: 'Удалить фотографию',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_name',
			  intro: 'Название фотогалереи',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_show',
			  intro: 'Управлять, отображать / не отображать фотогалерею на сайте',
			  position: 'bottom'
			},			
			{
			  element: 'span.mceEditor',
			  intro: 'Редактирование описания галереи',
			  position: 'top'
			},
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: 'Перейти к настройкам модуля фотогалереи',
			  position: 'bottom'
			}
		]
	});
	
	var introguide_gallery_new = introJs();
	introguide_gallery_new.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_name',
			  intro: 'Название фотогалереи',
			  position: 'bottom'
			},
			{
			  element: 'span.mceEditor',
			  intro: 'Редактирование описания галереи',
			  position: 'top'
			},
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: 'Перейти к настройкам модуля фотогалереи',
			  position: 'bottom'
			}
		]
	});	
	
	var introguide_photo = introJs();
	introguide_photo.setOptions({
		steps: [
			{
			  element: 'div#addfoto p.help_auto_small',
			  intro: 'Создание маленькой фотографии из большой',
			  position: 'bottom'
			},		
			{
			  element: 'div#addfoto textarea.help_desc_big',
			  intro: 'Подробное описание фотографии, при увеличении (опционально)',
			  position: 'bottom'
			},
			{
			  element: 'div#addfoto div.help_desc_small',
			  intro: 'Краткое описание фотографии, при наведении (опционально)',
			  position: 'top'
			},
			{
			  element: 'div#addfoto div.help_resize_big',
			  intro: 'Автоматический размер загружаемой большой фотографии (ширина / высота для вертикальных фото / высота для горизонтальных)',
			  position: 'bottom'
			},
			{
			  element: 'div#addfoto div.help_resize_small',
			  intro: 'Автоматический размер загружаемой малой фотографии (ширина / высота)',
			  position: 'bottom'
			},
			{
			  element: 'div#addfoto div.hdr',
			  intro: 'Собственная технология для работы с изображениями: нормализует цвета, восстанавливает баланс белого, делает картинку более контрастной',
			  position: 'top'
			}
		]
	});	
	
	$("a#help-tour").live('click', function(){
		if ($("table#page_new td.name_main").html() == "Новая фотогалерея"){
			introguide_gallery_new.start();
		}
		else if ($("div#tabs ul li a#click_fotogal").parent().attr("class") == "activetab"){
			introguide_gallery.start();
		}
		else if ($("div#tabs ul li a#click_addfoto").parent().attr("class") == "activetab"){
			introguide_photo.start();
		}
		$("div.highslide-container").css("z-index", "9999999999");
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});
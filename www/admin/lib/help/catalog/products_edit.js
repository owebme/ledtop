$(document).ready(function(){

	var help_desc = 'Редактирование краткого описания товара (анонс)';
	if ($("textarea").length == "2"){
		help_desc = 'Редактирование полного описания товара';
	}

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'a.multi-add',
			  intro: 'Пакетное добавление товаров',
			  position: 'bottom'
			},
			{
			  element: 'td.help_photo_big',
			  intro: 'Большая фотография товара. Вы можете найти в интернете фотографию к товару, скопировать ее адрес в буфер, далее навести курсор на это поле и нажать Ctrl+V, после чего фотография автоматически загрузится',
			  position: 'right'
			},			
			{
			  element: 'p.help_auto_small',
			  intro: 'Создание маленькой фотографии из большой',
			  position: 'bottom'
			},
			{
			  element: 'td.help_photo_small',
			  intro: 'Малая фотография товара. После добавления фотографии вы сможете поиграть с настройками изображения, а также обрезать изображение при необходимости',
			  position: 'right'
			},		
			{
			  element: 'table#page_new tr.help_name',
			  intro: 'Название товара',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_parent',
			  intro: 'Выберите принадлежность данного товара к категории',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_price',
			  intro: 'Цена товара',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_price_old',
			  intro: 'Старая цена товара',
			  position: 'bottom'
			},				
			{
			  element: 'table#page_new tr.help_art',
			  intro: 'Артикул товара',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_avail',
			  intro: 'Наличие товара на складе',
			  position: 'bottom'
			},				
			{
			  element: 'table#page_new tr.help_show',
			  intro: 'Управлять, отображать / не отображать товар на сайте',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_hit',
			  intro: 'Добавить товар в хиты на главную страницу',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_spec',
			  intro: 'Добавить товар в спец. предложение на главную страницу',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_new',
			  intro: 'Добавить товар в новинки на главную страницу',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new a.open_settings',
			  intro: 'Показать настройки изображения',
			  position: 'top'
			},
			{
			  element: 'table#page_new div.foto_settings',
			  intro: 'Собственная технология для работы с изображениями: нормализует цвета, восстанавливает баланс белого, делает картинку более контрастной',
			  position: 'top'
			},
			{
			  element: 'table#page_new a.show_autoresize',
			  intro: 'Показать параметры автоматического изменения изображения (ниже переходим к ним)',
			  position: 'top'
			},			
			{
			  element: 'table#page_new tr.help_resize_big',
			  intro: 'Автоматический размер загружаемой большой фотографии (ширина / высота)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_resize_small',
			  intro: 'Автоматический размер загружаемой малой фотографии (ширина / высота)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new span.help_crop',
			  intro: 'Обрезает при необходимости края изображения, задавая фиксированный размер',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_resize_more',
			  intro: 'Автоматический размер дополнительных фотографий (ширина / высота)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_desc_small',
			  intro: 'Краткое описание товара (опционально)',
			  position: 'bottom'
			},	
			{
			  element: 'tr.help_recomend',
			  intro: 'Добавление рекумендуемых товаров с привязкой к данному товару (отображается в подробной карточке товара)',
			  position: 'right'
			},
			{
			  element: 'table#page_new tr.help_add_params a.ext',
			  intro: 'Показать расширенные настройки товара (ниже переходим к ним)',
			  position: 'top'
			},
			{
			  element: 'table#page_new tr.help_add_photo',
			  intro: 'Дополнительные фотографии к товару',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_products_reviews',
			  intro: 'Отзывы покупателей. Вам будут приходить отзывы с сайта для одобрения. Вы также может добавлять свои отзывы',
			  position: 'left'
			},			
			{
			  element: 'table#page_new tr.help_alias',
			  intro: 'Адрес товара (alias)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_maket',
			  intro: 'Любой товар можно привязывать к макету (HTML-шаблону). Шаблоны сайта создаются / редактируются по <a target="_blank" href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&num_edit=1">адресу</a>',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.redirect',
			  intro: 'Возможность сделать переадресацию товара (редирект 301)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_header',
			  intro: 'Отображать / не отображать заголовок товара (H1). Иногда требуется создать другой &lt;h1&gt;Заголовок&lt;/h1&gt; отличный от названия товара',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_meta-title',
			  intro: 'Редактирование тайтла товара (title)',
			   position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-desc',
			  intro: 'Редактирование Meta Description товара',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-key',
			  intro: 'Редактирование Meta Keywords товара',
			  position: 'bottom'
			},			
			{
			  element: 'span#elm1_sm_parent',
			  intro: help_desc,
			  position: 'top'
			},
			{
			  element: 'span#elm1_parent',
			  intro: 'Редактирование полного описания товара',
			  position: 'top'
			},	
			{
			  element: 'div.save_content div.check_save',
			  intro: 'Возможность мгновенного сохранения контента, для этого отметьте опцию и нажмите сохранить',
			  position: 'top'
			},
			{
			  element: 'div.save_content a.preview_page',
			  intro: 'Предпросмотр товара, предварительно сделайте сохранение',
			  position: 'top'
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
		$("div.foto_settings").fadeIn(600);
		$("table.ext_param").fadeIn(600);
		$("table.autoresize").fadeIn(600);
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});
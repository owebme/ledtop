$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_name',
			  intro: 'Название категории',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_image',
			  intro: 'Обложка категории',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_image_url',
			  intro: 'Вы можете вставить ссылку на картинку в интернете, после чего она автоматически загрузится',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_parent',
			  intro: 'Установить принадлежность данной категории к уже существующим категориям, например сделать текущюю категорию подразделом. Если не требуется создавать подраздел, оставьте «Верхний уровень»',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_show_menu',
			  intro: 'Управлять, отображать / не отображать категорию на сайте',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new td.name a.ext',
			  intro: 'Показать расширенные настройки категории (ниже переходим к ним)',
			  position: 'top'
			},			
			{
			  element: 'table#page_new tr.help_alias',
			  intro: 'Адрес категории (alias)',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_maket',
			  intro: 'Любую категорию можно привязывать к макету (HTML-шаблону). Шаблоны сайта создаются / редактируются по <a target="_blank" href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&num_edit=1">адресу</a>',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.redirect',
			  intro: 'Возможность сделать переадресацию категории (редирект 301)',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.autoresize',
			  intro: 'Автоматический размер загружаемой картинки (ширина и высота в px)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_header',
			  intro: 'Отображать / не отображать заголовок категории (H1). Иногда требуется создать другой &lt;h1&gt;Заголовок&lt;/h1&gt; отличный от названия категории',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_hide',
			  intro: 'Возможность скрыть категорию от поисковиков. По адресу страницы сайт будет отвечать 404 ошибкой',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_hide_child',
			  intro: 'Возможность скрывать из меню подразделы текущей категории',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_hide_child_count',
			  intro: 'Количество скрываемых подразделов, без указания количества будут скрыты все',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_meta-title',
			  intro: 'Редактирование тайтла категории (title)',
			   position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-desc',
			  intro: 'Редактирование Meta Description категории',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-key',
			  intro: 'Редактирование Meta Keywords категории',
			  position: 'bottom'
			},
			{
			  element: 'span#elm1_sm_parent',
			  intro: 'Редактирование краткого описания категории (анонс, над товарами)',
			  position: 'top'
			},
			{
			  element: 'span#elm1_parent',
			  intro: 'Редактирование полного описания категории (под товарами)',
			  position: 'top'
			},	
			{
			  element: 'div.save_content div.check_save',
			  intro: 'Возможность мгновенного сохранения контента, для этого отметьте опцию и нажмите сохранить',
			  position: 'top'
			},
			{
			  element: 'div.save_content a.preview_page',
			  intro: 'Предпросмотр категории, предварительно сделайте сохранение',
			  position: 'top'
			},				
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: 'Перейти к настройкам модуля каталог товаров',
			  position: 'bottom'
			},
			{
			  element: 'a#click_pages',
			  intro: 'Не перезагружая страницу, возможно перейти к перечню категорий каталога',
			  position: 'bottom'
			}			
		]
	});
	
	$("a#help-tour").live('click', function(){
		introguide.start();
		$("table.ext_param").fadeIn(600);
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});
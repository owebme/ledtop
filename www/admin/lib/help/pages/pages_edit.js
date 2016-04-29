$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_name',
			  intro: 'Название страницы',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_sort',
			  intro: 'Порядок сортировки страницы',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_parent',
			  intro: 'Установить принадлежность данной страницы к уже существующим страницам, например сделать текущюю страницу подразделом. Если не требуется создавать подраздел, оставьте «Верхний уровень»',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_show_menu',
			  intro: 'Управлять, отображать / не отображать страницу в меню на сайте',
			  position: 'bottom'
			},				
			{
			  element: 'table#page_new tr.help_feedback',
			  intro: 'Добавить в конец страницы обратную связь. Указать почту для приема писем возможно в модуле «<a target="_blank" href="/cgi-bin/admin/engine/index.cgi?adm_act=settings">Настройки</a>»',
			  position: 'bottom'
			},		
			{
			  element: 'table#page_new tr.help_sitemap',
			  intro: 'Сделать страницу картой сайта',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new td.name a.ext',
			  intro: 'Показать расширенные настройки страницы (ниже переходим к ним)',
			  position: 'top'
			},			
			{
			  element: 'table#page_new tr.help_alias',
			  intro: 'Адрес страницы (alias)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_maket',
			  intro: 'Любую страницу можно привязывать к макету (HTML-шаблону). Шаблоны сайта создаются / редактируются по <a target="_blank" href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&num_edit=1">адресу</a>',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.redirect',
			  intro: 'Возможность сделать переадресацию страницы (редирект 301)',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_header',
			  intro: 'Отображать / не отображать заголовок страницы (H1). Иногда требуется создать другой &lt;h1&gt;Заголовок&lt;/h1&gt; отличный от названия страницы',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_hide',
			  intro: 'Возможность скрыть страницу от поисковиков. По адресу страницы сайт будет отвечать 404 ошибкой',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_hide_child',
			  intro: 'Возможность скрывать из меню подразделы текущей страницы',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_hide_child_count',
			  intro: 'Количество скрываемых подразделов, без указания количества будут скрыты все',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_meta-title',
			  intro: 'Редактирование тайтла страницы (title)',
			   position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-desc',
			  intro: 'Редактирование Meta Description страницы',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-key',
			  intro: 'Редактирование Meta Keywords страницы',
			  position: 'bottom'
			},
			{
			  element: 'span.mceEditor',
			  intro: 'Редактор текста. В нем возможно все, что касается текста, картинок, таблиц, ссылок и т.д.',
			  position: 'top'
			},
			{
			  element: 'div.save_content div.check_save',
			  intro: 'Возможность мгновенного сохранения контента, для этого отметьте опцию и нажмите сохранить',
			  position: 'top'
			},
			{
			  element: 'div.save_content a.preview_page',
			  intro: 'Предпросмотр страницы, предварительно сделайте сохранение',
			  position: 'top'
			},		
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: 'Перейти к настройкам модуля страниц',
			  position: 'bottom'
			},
			{
			  element: 'a#click_pages',
			  intro: 'Не перезагружая страницу, возможно перейти к перечню страниц',
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
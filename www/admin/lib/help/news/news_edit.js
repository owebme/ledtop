$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_name',
			  intro: 'Название новости',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_image',
			  intro: 'Обложка новости',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_image_url',
			  intro: 'Вы можете вставить ссылку на картинку в интернете, после чего она автоматически загрузится',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_show_menu',
			  intro: 'Управлять, отображать / не отображать новость на сайте',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new td.name a.ext',
			  intro: 'Показать расширенные настройки новости (ниже переходим к ним)',
			  position: 'top'
			},			
			{
			  element: 'table#page_new tr.help_alias',
			  intro: 'Адрес новости (alias)',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_maket',
			  intro: 'Любую новость можно привязывать к макету (HTML-шаблону). Шаблоны сайта создаются / редактируются по <a target="_blank" href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&num_edit=1">адресу</a>',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.autoresize',
			  intro: 'Автоматический размер загружаемой картинки (ширина и высота в px)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.redirect',
			  intro: 'Возможность сделать переадресацию новости (редирект 301)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_header',
			  intro: 'Отображать / не отображать заголовок новости (H1). Иногда требуется создать другой &lt;h1&gt;Заголовок&lt;/h1&gt; отличный от названия новости',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_meta-title',
			  intro: 'Редактирование тайтла новости (title)',
			   position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-desc',
			  intro: 'Редактирование Meta Description новости',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-key',
			  intro: 'Редактирование Meta Keywords новости',
			  position: 'bottom'
			},
			{
			  element: 'span#elm1_sm_parent',
			  intro: 'Редактирование краткого содержания новости (анонс)',
			  position: 'top'
			},
			{
			  element: 'span#elm1_parent',
			  intro: 'Редактирование полного содержания новости',
			  position: 'top'
			},	
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: 'Перейти к настройкам модуля новостей',
			  position: 'bottom'
			},
			{
			  element: 'a#click_pages',
			  intro: 'Не перезагружая страницу, возможно перейти к перечню новостей',
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
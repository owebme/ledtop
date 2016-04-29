$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_sort',
			  intro: 'Выбор способа сортировки: по позициям, названию, дате',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_quick_save',
			  intro: 'Возможность быстрого сохранения страниц без перезагрузки',
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
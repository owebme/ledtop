$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_count',
			  intro: ' оличество отображаемых новостей (касаетс€ анонса новостей)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_sort',
			  intro: '¬ыбор способа сортировки: по дате и названию',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_theme',
			  intro: '“ема оформлени€: серый, зеленый, синий, фиолетовый, красный',
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
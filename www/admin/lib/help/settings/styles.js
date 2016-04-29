$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'a.save_css.button',
			  intro: 'Для удобства доступно сохранение изменений комбинацией клавиш Ctrl+S',
			  position: 'left'
			}	
		]
	});
	
	$("a#help-tour").live('click', function(){
		introguide.start();
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});
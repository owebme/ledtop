$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'a.save_maket.button',
			  intro: 'Для удобства доступно сохранение изменений комбинацией клавиш Ctrl+S',
			  position: 'left'
			},		
			{
			  element: 'div.makets',
			  intro: 'Любой шаблон возможно привязывать индивидуально к странице, новости, товару и т.д.',
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
$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'div.tab_sendmail',
			  intro: 'Табло отправленных и не отправленных сообщений',
			  position: 'top'
			},
			{
			  element: 'div.send_count',
			  intro: 'Установленный лимит, количество отправленных писем за раз',
			  position: 'left'
			},
			{
			  element: 'div.send_email',
			  intro: 'Статус панель по отправленным письмам',
			  position: 'top'
			},
			{
			  element: 'div.interval',
			  intro: 'Установленный интервал между письмами в секундах',
			  position: 'top'
			},	
			{
			  element: 'a.clear_mail',
			  intro: 'Очистить очередь между письмами',
			  position: 'left'
			},			 
			{
			  element: 'a.send_mail',
			  intro: 'Запустить рассылку',
			  position: 'left'
			},
			{
			  element: 'div.sendmail_theme',
			  intro: 'Заголовок (тема) письма для получателя',
			  position: 'top'
			},
			{
			  element: '#elm1_parent',
			  intro: 'Содержание письма для рассылки. Вы может добавлять текст, картинки, весь необходимый материал для рассылки',
			  position: 'top'
			},
			{
			  element: 'a.ajaxSave',
			  intro: 'Сохранить содержание письма',
			  position: 'top'
			}			
		]
	});
	
	$("a#help-tour").live('click', function(){
		introguide.start();
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});
$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_title',
			  intro: 'Основной тайтл сайта. Он подставляется к каждой страницы если тайтл не задан для нее индивидуально',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_cache',
			  intro: 'Включите эту опцию, она заметно ускорит работу сайта, настоятельно рекомендуется для интернет-магазинов',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_main_page',
			  intro: 'Наведите на «Главная страница», нажмите «Изменить» и вы сможете назначить любую главную страницу для вашего сайта',
			  position: 'bottom'
			},				
			{
			  element: 'div#pages div.help_contacts',
			  intro: 'Контактные данные, отображение на всех страницах сайта',
			  position: 'left'
			},
			{
			  element: 'div#pages div.help_social',
			  intro: 'Вы можете организовать вход в UpleCMS через вашу любимую социальную сеть, вам не придется каждый раз вводить логин и пароль для входа в систему',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new table.help_maket',
			  intro: 'Выбор шаблона по умолчанию для каждого из модулей',
			  position: 'right'
			},
			{
			  element: 'table#page_new table.help_mysql',
			  intro: 'Установка доступов к MySQL базе',
			  position: 'right'
			},
			{
			  element: 'table#page_new tr.help_feedback',
			  intro: 'Почта для приема писем через обратную связь на сайте. Добавление обратной связи на страницу возможно в модуле страниц при создании / редактировании страницы, опция «Обратная связь»',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_orders',
			  intro: 'Почта для приема заказов интернет-магазина',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new table.help_yamarket',
			  intro: 'Реквизиты доступов в сервис яндекс.маркет, товары в формате YML автоматически формируются по адресу: <a target="_blank" href="http://'+location.hostname+'/products.xml">http://'+location.hostname+'/products.xml</a>. Инструкцию по работе с прайс-листом яндекс.маркета вы можете посмотреть <a target="_blank" href="http://help.yandex.ru/partnermarket/export/feed.xml">здесь</a>',
			  position: 'right'
			},
			{
			  element: 'table#page_new table.help_payment',
			  intro: 'Реквизиты доступов к платежной системе Robokassa. Поддержка платежной системы по <a target="_blank" href="http://www.robokassa.ru/ru/Support/SendMsg.aspx">адресу</a>',
			  position: 'right'
			},			
			{
			  element: 'table#page_new div.slideshow',
			  intro: 'Редактирование слайдера изображений на главной странице. Нажмите на «Добавить слайд» и выберите файл с изображением',
			  position: 'top'
			},	
			{
			  element: 'table#page_new div.slideshow div.help_slides.options',
			  intro: 'Автоматический размер загружаемых слайдов (ширина / высота в px)',
			  position: 'left'
			},
			{
			  element: 'table#page_new td.help_counter',
			  intro: 'Поле для вставки счетчиков: liveinternet, яндекс.метрики, google.adwords и т.д.',
			  position: 'left'
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
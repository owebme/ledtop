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
			  element: 'div.template a#help_articles',
			  intro: 'Модуль «Статьи» (публикации)',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_auth',
			  intro: 'Модуль «Авторизация пользователя»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_banners',
			  intro: 'Модуль «Баннеры»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_basket',
			  intro: 'Модуль «Корзина товаров»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_basket_ajax',
			  intro: 'Модуль «Корзина товаров мини» (добавление товара)',
			  position: 'bottom'
			},	
			{
			  element: 'div.template a#help_callback',
			  intro: 'Модуль «Обратный звонок»',
			  position: 'bottom'
			},	
			{
			  element: 'div.template a#help_catalog',
			  intro: 'Модуль «Категории каталога»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_contacts',
			  intro: 'Модуль «Контакты»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_feedback',
			  intro: 'Модуль «Обратная связь»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_gallery',
			  intro: 'Модуль «Галерея»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_name',
			  intro: 'Элементы навигации',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_news',
			  intro: 'Модуль «Новости»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_pages',
			  intro: 'Модуль «Страницы»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_private',
			  intro: 'Модуль «Личный кабинет»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_products',
			  intro: 'Модуль «Товары каталога»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_products_hit',
			  intro: 'Модуль «Хиты товаров»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_products_random',
			  intro: 'Модуль «Случайные товары»',
			  position: 'bottom'
			},	
			{
			  element: 'div.template a#help_products_recomend',
			  intro: 'Модуль «Рекомендуемые товары»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_products_related',
			  intro: 'Модуль «Соседние товары»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_products_viewed',
			  intro: 'Модуль «Просмотренные товары»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_questions',
			  intro: 'Модуль «Вопросник»',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_slideshow',
			  intro: 'Модуль «Слайд-шоу»',
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
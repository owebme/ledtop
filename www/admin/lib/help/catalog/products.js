$(document).ready(function(){

	function guide(){
	
		var items = [
			{
			  element: 'div.main_button',
			  intro: 'Показать все товары каталога',
			  position: 'bottom'
			},
			{
			  element: 'div.search_catalog',
			  intro: 'Поиск товаров по каталогу. Горячий поиск с подсказками: введите первые буквы в названии товара',
			  position: 'bottom'
			}
		];
		
		if ($("div.select_category select.category").length){
			items.push(
						{
						  element: 'div.select_category',
						  intro: 'Категории каталога. Выберите нужную вам категорию, и вам не придется ждать, вы увидите ее товары',
						  position: 'bottom'
						}		
					);
		}
		
		items.push(
			{
			  element: 'div.main_button.list',
			  intro: 'Вывод товаров списком без фотографий',
			  position: 'bottom'
			},
			{
			  element: 'div.main_button.foto',
			  intro: 'Вывод товаров c фотографиями',
			  position: 'bottom'
			},	
			{
			  element: 'a.multi-add',
			  intro: 'Пакетное добавление товаров',
			  position: 'bottom'
			}	
		);

		if (!$("div.select_category select.category").length && $("div#category_products").length){
			items.push(
						{
						  element: 'div#category_products',
						  intro: 'Категории каталога',
						  position: 'top'
						},
						{
						  element: 'div#category_products ul li span.move',
						  intro: 'Управление порядком сортировки категорий',
						  position: 'bottom'
						},
						{
						  element: 'div#category_products ul li a.show_cat',
						  intro: 'Кликайте на нужную вам категорию, и вам не придется ждать, вы увидите ее товары',
						  position: 'bottom'
						}				
					);
		}
				
		items.push(
					{
					  element: 'div#allProducts ul#product_foto li',
					  intro: 'Нажмите правую кнопку на товаре и вы сможет создать копию товара. Вы также можете менять местоположение товара перетаскивая его с места на место, также вы можете перетащить товар в нужную вам категорию, наведите курсор на товар зажмите левую кнопку мыши и тащите его влево в категорию, после отпустите',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_foto li span.price',
					  intro: 'Можете изменять цену не заходя в товар, кликните на цену и меняйте ее',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_foto li span.name',
					  intro: 'Меняйте название товара не заходя в него',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_foto li a.product_del',
					  intro: 'Удалить товар',
					  position: 'bottom'
					}			
				);

		items.push(
					{
					  element: 'div#allProducts ul#product_list li a.product_del',
					  intro: 'Удалить товар',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_list li a.product_lamp',
					  intro: 'Сделать активным / не активным товар для отображения на сайте',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_list li span.move',
					  intro: 'Управление порядком сортировки товаров',
					  position: 'bottom'
					},				
					{
					  element: 'div#allProducts ul#product_list li a#p_name',
					  intro: 'Кликнув на название вы перейдете к редактированию товара',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_list li span.price',
					  intro: 'Можете изменять цену не заходя в товар, кликните на цену и меняйте ее',
					  position: 'bottom'
					}			
				);	

		items.push(
					{
					  element: 'div.pages',
					  intro: 'Страницы категории',
					  position: 'top'
					}
				);
			
		return items;
	}
	
	$("a#help-tour").live('click', function(){
		if (!$("div#category_products").length && !$("div.select_category select.category").length){
			var el = $(this).parent();
			$(el).html('<div class="warning">'+$(el).html()+'<span>Добавьте категории и товары</span></div>');
			$(el).find("div.warning").find("span").animate({"opacity": "1"}, 200, "easeInSine");
			$(el).find("a#help-tour").remove();
		}	
		else if ($("div#allProducts ul").html() == ""){
			var el = $(this).parent();
			$(el).html('<div class="warning">'+$(el).html()+'<span>Выберите категорию с товарами</span></div>');
			$(el).find("div.warning").find("span").animate({"opacity": "1"}, 200, "easeInSine");
			$(el).find("a#help-tour").remove();
		}
		else {
			var introguide = introJs();
			introguide.setOptions({
				steps: guide()
			})			
			introguide.start();
		}
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});
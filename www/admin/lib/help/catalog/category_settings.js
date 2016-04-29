$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_sort_category',
			  intro: '¬ыбор способа сортировки дл€ категорий: по позици€м, названию, дате',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_sort_products',
			  intro: '¬ыбор способа сортировки дл€ товаров: по позици€м, названию, дате, цене',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_wide_review',
			  intro: 'ѕросмотр товаров на всю ширину контента, список категорий скрываетс€ в Select',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_count_products_cms',
			  intro: ' оличество выводимых товаров на одной страницы в CMS',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_count_products_site',
			  intro: ' оличество выводимых товаров на одной страницы на сайте',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_add_photo',
			  intro: ' оличество дополнительных фотографий к товару',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_desc',
			  intro: '¬озможность редактировать описание категории над товарами и под товарами',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_ext_desc_products',
			  intro: 'ѕри выборе, описание товара разбиваетс€ на два содержани€: справа от фотографии товара (краткое описание) и ниже под фотографией (полное описание). ќтключив опцию, описание к товару будет находитс€ только под его фотографией.',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new div.help_hide_photo_settings',
			  intro: 'ѕо умолчанию скрывать настройки изображени€ товара: HDR, резкость, контрастность, насыщенность и т.д.',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_quick_save',
			  intro: '¬озможность быстрого сохранени€ контента без перезагрузки',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new div.watermark-settings div.watermark-img',
			  intro: ' ликните в это поле, чтобы выбрать файл вод€ного знака или введите свой текст справа',
			  position: 'top'
			},	
			{
			  element: 'table#page_new div.watermark-fonts div.container',
			  intro: '¬ы можете использовать свой текст дл€ нанесени€ вод€ного знака на фотографии',
			  position: 'left'
			},	
			{
			  element: 'table#page_new tr.help_watermark_pos',
			  intro: '–асположение нанесени€ вод€ного знака',
			  position: 'top'
			},	
			{
			  element: 'table#page_new tr.help_opacity',
			  intro: '¬ыберите прозрачность',
			  position: 'top'
			},	
			{
			  element: 'table#page_new tr.help_watermark_type',
			  intro: '¬озможность нанесени€ на большую, среднюю и маленькую фотографию',
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